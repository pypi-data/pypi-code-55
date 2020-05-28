import sys,shutil,os,glob,copy
from drizzlepac import astrodrizzle
from astropy.io import fits
class GrismDRZ:
    def __init__(self,pairs,group,params,run,outpath,meta):
        if group:
            self.group = group
        else:
            self.group = self.make_group(pairs)
        if params:
            self.params = params
        else:
            self.params = self.make_params(meta)
        if run:
            if not outpath:
                self.outpath = os.getcwd() + '/drz/'
            if len(glob.glob(self.outpath))==0:
                os.mkdir(self.outpath)
            self.meta = self.run(meta)
    #####
    #####
    #####
    def run(self,meta):
        outmeta = {}
        for i in self.group:
            inputlist = []
            for j in i:
                source = meta[j]['FILE']
                destination = self.outpath + source.split('/')[-1]
                shutil.copyfile(source,destination)                 
                inputlist.append(destination)
            for j,jj in enumerate(i):
                x = fits.open(meta[jj]['FILE'])
                ext = meta[jj]['EXT']
                xdata = meta[jj]['CLEAN']
                x[ext].data = copy.deepcopy(xdata)
                x.writeto(inputlist[j],overwrite=True)
                x.close()
            self.params['final_refimage'] = inputlist[0]
            self.params['output'] = inputlist[0].split('flt')[0]
            astrodrizzle.AstroDrizzle(input=inputlist, **self.params)
            for j,jj in enumerate(i):
                source = inputlist[j]
                os.remove(source)
            outfile = self.params['output'] + '_drz.fits'
            outmeta[i[0]] = copy.deepcopy(meta[i[0]])
            outmeta[i[0]]['FILE'] = copy.deepcopy(outfile)
            outmeta[i[0]]['CLEAN'] = copy.deepcopy(fits.open(outfile)[outmeta[i[0]]['EXT']].data)
        return outmeta                      
    #####
    #####
    #####
    def make_params(self,meta):
        PARAMS = {'driz_sep_bits': 11775,
                  'combine_type': 'median',
                  'blot': 'Yes',
                  'blot_addsky': 'No',
                  'final_bits': 11775,
                  'final_wcs': 'Yes',
                  'build': 'Yes',
                  'clean': 'Yes'
                 }
        return PARAMS
    #####
    #####
    #####
    def make_group(self,pairs):
        gr = []
        for i in pairs:
            gr.append(pairs[i])
        return gr
        