import os, sys,re, glob
import xlsxwriter as xw
import pandas as pd
import shutil
import csv

import logging


log = logging.getLogger(__name__)

def renamer(pathname, pattern, replacement):
	basename = os.path.basename(pathname)
	newFile = re.sub(pattern, replacement, basename)
	newPath = os.path.join(os.path.dirname(pathname), newFile)
	if newFile != basename and not os.path.exists(newPath):
		print("Renamin File:\t" + newFile)
		os.rename(
			pathname, 
			os.path.join(os.path.dirname(pathname), newFile))
		return newPath
	else:
		return 0
				
def copy(src_file,  dst_dir):
	
	fname = os.path.basename(src_file).split(".")[0]
	inDir = glob.glob(dst_dir + fname +"*")

	if not inDir:
		print("Copying File:\t" + os.path.basename(src_file))
		shutil.copy(src_file,dst_dir)
		return os.path.join(dst_dir,os.path.basename(src_file))
	else:
		return 0


def rename_fcs_files(origin_dir, destination_dir, pattern, replacement):

    files = glob.glob(origin_dir + "*.xls")
    for file in files:
        # copy file if not already copied
        cFile = copy(file,destination_dir)
        if cFile:
            # rename file if not already renamed
            rFile = renamer(cFile, pattern ,replacement)

            # load data to be processed
            data = pd.read_csv(rFile,delimiter ='\t', encoding="UTF-16")
            #data = pd.read_csv(rFile,delimiter ='\t')
            for col in data:
                for indx,item in enumerate(data[col]):
                    if isinstance(item, str):
                        data[col][indx] = float(data[col][indx].replace(',',''))
            # re-write data to file in proper format
            data.to_csv(rFile, index=False)
