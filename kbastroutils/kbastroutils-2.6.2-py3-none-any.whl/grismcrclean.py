import sys,shutil,os,glob
from drizzlepac import astrodrizzle
class GrismCRClean:
    def __init__(self,identifier,pairs,group,params,run,outpath,meta):
        if group:
            self.group = group
        else:
            self.group = self.make_group(pairs)
        if params:
            self.params = params
        else:
            self.params = self.make_params(meta,identifier)
        if run:
            if not outpath:
                self.outpath = os.getcwd() + '/crclean/'
            if len(glob.glob(self.outpath))==0:
                os.mkdir(self.outpath)
            self.meta = self.run(meta)
    #####
    #####
    #####
    def run(self,meta):
        out = {}
        for i in self.group:
            inputlist = []
            for j in i:
                source = meta[j]['FILE']
                destination = self.outpath + source.split('/')[-1]
                shutil.copyfile(source,destination)                 
                inputlist.append(destination)
            astrodrizzle.AstroDrizzle(input=inputlist, **self.params)
            for j,jj in enumerate(i):
                source = inputlist[j]
                os.remove(source)
                new = source.split('flt')[0] + 'crclean.fits'
                out[jj] = new
        return out
    #####
    #####
    #####
    def make_params(self,meta,identifier):
        if identifier==('HST','WFC3','IR'):
            PARAMS = {'driz_sep_bits': 11775,
                      'combine_type': 'median',
                      'driz_cr_corr': 'Yes',
                      'build': 'Yes',
                      'clean': 'Yes'
                     }
        elif identifier==('HST','ACS','WFC'):
            PARAMS = {'driz_sep_bits': 16383,
                      'combine_type': 'median',
                      'driz_cr_corr': 'Yes',
                      'build': 'Yes',
                      'clean': 'Yes'
                     }
        else:
            print('Line57')
            pass
        return PARAMS
    #####
    #####
    #####
    def make_group(self,pairs):
        gr = []
        for i in pairs:
            gr.append(pairs[i])
        return gr
        