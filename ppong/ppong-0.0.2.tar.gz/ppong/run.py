from rohan.dandage.io_dict import read_dict,to_dict
from os.path import exists,basename,dirname
from glob import glob

def analyser(input_audio_path,output_directory,test=False,force=False,cores=4):
    """
    runs the analysis.
    
    :param path: path to audio file/s (ext:.m4a) e.g. 'drive/*.m4a'
    """
    packagen=basename(dirname(__file__))
    
    cfgp=f"{basename(output_directory).replace('/','')}.json"
    cfg={}
    cfg['date2pathm4ap']={basename(p).replace('.m4a',''):p for p in sorted(glob(input_audio_path))}
    to_dict(cfg,cfgp)
    
    from rohan.dandage.io_fun import run_package
    cfg=run_package(cfgp,packagen=packagen,test=test,force=force,cores=cores)
    

## begin
import argh
import sys
parser = argh.ArghParser()
parser.add_commands([analyser,])

if __name__ == '__main__':
    parser.dispatch()
