

import numpy as np
import time
import tqdm
import os

from photonpy.cpp.gaussian import Gaussian
from photonpy.cpp.lib import SMLM
import photonpy.cpp.spotdetect as spotdetect
from photonpy.cpp.calib import GainOffset_Calib
from photonpy.cpp.calib import GainOffsetImage_Calib
from photonpy.cpp.context import Context
from photonpy.cpp.estim_queue import EstimQueue
from photonpy.cpp.estimator import Estimator
from photonpy.cpp.roi_queue import ROIQueue
import photonpy.utils.multipart_tiff as tiff

import threading

def end_of_file(f):
    curpos = f.tell()
    f.seek(0,2)
    file_size = f.tell()
    f.seek(curpos,0)
    return curpos == file_size 


def detect_spots(imgshape, sdcfg, calib, movie, sumframes, output_fn, batch_size, ctx:Context):
    sm = spotdetect.SpotDetectionMethods(ctx)

    with Context(ctx.smlm) as lq_ctx, open(output_fn, "wb") as f:
        roishape = [sdcfg.roisize,sdcfg.roisize]
        
        q,rq = sm.CreateQueue(imgshape, roishape, sdcfg, calib=calib,sumframes=sumframes, ctx=lq_ctx)
        numframes = 0
        numrois = 0
        
        def save_rois(rois_info, pixels):
            np.save(f, rois_info, allow_pickle=False)
            np.save(f, pixels, allow_pickle=False)
            nonlocal numrois
            numrois += len(rois_info)
                
        for fr,img in movie:
            q.PushFrame(img)
            numframes += 1
            
            rl = rq.Length()
            if rl>batch_size:
                save_rois(*rq.Fetch())
                   
        while q.NumFinishedFrames() < numframes//sumframes:
            time.sleep(0.1)
        
        if rq.Length()>0:
            save_rois(*rq.Fetch())
            
        return numrois


def load_rois_iterator(rois_fn):
    """
    Load rois sequentially so we can deal with very large datasets
    """
    with open(rois_fn, "rb") as f:
        while not end_of_file(f):
            rois_info = np.load(f)
            pixels = np.load(f)
            yield rois_info, pixels
            
    
def load_rois(rois_fn):
    rois_info = []
    pixels = []
    for ri,px in load_rois_iterator(rois_fn):
        rois_info.append(ri)
        pixels.append(px)
    
    return np.concatenate(rois_info), np.concatenate(pixels)


def create_calib_obj(gain,offset,imgshape,ctx):
    if type(offset)==str:
        print(f'using mean values from {offset} as camera offset')
        offset=tiff.get_tiff_mean(offset)
    
    if( type(offset)==np.ndarray):
        gain = np.ones(imgshape)*gain
        calib = GainOffsetImage_Calib(gain, offset, ctx)
    else:
        calib = GainOffset_Calib(gain, offset, ctx) 
    
    return calib


def localize(fn, cfg, output_file=None, progress_cb=None, estimate_sigma=False):
    """Perform localization on a tiff with a 2D Gaussian PSF model

    :param fn (str): .tif filename
    :param cfg: configuration dictionary for camera parameters and for
        PSF parameters.
    :param output_file: .hdf5 file where results will be saved.
    :param progress_cb: Progress callback
    :param estimate_sigma: if true, sigma will be estimated. In that case
        the sigma in cfg will be considered as initial estimate.

    :return: tuple with (EstimQueue_Result, image shape)
    """

    sigma = cfg['sigma']
    roisize = cfg['roisize']
    threshold = cfg['threshold']
    gain = cfg['gain']
    offset = cfg['offset']
    startframe = cfg['startframe'] if 'startframe' in cfg else 0
    maxframes = cfg['maxframes'] if 'maxframes' in cfg else -1
    sumframes = 1
    
    with Context() as ctx:
        imgshape = tiff.tiff_get_image_size(fn)

        gaussian = Gaussian(ctx)
            
        spotDetector = spotdetect.SpotDetector(np.mean(sigma), roisize, threshold)

        if estimate_sigma:
            psf = gaussian.CreatePSF_XYIBgSigmaXY(roisize, sigma, True)
        else:
            psf = gaussian.CreatePSF_XYIBg(roisize, sigma, True)

        queue = EstimQueue(psf, batchSize=1024)
        
        calib = create_calib_obj(gain,offset,imgshape,ctx)

        run_spot_detection_queue(imgshape, spotDetector, calib, queue, 
                           tiff.tiff_read_file(fn, startframe, maxframes, progress_cb), sumframes)

        queue.WaitUntilDone()
        
        if progress_cb is not None:
            if not progress_cb(None,None): return None,None
        
        r = queue.GetResults()
        r.SortByID() # sort by frame numbers
        
        print(f"Filtering {len(r.estim)} spots...")
        minX = 2.1
        minY = 2.1
        r.FilterXY(minX,minY,roisize-minX-1, roisize-minY-1)
        r.Filter(np.where(r.iterations<50)[0])
        
        nframes = np.max(r.ids)+1 if len(r.ids)>0 else 1
        print(f"Num spots: {len(r.estim)}. {len(r.estim) / nframes} spots/frame")
        
        if output_file is not None:
            r.SaveHDF5(output_file, imgshape)
            
        
        return r,imgshape
    
    
