try:
    from .import gen_lookup
except:
    from .import gen_lookup_python as gen_lookup
    print("using python integration for line aware stat (install boost and gsl C++ libraries for faster runtime -- see documentation)")
import numpy as np
import sys
import json
import pickle as pickle
import argparse
import os

def save_lookup_amp(p1,p2,ratio,outdir, pow_range = (1,400,500), frac_range = (0.1,1,10)):
    """
    save the lookup table for two detectors with the line aware statistic with consitistent amplitude
    (uses json to save file)
    Args
    --------------
    p1 : float
        width of prior of signal model
    p2 : float
        width of prior of line model
    ratio : float
        ratio of line to noise models
    outdir: string
        directory to save lookup table file
    pow_range: tuple
        ranges for the spectrogram power (lower, upper, number), default (1,400,500)
    frac_range: tuple
        ranges for the ratios of sensitivity and duty cycle (lower, upper, number), default (0.1,1,10)
    """
    minimum,maximum,num = pow_range
    minn,maxn,numn = frac_range
    #ch_arr_app = gen_data.gen_lookup_noise(np.linspace(minimum,maximum,num),np.linspace(minimum,maximum,num),np.linspace(minn,maxn,numn),int_type="chi2",approx=False,pvs=p1,pvl=p2,beta=ratio)
    filename = outdir+"/ch2_signoiseline_{}_{}_{}.json".format(p1,p2,ratio)
    if os.path.isfile(filename):
        print(("File {} exists".format(filename)))
    else:
        ch_arr_app = gen_lookup.gen_lookup_line_aware_amp(np.linspace(minimum,maximum,num),np.linspace(minimum,maximum,num),np.log(np.linspace(minn,maxn,numn)),pvs=p1,pvl=p2,ratio=ratio)
        with open(filename,'w+') as f:
            save_data = [[minimum,maximum,num,minn,maxn,numn],np.log(ch_arr_app[0]).tolist()]

            json.dump(save_data,f)

def save_lookup_2det(p1,p2,ratio,outdir,log=True, pow_range = (1,400,500)):
    """
    save the lookup table for two detectors with the line aware statistic
    
    Args
    --------------
    p1 : float
        width of prior of signal model
    p2 : float
        width of prior of line model
    ratio : float
        ratio of line to noise models
    outdir: string
        directory to save lookup table file
    pow_range: tuple
        ranges for the spectrogram power (lower, upper, number), default (1,400,500)

    """
    minimum,maximum,num = pow_range

    if os.path.isfile(outdir+"/signoiseline_2det_{}_{}_{}.txt".format(p1,p2,ratio)):
        pass
    else:
        ch_arr_app = gen_lookup.LineAwareStatistic([np.linspace(minimum,maximum,num),np.linspace(minimum,maximum,num)],pvs=p1,pvl=p2,ratio=ratio)
        with open(outdir+"/signoiseline_2det_{}_{}_{}.txt".format(p1,p2,ratio),'wb') as f:
            header = "{} {} {}".format(minimum,maximum,num)
            if log:
                np.savetxt(f,np.log(ch_arr_app.signoiseline),header = header)
            elif not log:
                np.savetxt(f,ch_arr_app.signoiseline,header = header)

def save_lookup_1det(p1,p2,ratio,outdir,pow_range = (1,400,500)):
    """
    save the lookup table for two detectors with the line aware statistic
    
    Args
    --------------
    p1 : float
        width of prior of signal model
    p2 : float
        width of prior of line model
    ratio : float
        ratio of line to noise models
    outdir: string
        directory to save lookup table file
    pow_range: tuple
        ranges for the spectrogram power (lower, upper, number), default (1,400,500)

    """

    minimum,maximum,num = pow_range

    if os.path.isfile(outdir+"/signoiseline_1det_{}_{}_{}.txt".format(p1,p2,ratio)):
        pass
    else:
        ch_arr_app = gen_lookup.LineAwareStatistic(np.linspace(minimum,maximum,num),pvs=p1,pvl=p2,ratio=ratio)
        with open(outdir+"/signoiseline_1det_{}_{}_{}.txt".format(p1,p2,ratio),'wb') as f:
            header = "{} {} {}".format(minimum,maximum,num)
            np.savetxt(f,np.log(ch_arr_app.signoiseline),header = header)



def resave_files(p1,p2,ratio,output):
    """
    resave text files into pickle format
    """
    if os.path.isfile(output+"/txt/ch2_signoiseline_{}_{}_{}.txt".format(p1,p2,ratio)):
        with open(output+"/txt/ch2_signoiseline_{}_{}_{}.txt".format(p1,p2,ratio),'rb') as f:
            save_array = pickle.load(f)
        if os.path.isdir(output+"/pkl/"):
            pass
        else:
            os.mkdir(output+"/pkl/")
        with open(output+"/pkl/ch2_signoiseline_{}_{}_{}.pkl".format(p1,p2,ratio),'wb') as f:
            pickle.dump(save_array,f,protocol=pickle.HIGHEST_PROTOCOL)

