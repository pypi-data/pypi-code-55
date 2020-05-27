"""
Main SIMFLUX data processing pipeline.


"""
import numpy as np
from photonpy.cpp.lib import SMLM
from photonpy.smlm import util as su
#import gaussian.fitters as gaussfit
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy.io as sio
import photonpy.utils.peaks as peaks
import photonpy.utils.localizations as loc
from photonpy.utils.localizations import DataColumns
from photonpy.simflux.spotlist import SpotList
import matplotlib.patches
import math
import os,pickle
from photonpy.cpp.context import Context
import sys

import tqdm
from photonpy.cpp.estimator import Estimator
from photonpy.cpp.estim_queue import EstimQueue,EstimQueue_Results
from photonpy.cpp.roi_queue import ROIQueue
from photonpy.cpp.gaussian import Gaussian
import photonpy.cpp.spotdetect as spotdetect
from photonpy.cpp.calib import GainOffset_Calib,GainOffsetImage_Calib
from photonpy.cpp.simflux import SIMFLUX
import time

import photonpy.utils.caching as caching

import photonpy.utils.multipart_tiff as read_tiff
import photonpy.smlm.process_movie as process_movie
from photonpy.smlm.util import plot_traces

figsize=(9,7)

ModDType = SIMFLUX.modulationDType

#mpl.use('svg')

# Make sure the angles dont wrap around, so you can plot them and take mean
def unwrap_angle(ang):
    r = ang * 1
    ang0 = ang.flatten()[0]
    r[ang > ang0 + math.pi] -= 2 * math.pi
    r[ang < ang0 - math.pi] += 2 * math.pi
    return r


# Pattern angles wrap at 180 degrees
def unwrap_pattern_angle(ang):
    r = ang * 1
    ang0 = ang.flatten()[0]
    r[ang > ang0 + math.pi / 2] -= math.pi
    r[ang < ang0 - math.pi / 2] += math.pi
    return r


def print_phase_info(mod):
    for axis in [0, 1]:
        steps = np.diff(mod[axis::2, 3])
        steps[steps > np.pi] = -2 * np.pi + steps[steps > np.pi]
        print(f"axis {axis} steps: {-steps*180/np.pi}")


# Flip kx,ky,phase
def flip_mod(mod_row):
    mod_row['k'] = -mod_row['k']
    mod_row['phase'] = -mod_row['phase']
    mod_row['phase'] += np.pi
    return mod_row

# Flip modulation directions so they all align with the first modulation pattern of a particular axis
def fix_mod_angles(mod):
    mod = 1*mod
    k = mod[:,[0,1]]
    for axis in range(2):
        am = get_axis_mod(mod,axis)
#        print(f"am0: {mod[am[0]]}")
        for i in np.arange(1,len(am)):
            if np.dot(k[am[0]],k[am[i]])<0: 
#                print(f"should flip axis {am[i]}: {mod[am[i]]}")
                mod[am[i]] = flip_mod(mod[am[i]])
    return mod


def result_dir(path):
    dir, fn = os.path.split(path)
    return dir + "/results/" + os.path.splitext(fn)[0] + "/"


        
def load_mod(tiffpath):
    with open(os.path.splitext(tiffpath)[0]+"_mod.pickle", "rb") as pf:
        mod = pickle.load(pf)['mod']
        assert(mod.dtype == ModDType)
        return mod
    
    


def print_mod(reportfn, mod, pattern_frames, pixelsize):
    k = mod['k']
    phase = mod['phase']
    depth = mod['depth']
    ri = mod['relint']
    
    for i in range(len(mod)):
        reportfn(f"Pattern {i}: kx={k[i,0]:.4f} ky={k[i,1]:.4f} Phase {phase[i]*180/np.pi:8.2f} Depth={depth[i]:5.2f} "+
               f"Power={ri[i]:5.3f} ")

    for ang in range(len(pattern_frames)):
        pat=pattern_frames[ang]
        d = np.mean(depth[pat])
        phases = phase[pat]
        shifts = (np.diff(phases[-1::-1]) % (2*np.pi)) * 180/np.pi
        shifts[shifts > 180] = 360 - shifts[shifts>180]
        
        with np.printoptions(precision=3, suppress=True):
            reportfn(f"Angle {ang} shifts: {shifts} (deg) (patterns: {pat}). Depth={d:.3f}")
    
    
def equal_cache_cfg(data_fn, cfg):
    """
    Returns true if the config file associated with data file data_fn contains the same value as cfg
    """ 
    cfg_fn = os.path.splitext(data_fn)[0]+"_cfg.pickle"
    if not os.path.exists(cfg_fn):
        return False
    with open(cfg_fn,"rb") as f:
        return pickle.load(f) == cfg
    
def save_cache_cfg(data_fn, cfg):
    cfg_fn = os.path.splitext(data_fn)[0]+"_cfg.pickle"
    with open(cfg_fn,"wb") as f:
        pickle.dump(cfg,f)
    
    
def gauss2D_fit(rois_fn, ctx:Context):
    """
    Run 2D Gaussian fit on all ROIs and fit intensity/background for each pattern
    """
    roipos = np.zeros((len(rois_info),3), dtype=np.int32)
    roipos[:,0] = 0
    roipos[:,1] = rois_info['y']
    roipos[:,2] = rois_info['x']
    
class SimfluxProcessor:
    """
    Simflux processing. 
    Goal is to do all computations using the load_rois_iterator, so the full pixel data is never all in memory.
    """
    def __init__(self, src_fn, cfg, ctx:Context, chisq_threshold=4, ignore_cache=True):
        """
        chi-square threshold: Real threshold = chisq_threshold*roisize^2
        """
        self.pattern_frames = np.array(cfg['patternFrames'])
        self.src_fn = src_fn
        self.rois_fn = os.path.splitext(src_fn)[0] + "_rois.npy"
        self.ctx=ctx
        self.cfg = cfg
        self.imgshape = read_tiff.tiff_get_image_size(src_fn)
        self.sigma = cfg['sigma']
        self.roisize = cfg['roisize']
        self.pixelsize = cfg['pixelsize']
        self.spotfilter = cfg['spotfilter']
        self.threshold = cfg['detectionThreshold']
        self.maxframes = cfg['maxframes'] if 'maxframes' in cfg else -1
        
        spotDetector = spotdetect.SpotDetector(self.sigma, self.roisize, self.threshold)
        calib = process_movie.create_calib_obj(cfg['gain'],cfg['offset'],self.imgshape,ctx)
            
        if not equal_cache_cfg(self.rois_fn, cfg) or ignore_cache:
            process_movie.detect_spots(self.imgshape, spotDetector, calib, 
                               read_tiff.tiff_read_file(src_fn, cfg['startframe'], self.maxframes), 
                               self.pattern_frames.size, self.rois_fn, batch_size = 20000, ctx=ctx)
            save_cache_cfg(self.rois_fn, cfg)
        
        self.numrois = np.sum([len(ri) for ri,px in self._load_rois_iterator()])
        print(f"Num ROIs: {self.numrois}")
        
        self.IBg = None
        self.sum_fit = None
        
        self.chisq_threshold = chisq_threshold
        
        dir, fn = os.path.split(src_fn)
        self.resultsdir = dir + "/results/" + os.path.splitext(fn)[0] + "/"
        os.makedirs(self.resultsdir, exist_ok=True)
        self.resultprefix = self.resultsdir
            
        self.reportfile = self.resultprefix + "report.txt"
        with open(self.reportfile,"w") as f:
            f.write("")

    def close(self):
        ...
                
    def estimate_sigma(self, plot=True):
        estimates = []
        chisq = []
        
        with Gaussian(self.ctx).CreatePSF_XYIBgSigmaXY(self.roisize, [3,3], True) as psf:
            psf.SetLevMarParams(1e-15,40)
            for rois_info, pixels in self._load_rois_iterator():
                summed_patterns = pixels.sum(1)
                e, diag, traces = psf.Estimate(summed_patterns)
                chisq.append(psf.ChiSquare(e, summed_patterns))
                
                nant = np.where(np.sum(np.isnan(e),1)!=0)[0]
                
                if len(nant)>0:
                    print(e[nant])
                    plot_traces([traces[i] for i in nant], e[nant], psf, 2)
                    plot_traces([traces[i] for i in nant], e[nant], psf, 3)
                    raise ValueError('TODO: Fix nan results in 2D Gaussian + Sigma fit')
                                
                estimates.append(e)
         
        chisq = np.concatenate(chisq)
        estimates = np.concatenate(estimates)
        estimates = estimates[chisq<np.median(chisq)] # use the best half
        
        if plot:
            plt.figure()
            plt.hist(estimates [:,4], range=[1, 4],bins=50)
            plt.title('Sigma X')
        
            plt.figure()
            plt.hist(estimates [:,5], range=[1, 4],bins=50)
            plt.title('Sigma Y')
        
        best = np.median(estimates [:,[4,5]],0)
        print(f'Now using estimated sigma: {best}')
        
        self.cfg['sigma'] = best
        self.sigma = best
        return best
    
    def view_rois(self, summed=False, accepted=True, fits=None):
        import napari    
        
        ri, pixels = process_movie.load_rois(self.rois_fn)
        
        px = pixels[self.accepted] if accepted else pixels
        
        if summed:
            px = px.sum(1)
        
        with napari.gui_qt():
            viewer = napari.view_image(px)

            if fits is not None:
                #points = np.array([[100, 100], [200, 200], [300, 100]])
                
                coords = np.zeros((len(fits),3))
                coords[:,0] = np.arange(len(fits))
                coords[:,[2,1]] = fits[:,:2]
  
                viewer.add_points(coords, size=0.1)
                print('test')
                
        return viewer
    
    def gaussian_fitting(self):
        """
        Make sure self.IBg and self.sum_fits are known
        """
        if self.IBg is not None and self.sum_fit is not None:
            return
        
        rois_info = []
        sum_fit = []
        ibg = []
        sum_crlb = []
        sum_chisq = []
        
        sigma = np.array(self.sigma)
        
        print('2D Gaussian fitting...',flush=True)
        
        gaussfn = Gaussian(self.ctx)
        with gaussfn.CreatePSF_XYIBg(self.roisize, self.sigma, True) as psf, tqdm.tqdm(total=self.numrois) as pb:
            for ri, pixels in self._load_rois_iterator():
                summed = pixels.sum(1)
                e = psf.Estimate(summed)[0]
                sum_crlb.append(psf.CRLB(e))
                sum_chisq.append(psf.ChiSquare(e, summed))
                
                rois_info.append(ri)
                
                sh = pixels.shape # numspots, numpatterns, roisize, roisize
                pixels_rs = pixels.reshape((sh[0]*sh[1],sh[2],sh[3]))
                xy = np.repeat(e[:,[0,1]], sh[1], axis=0)
                
                ibg_, crlb_ = gaussfn.EstimateIBg(pixels_rs, sigma[None], xy,useCuda=True)
                ic = np.zeros((len(e)*sh[1],4))
                ic [:,[0,1]] = ibg_
                ic [:,[2,3]] = crlb_
                ibg.append(ic.reshape((sh[0],sh[1],4)))
                                
                sum_fit.append(e)

                pb.update(len(pixels))
        print(flush=True)
                
        self.sum_fit = np.concatenate(sum_fit)
        self.IBg = np.concatenate(ibg)
        self.sum_chisq = np.concatenate(sum_chisq)
        self.sum_crlb = np.concatenate(sum_crlb)

        rois_info = np.concatenate(rois_info)        
        roipos = np.zeros((len(rois_info),3), dtype=np.int32)
        roipos[:,0] = 0
        roipos[:,1] = rois_info['y']
        roipos[:,2] = rois_info['x']
        self.roipos = roipos
        
        plt.figure()
        plt.hist(self.sum_chisq, bins=50, range=[0,4000])
        plt.title('2D Gaussian fit chi-square')
        
        threshold = self.roisize**2 * self.chisq_threshold
        ok = self.sum_chisq < threshold

        self.roipos = self.roipos[ok]
        self.sum_fit = self.sum_fit[ok]
        self.IBg = self.IBg[ok]
        self.sum_chisq = self.sum_chisq[ok]
        self.sum_crlb = self.sum_crlb[ok]
        self.framenum = rois_info['id'][ok]
        
        self.accepted = ok
        print(f"Accepted {np.sum(ok)}/{self.numrois} spots (chi-square threshold={threshold:.1f}")
        
        area = [0,0,self.imgshape[1],self.imgshape[0]]
        self.loc_sum = loc.from_estim(self.cfg, area, self.src_fn, 
                                 self.sum_fit, self.sum_crlb, self.roipos, self.framenum)
        
        fn = self.resultprefix+'summed_fits.hdf5'
        self.loc_sum.save_picasso_hdf5(fn)

        self.spotlist = SpotList(self.loc_sum, pixelsize=self.cfg['pixelsize'], 
                            outdir=self.resultsdir, IBg=self.IBg[:,:,:2], IBg_crlb=self.IBg[:,:,2:])
        
        median_crlb_x = np.median(self.loc_sum.get_crlb()[:,0])
        median_I = np.median(self.loc_sum.get_xyI()[:,2])

        self.report(f"g2d mean I={median_I:.1f}. mean crlb x {median_crlb_x:.4f}")

        
    def estimate_patterns(self, num_angle_bins=1,num_phase_bins=10, 
                          freq_minmax=[1.5, 3], 
                          fix_phase_shifts=None, 
                          fix_depths=None,
                          show_plots=True):
        self.gaussian_fitting()
        
        fr = np.arange(len(self.loc_sum.frames))
    
        angles, pitch = self.spotlist.estimate_angle_and_pitch(
            self.pattern_frames, 
            frame_bins=np.array_split(fr, num_angle_bins), 
            ctx=self.ctx,
            freq_minmax=freq_minmax
        )
        
        num_patterns = self.pattern_frames.size
        mod = np.zeros((num_patterns),dtype=ModDType)

        print("Pitch and angle estimation: ")
        for k in range(len(self.pattern_frames)):
            angles[angles[:, k] > 0.6 * np.pi] -= np.pi  # 180 deg to around 0
            angles[:, k] = unwrap_pattern_angle(angles[:, k])
            angles_k = angles[:, k]
            pitch_k = pitch[:, k]
            self.report(f"Angle {k}: { np.rad2deg(np.mean(angles_k)) :7.5f} [deg]. Pitch: {np.mean(pitch_k)*self.pixelsize:10.5f} ({2*np.pi/np.mean(pitch_k):3.3f} [rad/pixel])")

            freq = 2 * np.pi / np.mean(pitch_k)
            kx = np.cos(np.mean(angles_k)) * freq
            ky = np.sin(np.mean(angles_k)) * freq
            mod['k'][self.pattern_frames[k], :2] = kx,ky
                        
        if num_phase_bins is not None:
            
            method = 1
            phase, depth, power = self.spotlist.estimate_phase_and_depth(mod['k'], self.pattern_frames, np.array_split(fr, num_phase_bins), method=method)
            phase_all, depth_all, power_all = self.spotlist.estimate_phase_and_depth(mod['k'], self.pattern_frames, [fr], method=method)
                
            fig = plt.figure(figsize=figsize)
            styles = [":", "-"]
            for ax, idx in enumerate(self.pattern_frames):
                for k in range(len(idx)):
                    plt.plot(unwrap_angle(phase[:, idx[k]]) * 180 / np.pi, styles[ax%len(styles)], label=f"Phase {idx[k]} (axis {ax})")
            plt.legend()
            plt.title(f"Phases for {self.src_fn}")
            plt.xlabel("Timebins"); plt.ylabel("Phase [deg]")
            plt.grid()
            plt.tight_layout()
            fig.savefig(self.resultprefix + "phases.png")
            if not show_plots: plt.close(fig)
    
            fig = plt.figure(figsize=figsize)
            for ax, idx in enumerate(self.pattern_frames):
                for k in range(len(idx)):
                    plt.plot(depth[:, idx[k]], styles[ax%len(styles)], label=f"Depth {idx[k]} (axis {ax})")
            plt.legend()
            plt.title(f"Depths for {self.src_fn}")
            plt.xlabel("Timebins"); plt.ylabel("Modulation Depth")
            plt.grid()
            plt.tight_layout()
            fig.savefig(self.resultprefix + "depths.png")
            if not show_plots: plt.close(fig)
    
            fig = plt.figure(figsize=figsize)
            for ax, idx in enumerate(self.pattern_frames):
                for k in range(len(idx)):
                    plt.plot(power[:, idx[k]], styles[ax%len(styles)], label=f"Power {idx[k]} (axis {ax})")
            plt.legend()
            plt.title(f"Power for {self.src_fn}")
            plt.xlabel("Timebins"); plt.ylabel("Modulation Power")
            plt.grid()
            plt.tight_layout()
            fig.savefig(self.resultprefix + "power.png")
            if not show_plots: plt.close(fig)
    
            # Update mod
            phase_std = np.zeros(len(mod))
            for k in range(len(mod)):
                ph_k = unwrap_angle(phase[:, k])
                mod['phase'][k] = phase_all[0, k]
                mod['depth'][k] = depth_all[0, k]
                mod['relint'][k] = power_all[0, k]
                phase_std[k] = np.std(ph_k)

            s=np.sqrt(num_phase_bins)
            for k in range(len(mod)):
                self.report(f"Pattern {k}: Phase {mod[k]['phase']*180/np.pi:8.2f} (std={phase_std[k]/s*180/np.pi:6.2f}) "+
                       f"Depth={mod[k]['depth']:5.2f} (std={np.std(depth[:,k])/s:5.3f}) "+
                       f"Power={mod[k]['relint']:5.3f} (std={np.std(power[:,k])/s:5.5f}) ")

            #mod=self.spotlist.refine_pitch(mod, self.ctx, self.spotfilter, plot=True)[2]

            if fix_phase_shifts:
                self.report(f'Fixing phase shifts to {fix_phase_shifts}' )
                phase_shift_rad = fix_phase_shifts / 180 * np.pi
                for ax in self.pattern_frames:
                    mod[ax]['phase'] = mod[ax[0]]['phase'] + np.arange(len(ax)) * phase_shift_rad

                mod=self.spotlist.refine_pitch(mod, self.ctx, self.spotfilter, plot=True)[2]

            mod_info = {"mod": mod, "pitch": pitch, "angles": angles, "phase": phase, "depth": depth, 'power': power}
            with open(os.path.splitext(self.src_fn)[0]+"_mod.pickle", "wb") as df:
                pickle.dump(mod_info, df)

        for angIndex in range(len(self.pattern_frames)):
            mod[self.pattern_frames[angIndex]]['relint'] = np.mean(mod[self.pattern_frames[angIndex]]['relint'])
            # Average modulation depth
            mod[self.pattern_frames[angIndex]]['depth'] = np.mean(mod[self.pattern_frames[angIndex]]['depth'])

        mod['relint'] /= np.sum(mod['relint'])

        if fix_depths:
            self.report(f'Fixing modulation depth to {fix_depths}' )
            mod['depth']=fix_depths

        self.report("Final modulation pattern parameters:")
        print_mod(self.report, mod, self.pattern_frames, self.pixelsize)
        
        self.mod = mod
        
    def draw_mod(self, showPlot=False):
        allmod = self.mod
        filename = self.resultprefix+'patterns.png'
        fig,axes = plt.subplots(1,2)
        fig.set_size_inches(*figsize)
        for axis in range(len(self.pattern_frames)):
            axisname = ['X', 'Y']
            ax = axes[axis]
            indices = self.pattern_frames[axis]
            freq = np.sqrt(np.sum(allmod[indices[0]]['k']**2))
            period = 2*np.pi/freq
            x = np.linspace(0, period, 200)
            sum = x*0
            for i in indices:
                mod = allmod[i]
                q = (1+mod['depth']*np.sin(x*freq-mod['phase']) )*mod['relint']
                ax.plot(x, q, label=f"Pattern {i}")
                sum += q
            ax.plot(x, sum, label=f'Summed {axisname[axis]} patterns')
            ax.legend()
            ax.set_title(f'{axisname[axis]} modulation')
            ax.set_xlabel('Pixels');ax.set_ylabel('Modulation intensity')
        fig.suptitle('Modulation patterns')
        if filename is not None: fig.savefig(filename)
        if not showPlot: plt.close(fig)
        return fig
        
        
    def set_mod(self, mod):
        self.mod = mod
        
    def plot_ffts(self):
        self.spotlist.generate_projections(self.mod, 4,self.ctx)
        self.spotlist.plot_proj_fft()
        
    def process(self):
        self.gaussian_fitting()

        # TODO: stream rois. Up to this point SimfluxProcessor works without a giant ROI array
        
        self.spotlist.rois = process_movie.load_rois(self.rois_fn)[1][self.accepted]
        
        if self.mod is None:
            raise ValueError('modulation matrix not defined (use set_mod / estimate_pattern')
        
        #self.spotlist.plot_moderr_vs_intensity(self.mod, self.spotfilter)
        
        if False:
            errs = self.spotlist.compute_modulation_chisq(self.mod, self.pattern_frames, self.spotfilter, plot=False)#, frames=np.arange(fr))
            self.report(f"Modulation qualities per axis:")
            for k in range(len(self.pattern_frames)):
                ind = self.pattern_frames[k]
                for step in range(len(ind)):
                    self.report(f"\tAxis {k}, step {step}: {errs[ind[step]]:.5f}")
        
        if False:
            moderrs = self.spotlist.compute_modulation_error(self.mod, self.spotfilter)
            self.report(f"RMS moderror: {np.sqrt(np.mean(moderrs**2)):.3f}")

        #self.spotlist.plot_modulation_chisq_timebins(self.mod, self.pattern_frames, self.spotfilter, 50)        

        if len(self.pattern_frames)==2: # assume XY modulation
            self.draw_mod()

        #self.spotlist.bias_plot2D(self.mod, self.ctx, self.spotfilter, tag='')
#        spotlist.plot_intensity_variations(mod, minfilter, pattern_frames)

        med_sum_I = np.median(self.IBg[:,:,0].sum(1))
        lowest_power = np.min(self.mod['relint'])
        depth = self.mod[np.argmin(self.mod['relint'])]['depth']
        median_intensity_at_zero = med_sum_I * lowest_power * (1-depth)
        self.report(f"Median summed intensity: {med_sum_I:.1f}. Median intensity at pattern zero: {median_intensity_at_zero:.1f}")
        self.report(f"Using spot filter: {self.spotfilter}. ")

        for k in range(len(self.mod)):
            png_file= f"{self.resultprefix}patternspots{k}.png"
            print(f"Generating {png_file}...")
            src_name = os.path.split(self.src_fn)[1]
            self.spotlist.draw_spots_in_pattern(png_file, self.mod, 
                                       k, tiffname=src_name, numpts= 2000, spotfilter=self.spotfilter)
            self.spotlist.draw_spots_in_pattern(f"{self.resultprefix}patternspots{k}.svg", self.mod, 
                                       k, tiffname=src_name, numpts= 2000, spotfilter=self.spotfilter)

        self.spotlist.draw_axis_intensity_spread(self.pattern_frames, self.mod, self.spotfilter)
        
        print(f"Running simflux fits...")
        # g2d_results are the same set of spots used for silm, for fair comparison
        sf_results,g2d_results = self.spotlist.simflux_fit(self.mod, self.ctx, spotfilter=self.spotfilter,
                                                 draw_silm_compare=False)
        
        border = 2.1
        num_removed, indices = sf_results.filter_inroi(border, border, self.roisize-border-1, self.roisize-border-1)
        self.report(f"Removing {num_removed} ({100*num_removed/len(self.IBg)}%) unconverged SIMFLUX fits")
        #g2d_results.filter_indices(indices)
        
        if None:#drift_correct:
            drift_fn = os.path.split(self.src_fn)[0]+ "/" + drift_correct
            g2d_results.drift_correct_from_file(drift_fn, 1)#len(mod))
            sf_results.drift_correct_from_file(drift_fn, 1)#len(mod))
            sf_results.plot_drift('drift' )
            
        sf_results.save_picasso_hdf5(self.resultprefix+"simflux.hdf5")
        g2d_results.save_picasso_hdf5(self.resultprefix+"g2d.hdf5")
                
        crlb = g2d_results.get_crlb()
        maxdist = 1.5*np.sqrt(np.sum(np.mean(crlb[:,[0,1]],0)**2))
        self.report(f"Linking localizations (max dist: {maxdist:.2f} pixels)...")
        sf_linked = sf_results.link_locs(self.ctx,maxdist)
        g2d_linked = g2d_results.link_locs(self.ctx,maxdist)
        
        sf_linked.save_picasso_hdf5(self.resultprefix+"simflux-linked.hdf5")
        g2d_linked.save_picasso_hdf5(self.resultprefix+"g2d-linked.hdf5")
        
        self.sf_results = sf_results
        self.sum_results = g2d_results
        
        self.sf_fit = sf_results.get_xyIBg()
        self.sf_fit[:,:2] -= sf_results.get_roipos()

#        silm_data = silm_results.save_csv_with_drift(resultprefix + "simflux.csv")
 #       g2d_data = g2d_results.save_csv_with_drift(resultprefix + "g2d.csv")
  #      sio.savemat(resultprefix + "localizations.mat", {"simflux": silm_data, "g2d": g2d_data})
        
                
    def _load_rois_iterator(self):
        return process_movie.load_rois_iterator(self.rois_fn)
    
    def report(self, msg):
        with open(self.reportfile,"a") as f:
            f.write(msg+"\n")
        print(msg)
        
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()



    
def view_napari(mov):
    import napari
    
    with napari.gui_qt():
        napari.view_image(mov)


def set_plot_fonts():
    import matplotlib as mpl
    new_rc_params = {
    #    "font.family": 'Times',
        "font.size": 15,
    #    "font.serif": [],
        "svg.fonttype": 'none'} #to store text as text, not as path
    mpl.rcParams.update(new_rc_params)
