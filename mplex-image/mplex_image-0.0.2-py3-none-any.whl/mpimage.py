####
# title: mpimage.py
#
# language: Python3.6
# date: 2019-05-00
# license: GPL>=v3
# author: Jenny
#
# description:
#   python3 library to display, normalize and crop multiplex images
####

#libraries
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import skimage
import pandas as pd
import copy
import javabridge #meta
import bioformats #meta
import re
import shutil
from itertools import chain

#functions

#add original images to dataframe

def parse_img(s_end =".tif",s_start='',s_sep1='_',s_sep2='.',s_exclude='Gandalf',ls_column=['rounds','color','imagetype','scene'],b_test=True):
    '''
    required columns: ['rounds','color','imagetype','scene']
    meta names names=['rounds','color','minimum', 'maximum', 'exposure', 'refexp','location'],#'marker',
    return = df_img
    '''
    ls_file = []
    for file in os.listdir():
        #find all filenames ending in s_end
        if file.endswith(s_end):
            if file.find(s_start)==0:
                if file.find(s_exclude)==-1:
                     ls_file = ls_file + [file]
        
    print(f'test {int(1.1)}')
    #make a list of list of file name items separated by s_sep
    llls_split = []
    for items in [item.split(s_sep1)for item in ls_file]:
        llls_split.append([item.split(s_sep2) for item in items])

    lls_final = []
    for lls_split in llls_split:
        lls_final.append(list(chain.from_iterable(lls_split)))

    #make a blank dataframe with the index being the filename 
    df_img = pd.DataFrame(index=ls_file, columns=ls_column)
    if b_test:
        print(lls_final[0])
        print(f'Length = {len(lls_final[0])}')
    #add a column for each part of the name
    else:
        for fidx, ls_final in enumerate(lls_final):
            for idx, s_name in enumerate(ls_final):
                df_img.loc[ls_file[fidx],ls_column[idx]] = s_name
        print('Mean number of items in file name')
        print(np.asarray([(len(item)) for item in lls_final]).mean())
        if (np.asarray([(len(item)) for item in lls_final]).mean()).is_integer()==False:
            print([(len(item)) for item in lls_final])
            i_right = np.asarray([(len(item)) for item in lls_final]).max()
            for fidx, ls_final in enumerate(lls_final):
                if len(ls_final) < i_right:
                    print(f' inconsitent name: {ls_file[fidx]}')
    return(df_img)

def parse_org(s_end = "ORG.tif",s_start='R',type='reg'):
    """
    This function will parse images following koei's naming convention
    Example: Registered-R1_PCNA.CD8.PD1.CK19_Her2B-K157-Scene-002_c1_ORG.tif
    The output is a dataframe with image filename in index
    And rounds, color, imagetype, scene (/tissue), and marker in the columns
    type= 'reg' or 'raw'
    """

    ls_file = []
    for file in os.listdir():
    #find all filenames ending in 'ORG.tif'
        if file.endswith(s_end):
            if file.find(s_start)==0:
                ls_file = ls_file + [file]
    lls_name = [item.split('_') for item in ls_file]
    df_img = pd.DataFrame(index=ls_file)

    if type == 'raw':
        lls_scene = [item.split('-Scene-') for item in ls_file]
    elif type== 'noscenes':
        ls_scene = ['Scene-001'] * len(ls_file)
    if type == 'raw':
        df_img['rounds'] = [item[0] for item in lls_name]
    elif type== 'noscenes':
        df_img['rounds'] = [item[0] for item in lls_name]
    else:
        df_img['rounds'] = [item[0].split('Registered-')[1] for item in lls_name]
    df_img['color'] = [item[-2] for item in lls_name]
    df_img['imagetype'] = [item[-1].split('.tif')[0] for item in lls_name]
    if type == 'raw':
        df_img['slide'] = [item[2] for item in lls_name]
        df_img['scene'] = [item[1].split('_')[0] for item in lls_scene]
    elif type == 'noscenes':
        df_img['scene'] = ls_scene
    else:
        df_img['scene'] = [item[2] for item in lls_name]

    #parse file name for biomarker
    for s_index in df_img.index:
        #print(s_index)
        s_color = df_img.loc[s_index,'color']
        if s_color == 'c1':
            s_marker = 'DAPI'
        elif s_color == 'c2':
            s_marker = s_index.split('_')[1].split('.')[0]
        elif s_color == 'c3':
            s_marker = s_index.split('_')[1].split('.')[1]
        elif s_color == 'c4':
            s_marker = s_index.split('_')[1].split('.')[2]
        elif s_color == 'c5':
            s_marker = s_index.split('_')[1].split('.')[3]
        else: print('Error')
        df_img.loc[s_index,'marker'] = s_marker

    return(df_img) #,lls_name)

def filename_dataframe(s_end = ".czi",s_start='R',s_split='_'):
    '''
    quick and dirty way to select files for dataframe. 
    s_end = string at end of file names
    s_start = string at beginning of filenames
    s_split = character/string in all file names
    '''
    ls_file = []
    for file in os.listdir():
    #find all filenames ending in 'ORG.tif'
        if file.endswith(s_end):
            if file.find(s_start)==0:
                ls_file = ls_file + [file]
    lls_name = [item.split(s_split) for item in ls_file]
    df_img = pd.DataFrame(index=ls_file)
    df_img['data'] = [item[0] for item in lls_name]
    return(df_img)

def get_exposure(s_image, s_find="Information\|Image\|Channel\|ExposureTime\<\/Key\>\<Value\>"):

    s_meta = bioformats.get_omexml_metadata(path=s_image)
    o = bioformats.OMEXML(s_meta)
    print(o.image().Name)
    print(o.image().AcquisitionDate)

    li_start = [m.start() for m in re.finditer(s_find, s_meta)]
    if len(li_start)!=1:
        print('Error: found wrong number of exposure times')

    ls_exposure = []
    for i_start in li_start:
        ls_exposure.append(s_meta[i_start:i_start+200])
    s_exposure =  ls_exposure[0].strip(s_find)
    s_exposure = s_exposure[1:s_exposure.find(']')]
    ls_exposure = s_exposure.split(',')
    li_exposure = [int(item)/1000000 for item in ls_exposure]
    return(li_exposure,s_meta)

def get_exposure_sample(s_sample,df_img):
    """
    return a dataframe with all exposure times for a sample (slide)
    """
    #make dataframe of exposure time metadata
    df_exposure = pd.DataFrame()
    ls_image = os.listdir()
    df_sample = df_img[df_img.index.str.contains(s_sample)]
    for s_image in df_sample.index:
                        print(s_image)
                        li_exposure, s_meta = get_exposure(s_image)
                        se_times = pd.Series(li_exposure,name=s_image)
                        df_exposure = df_exposure.append(se_times)
    return(df_exposure)

def get_meta(s_image, s_find = 'Scene\|CenterPosition\<\/Key\>\<Value\>\['):
    """czi scene metadata
    s_image = filename
    s_find = string to find in the omexml metadata
    returns: 
    ls_exposure = list of 200 character strings following s_find in metadata
    s_meta = the whole metadata string
    """
    s_meta = bioformats.get_omexml_metadata(path=s_image)
    o = bioformats.OMEXML(s_meta)
    #print(o.image().Name)
    #print(o.image().AcquisitionDate)

    li_start = [m.start() for m in re.finditer(s_find, s_meta)]
    if len(li_start)!=1:
        print('Error: found wrong number of exposure times')

    ls_exposure = []
    for i_start in li_start:
        ls_exposure.append(s_meta[i_start:i_start+200])
    s_exposure =  ls_exposure[0].strip(s_find)
    s_exposure = s_exposure[0:s_exposure.find(']')]
    ls_exposure = s_exposure.split(',')
    #li_exposure = [int(item)/1000000 for item in ls_exposure]
    return(ls_exposure,s_meta)

def add_exposure(df_img,df_t, type='roundcycles'):
    """
    df_img = dataframe of images with columns [ 'color', 'exposure', 'marker','sub_image','sub_exposure']
            and index with image names
    df_t = metadata with dataframe with ['marker','exposure']
    """
    if type == 'roundscycles':
        for s_index in df_img.index:
            s_marker = df_img.loc[s_index,'marker']
            #look up exposure time for marker in metadata
            df_t_image = df_t[(df_t.marker==s_marker)]
            if len(df_t_image) > 0:
                i_exposure = df_t_image.iloc[0].loc['exposure']
                df_img.loc[s_index,'exposure'] = i_exposure
            else:
                print(f'{s_marker} has no recorded exposure time')
    elif type == 'czi':
    #add exposure
        df_t['rounds'] = [item.split('_')[0] for item in df_t.index]
        df_t['tissue'] = [item.split('_')[2] for item in df_t.index]
        for s_index in df_img.index:
            s_tissue = df_img.loc[s_index,'scene'].split('-Scene')[0]
            s_color = str(int(df_img.loc[s_index,'color'].split('c')[1])-1)
            s_round = df_img.loc[s_index,'rounds']
            df_img.loc[s_index,'exposure'] = df_t[(df_t.tissue==s_tissue) & (df_t.rounds==s_round)].loc[:,s_color][0]

    return(df_img)

def subtract_images(df_img,d_channel={'c2':'L488','c3':'L555','c4':'L647','c5':'L750'},ls_exclude=[],b_8bit=True):#b_mkdir=True,
    """
    This code loads 16 bit grayscale tiffs, performs AF subtraction of channels/rounds defined by the user, and outputs 8 bit AF subtracted tiffs for visualization.
    The data required is:
    1. The RoundsCyclesTable with real exposure times
    2. dataframe of images to process (df_img); can be created with any custom parsing function
        df_img = dataframe of images with columns [ 'color', 'exposure', 'marker']
            and index with image names
        d_channel = dictionary mapping color to marker to subtract
        ls_exclude = lost of markers not needing subtraction
    """
    #if b_mkdir:
    #    os.mkdir('AFSubtracted')
    #generate dataframe of subtraction markers 
    es_subtract = set()
    for s_key, s_value in d_channel.items():
        es_subtract.add(s_value)
        print(f'Subtracting {s_value} for all {s_key}')
    
    df_subtract = pd.DataFrame()
    for s_subtract in sorted(es_subtract):
        se_subtract = df_img[df_img.marker==s_subtract]
        df_subtract = df_subtract.append(se_subtract)
    print(f'The background images {df_subtract.index.tolist}')
    print(f'The background markers {df_subtract.marker.tolist}')
    
    #generate dataframe of how subtraction is set up
    #set of markers minus the subtraction markers 
    es_markers = set(df_img.marker) - es_subtract
    #dataframe of markers
    df_markers = df_img[df_img.loc[:,'marker'].isin(sorted(es_markers))]
    #minus dapi (color 1 or DAPI)
    #df_markers = df_markers[df_markers.loc[:,'color']!='c1']
    #df_markers = df_markers[~df_markers.loc[:,'marker'].str.contains('DAPI')]
    df_copy = df_img[df_img.marker.isin(ls_exclude)]
    df_markers = df_markers[~df_markers.marker.isin(ls_exclude)]
    
    for s_file in df_copy.index.tolist():
        print(s_file)
        print(f'copied to ./AFSubtracted/{s_file}')
        shutil.copyfile(s_file,f'./AFSubtracted/{s_file}')
    #ls_scene = sorted(set(df_img.scene))
    #add columns with mapping of proper subtracted image to dataframe
    
    for s_index in df_markers.index.tolist():
        print('add colums')
        print(s_index)
        s_scene = s_index.split('_')[2]
        s_color = df_markers.loc[s_index,'color']
        if len(df_subtract[(df_subtract.color==s_color) & (df_subtract.scene==s_scene)])==0:
            print(f'missing {s_color} in {s_scene}')
        else:
            df_markers.loc[s_index,'sub_image'] = df_subtract[(df_subtract.color==s_color) & (df_subtract.scene==s_scene)].index[0]
            df_markers.loc[s_index,'sub_exposure'] = df_subtract[(df_subtract.color==s_color) & (df_subtract.scene==s_scene)].exposure[0]
    
    #loop to subtract
    for s_index in df_markers.index.tolist():
        print(f'Processing {s_index}')
        s_image = s_index
        s_color = '_' + df_markers.loc[s_index,'color'] + '_'
        s_background = df_markers.loc[s_index,'sub_image']
        print(f'From {s_image} subtracting \n {s_background}')
        a_img = skimage.io.imread(s_image)
        a_AF = skimage.io.imread(s_background)
        #divide each image by exposure time
        #subtract 1 ms AF from 1 ms signal
        #multiply by original image exposure time
        a_sub = (a_img/df_markers.loc[s_index,'exposure'] - a_AF/df_markers.loc[s_index,'sub_exposure'])*df_markers.loc[s_index,'exposure']
        a_zero = (a_sub.clip(min=0)).astype(int) #max=a_sub.max() #took out max parameter from np.clip, but it was fine in
        if b_8bit:
            #a_16bit = skimage.img_as_ubyte(a_zero)
            #a_zero = a_sub.clip(min=0,max=a_sub.max())
            a_bit = (a_zero/256).astype(np.uint8)
        else:
            a_bit = skimage.img_as_uint(a_zero)
        s_fname = f'./AFSubtracted/{s_index.split(s_color)[0]}_Sub{df_subtract.loc[df_markers.loc[s_index,"sub_image"],"marker"]}{s_color}{s_index.split(s_color)[1]}'
        skimage.io.imsave(s_fname,a_bit)
    
    return(df_markers,df_copy)#df_markers,es_subtract

def array_img(df_img,s_xlabel='color',ls_ylabel=['rounds','exposure'],s_title='marker',tu_array=(2,4),tu_fig=(10,20)):
    """
    create a grid of images
    df_img = dataframe of images with columns having image attributes
        and index with image names
    s_xlabel = coumns of grid
    ls_ylabel = y label 
    s_title= title

    """
     
    fig, ax = plt.subplots(tu_array[0],tu_array[1],figsize=tu_fig)
    ax = ax.ravel()
    for ax_num, s_index in enumerate(df_img.index):
        s_row_label = f'{df_img.loc[s_index,ls_ylabel[0]]}\n {df_img.loc[s_index,ls_ylabel[1]]}'
        s_col_label = df_img.loc[s_index,s_xlabel]
        a_image=skimage.io.imread(s_index)
        s_label_img = df_img.loc[s_index,s_title]
        a_rescale = skimage.exposure.rescale_intensity(a_image,in_range=(0,1.5*np.quantile(a_image,0.98)))
        ax[ax_num].imshow(a_rescale,cmap='gray')
        ax[ax_num].set_title(s_label_img)
        ax[ax_num].set_ylabel(s_row_label)
        ax[ax_num].set_xlabel(f'{s_col_label}\n 0 - {int(1.5*np.quantile(a_image,0.98))}')
    plt.tight_layout()
    return(fig)

def array_roi(df_img,s_column='color',s_row='rounds',s_label='marker',tu_crop=(0,0,100,100),tu_array=(2,4),tu_fig=(10,20), b_min_label=True,tu_rescale=(0,0)):
    """
    create a grid of images
    df_img = dataframe of images with columns having image attributes
        and index with image names
    s_column = coumns of grid
    s_row = rows of grid
    s_label= attribute to label axes
    tu_crop = (upper left corner x,  y , xlength, yheight)
    tu_dim = a tumple of x and y dimensinons of crop
    """
     
    fig, ax = plt.subplots(tu_array[0],tu_array[1],figsize=tu_fig,sharex=True, sharey=True) 
    if b_min_label:
        fig, ax = plt.subplots(tu_array[0],tu_array[1],figsize=tu_fig, sharey=True) 
    ax = ax.ravel()
    for ax_num, s_index in enumerate(df_img.index):
        s_row_label = df_img.loc[s_index,s_row]
        s_col_label = df_img.loc[s_index,s_column]
        s_label_img = df_img.loc[s_index,s_label]
        #load image, copr, rescale
        a_image=skimage.io.imread(s_index)
        a_crop = a_image[(tu_crop[1]):(tu_crop[1]+tu_crop[3]),(tu_crop[0]):(tu_crop[0]+tu_crop[2])]
        if tu_rescale==(0,0):
            a_rescale = skimage.exposure.rescale_intensity(a_crop,in_range=(0,np.quantile(a_image,0.98)+np.quantile(a_image,0.98)/2))
            tu_max = (0,np.quantile(a_image,0.98)+np.quantile(a_image,0.98)/2)
            ax[ax_num].imshow(a_rescale,cmap='gray')
        else:
            print(f'original {a_crop.min()},{a_crop.max()}')
            print(f'rescale to {tu_rescale}')
            a_rescale = skimage.exposure.rescale_intensity(a_crop,in_range=tu_rescale,out_range=tu_rescale)
            tu_max=tu_rescale
            ax[ax_num].imshow(a_rescale,cmap='gray',vmin=0, vmax=tu_max[1])
        ax[ax_num].set_title(s_label_img)
        ax[ax_num].set_ylabel(s_row_label)
        ax[ax_num].set_xlabel(s_col_label)
        if b_min_label:
            ax[ax_num].set_xticklabels('')
            ax[ax_num].set_xlabel(f'{tu_max[0]} - {int(tu_max[1])}') #min/max = 
    plt.tight_layout()
    return(fig)

def array_roi_if(df_img,df_dapi,s_label='rounds',s_title='Title',tu_crop=(0,0,100,100),tu_array=(2,4),tu_fig=(10,20),tu_rescale=(0,0),i_expnorm=0,i_micron_per_pixel=.325):
    """
    create a grid of images
    df_img = dataframe of images with columns having image attributes
        and index with image names
    df_dapi = like df_img, but with the matching dapi images
    s_label= attribute to label axes
    s_title = x axis title
    tu_crop = (upper left corner x,  y , xlength, yheight)
    tu_array = subplot array dimensions
    tu_fig = size of figue
    tu_rescele= 
    i_expnorm = 
    """
    cmap = mpl.colors.LinearSegmentedColormap.from_list('cmap', [(0,0,0),(0,1,0)], N=256, gamma=1.0)
    fig, ax = plt.subplots(tu_array[0],tu_array[1],figsize=tu_fig,sharey=True, squeeze=False) #
    ax = ax.ravel()
    for ax_num, s_index in enumerate(df_img.index):
        s_col_label = df_img.loc[s_index,s_label]
        #load image, copr, rescale
        a_image=skimage.io.imread(s_index)
        a_dapi = skimage.io.imread((df_dapi).index[0])# & (df_dapi.rounds=='R1')
        a_crop = a_image[(tu_crop[1]):(tu_crop[1]+tu_crop[3]),(tu_crop[0]):(tu_crop[0]+tu_crop[2])]
        a_crop_dapi = a_dapi[(tu_crop[1]):(tu_crop[1]+tu_crop[3]),(tu_crop[0]):(tu_crop[0]+tu_crop[2])]
        #a_crop_dapi = (a_crop_dapi/255).astype('int')
        if i_expnorm > 0:
            a_crop = a_crop/df_img.loc[s_index,'exposure']*i_expnorm
        if tu_rescale==(0,0):
            a_rescale = skimage.exposure.rescale_intensity(a_crop,in_range=(np.quantile(a_crop,0.03),1.5*np.quantile(a_crop,0.998)),out_range=(0, 255))
            tu_max = (np.quantile(a_crop,0.03),1.5*np.quantile(a_crop,0.998))
        else:
            print(f'original {a_crop.min()},{a_crop.max()}')
            print(f'rescale to {tu_rescale}')
            a_rescale = skimage.exposure.rescale_intensity(a_crop,in_range = tu_rescale,out_range=(0,255))
            tu_max=tu_rescale
        a_rescale_dapi = skimage.exposure.rescale_intensity(a_crop_dapi,in_range = (np.quantile(a_crop_dapi,0.03),2*np.quantile(a_crop_dapi,0.99)),out_range=(0,255)) 
        a_rescale_dapi = a_rescale_dapi.astype(np.uint8)
        a_rescale = a_rescale.astype(np.uint8)
        #2 color png
        zdh = np.dstack((np.zeros_like(a_rescale), a_rescale, a_rescale_dapi))
        ax[ax_num].imshow(zdh)
        ax[ax_num].set_title('')
        ax[ax_num].set_ylabel('')
        ax[ax_num].set_xlabel(s_col_label,fontsize = 'x-large')
        if tu_rescale == (0,0):
            if len(ax)>1:
                ax[ax_num].set_xlabel(f'{s_col_label} ({int(np.quantile(a_crop,0.03))} - {int(1.5*np.quantile(a_crop,0.998))})')
        ax[ax_num].set_xticklabels('')
    #pixel to micron (apply after ax is returned)
    #ax[0].set_yticklabels([str(int(re.sub(u"\u2212", "-", item.get_text()))*i_micron_per_pixel) for item in ax[0].get_yticklabels(minor=False)])
    plt.suptitle(s_title,y=0.93,size = 'xx-large',weight='bold')
    plt.subplots_adjust(wspace=.05, hspace=.05)
    # Now adding the colorbar
    norm = mpl.colors.Normalize(vmin=tu_max[0],vmax=tu_max[1])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    if len(ax) == 1:
        cbaxes = fig.add_axes([.88, 0.125, 0.02, 0.75]) #[left, bottom, width, height]
        plt.colorbar(sm, cax = cbaxes)
        plt.figtext(0.47,0.03,s_label.replace('_',' '),fontsize = 'x-large', weight='bold')
    elif tu_rescale != (0,0):
        cbaxes = fig.add_axes([.92, 0.175, 0.02, 0.64]) #[left, bottom, width, height]
        plt.colorbar(sm, cax = cbaxes)
        plt.figtext(0.42,0.03,s_label.replace('_',' '),fontsize = 'x-large', weight='bold')
    else:
        print("Different ranges - can't use colorbar") 
        plt.figtext(0.43,0.03,s_label.replace('_',' '),fontsize = 'x-large', weight='bold')

    return(fig,ax) 

def multicolor_png(df_img,df_dapi,s_scene,d_overlay,d_crop,es_dim={'CD8','FoxP3','ER','AR'},es_bright={'Ki67','pHH3'},low_thresh=4000,high_thresh=0.999):
    '''
    create RGB image with Dapi plus four - 6 channels
    '''

    d_result = {}
    print(s_scene)
    tu_crop = d_crop[s_scene]
    df_slide = df_img[df_img.scene == s_scene]
    x=tu_crop[1]
    y=tu_crop[0]
    img_dapi = skimage.io.imread(df_dapi[df_dapi.scene==s_scene].path[0])
    a_crop = img_dapi[x:x+800,y:y+800]
    a_rescale_dapi = skimage.exposure.rescale_intensity(a_crop,in_range=(np.quantile(img_dapi,0.2),1.5*np.quantile(img_dapi,high_thresh)),out_range=(0, 255))
    if 1.5*np.quantile(img_dapi,high_thresh) < low_thresh:
                a_rescale_dapi = skimage.exposure.rescale_intensity(a_crop,in_range=(low_thresh/2,low_thresh),out_range=(0, 255))
    elif len(es_dim.intersection(set(['DAPI'])))==1:
                new_thresh = float(str(high_thresh)[:-2])
                a_rescale_dapi = skimage.exposure.rescale_intensity(a_crop,in_range=(np.quantile(img_dapi,0.2),1.5*np.quantile(img_dapi,new_thresh)),out_range=(0, 255))
    elif len(es_bright.intersection(set(['DAPI'])))==1:
                a_rescale_dapi = skimage.exposure.rescale_intensity(a_crop,in_range=(np.quantile(img_dapi,0.2),1.5*np.quantile(img_dapi,float(str(high_thresh) + '99'))),out_range=(0, 255))

    #RGB
    for s_type, ls_marker in d_overlay.items():
        print(s_type)
        zdh = np.dstack((np.zeros_like(a_rescale_dapi), np.zeros_like(a_rescale_dapi),a_rescale_dapi))
        for idx, s_marker in enumerate(ls_marker):
            print(s_marker)
            s_index = df_slide[df_slide.marker == s_marker].index[0]
            img = skimage.io.imread(df_slide.loc[s_index,'path'])
            a_crop = img[x:x+800,y:y+800]
            in_range = (np.quantile(a_crop,0.2),1.5*np.quantile(a_crop,high_thresh))
            a_rescale = skimage.exposure.rescale_intensity(a_crop,in_range=in_range,out_range=(0, 255))
            if 1.5*np.quantile(a_crop,high_thresh) < low_thresh:
                print('low thresh')
                in_range=(low_thresh/2,low_thresh)
                a_rescale = skimage.exposure.rescale_intensity(a_crop,in_range=in_range,out_range=(0, 255))
            elif len(es_dim.intersection(set([s_marker])))==1:
                print('dim')
                new_thresh = float(str(high_thresh)[:-2])
                in_range=(np.quantile(a_crop,0.2),1.5*np.quantile(a_crop,new_thresh))
                a_rescale = skimage.exposure.rescale_intensity(a_crop,in_range=in_range,out_range=(0, 255))
            elif len(es_bright.intersection(set([s_marker])))==1:
                print('bright')
                in_range=(np.quantile(a_crop,0.2),1.5*np.quantile(a_crop,float(str(high_thresh) + '99')))
                a_rescale = skimage.exposure.rescale_intensity(a_crop,in_range=in_range,out_range=(0, 255))

            print(f'low {int(in_range[0])} high {int(in_range[1])}')
            if idx == 0:
                zdh = zdh + np.dstack((np.zeros_like(a_rescale), a_rescale,np.zeros_like(a_rescale)))

            elif idx == 1:
                zdh = zdh + np.dstack((a_rescale, a_rescale,np.zeros_like(a_rescale)))

            elif idx == 2:
                zdh = zdh + np.dstack((a_rescale, np.zeros_like(a_rescale),np.zeros_like(a_rescale) ))

            elif idx == 3:
                zdh = zdh + np.dstack((np.zeros_like(a_rescale), a_rescale, a_rescale))
        print(zdh.min())
        zdh = zdh.clip(0,255)
        zdh = zdh.astype('uint8')
        print(zdh.max())
        d_result.update({s_type:(ls_marker,zdh)})
    return(d_result)

#### old
def multicolor_border_png(df_img,df_dapi,s_scene,d_overlay,d_crop,es_dim={'CD8','FoxP3','ER','AR'},es_bright={'Ki67','pHH3'},low_thresh=4000,high_thresh=0.999):
    '''
    create RGB image with Dapi plus four - 6 channels (not ld- but Napari works better)
    '''

    d_result = {}
    print(s_scene)
    tu_crop = d_crop[s_scene]
    df_slide = df_img[df_img.scene == s_scene]
    x=tu_crop[1]
    y=tu_crop[0]
    img_dapi = skimage.io.imread(df_dapi[df_dapi.scene==s_scene].path[0])
    a_crop = img_dapi[x:x+800,y:y+800]
    a_rescale_dapi = skimage.exposure.rescale_intensity(a_crop,in_range=(np.quantile(img_dapi,0.2),1.5*np.quantile(img_dapi,high_thresh)),out_range=(0, 255))
    if 1.5*np.quantile(img_dapi,high_thresh) < low_thresh:
                a_rescale_dapi = skimage.exposure.rescale_intensity(a_crop,in_range=(low_thresh/2,low_thresh),out_range=(0, 255))
    elif len(es_dim.intersection(set(['DAPI'])))==1:
                new_thresh = float(str(high_thresh)[:-2])
                a_rescale_dapi = skimage.exposure.rescale_intensity(a_crop,in_range=(np.quantile(img_dapi,0.2),1.5*np.quantile(img_dapi,new_thresh)),out_range=(0, 255))
    elif len(es_bright.intersection(set(['DAPI'])))==1:
                a_rescale_dapi = skimage.exposure.rescale_intensity(a_crop,in_range=(np.quantile(img_dapi,0.2),1.5*np.quantile(img_dapi,float(str(high_thresh) + '99'))),out_range=(0, 255))

    #RGB
    for s_type, ls_marker in d_overlay.items():
        print(s_type)
        zdh = np.dstack((np.zeros_like(a_rescale_dapi), np.zeros_like(a_rescale_dapi),a_rescale_dapi))
        for idx, s_marker in enumerate(ls_marker):
            print(s_marker)
            s_index = df_slide[df_slide.marker == s_marker].index[0]
            img = skimage.io.imread(df_slide.loc[s_index,'path'])
            in_range = (np.quantile(img,0.2),1.5*np.quantile(img,high_thresh))
            a_rescale = skimage.exposure.rescale_intensity(img,in_range=in_range,out_range=(0, 255))
            if 1.5*np.quantile(img,high_thresh) < low_thresh:
                print('low thresh')
                in_range=(low_thresh/2,low_thresh)
                a_rescale = skimage.exposure.rescale_intensity(img,in_range=in_range,out_range=(0, 255))
            elif len(es_dim.intersection(set([s_marker])))==1:
                print('di,m')
                new_thresh = float(str(high_thresh)[:-2])
                in_range=(np.quantile(img,0.2),1.5*np.quantile(img,new_thresh))
                a_rescale = skimage.exposure.rescale_intensity(img,in_range=in_range,out_range=(0, 255))
            elif len(es_bright.intersection(set([s_marker])))==1:
                print('bright')
                in_range=(np.quantile(img,0.2),1.5*np.quantile(img,float(str(high_thresh) + '99')))
                a_rescale = skimage.exposure.rescale_intensity(img,in_range=in_range,out_range=(0, 255))
            a_crop = a_rescale[x:x+800,y:y+800]
            print(f'low {int(in_range[0])} high {int(in_range[1])}')
            if idx == 0:
                zdh = zdh + np.dstack((np.zeros_like(a_crop), a_crop,np.zeros_like(a_crop)))

            elif idx == 1:
                zdh = zdh + np.dstack((a_crop, a_crop,np.zeros_like(a_crop)))

            elif idx == 2:
                zdh = zdh + np.dstack((a_crop, np.zeros_like(a_crop),np.zeros_like(a_crop) ))

            elif idx == 3:
                zdh = zdh + np.dstack((np.zeros_like(a_crop), a_crop, a_crop))
        print(zdh.min())
        zdh = zdh.clip(0,255)
        zdh = zdh.astype('uint8')
        print(zdh.max())
        d_result.update({s_type:(ls_marker,zdh)})
    return(d_result)

def view_rois(df_img,d_crop,tu_dim,s_column='color',ls_drop=['DAPI'],s_row='rounds',tu_fig=(10,20)):
    """
    create a grid of ROIs
    df_img = dataframe of images with columns ['rounds', 'color', 'imagetype', 'scene', 'marker']
        and index with image names
    d_crop = dictionary with {tissdue-scene-ID:upper left corner x y coordinates
    tu_dim = a tumple of x and y dimensinons of crop
    s_column = coumns of grid
    ls_drop = columns to exclude
    s_row = rows of grid

    """
    #drop rows of unwanted images
    df_img = df_img[~df_img.marker.isin(ls_drop)]
    i_rows = len(set(df_img.loc[:,s_row]))
    i_columns = len(set(df_img.loc[:,s_column]))
    
    #go scene by scene
    for s_scene,tu_crop in d_crop.items():
        df_img_scene = df_img[df_img.scene==s_scene] 
 
        fig, ax = plt.subplots(i_rows,i_columns,figsize=tu_fig,sharex=True, sharey=True) 
        ax = ax.ravel()
        ax_num = -1
        df_img_scene.sort_values(by=[s_row,s_column],inplace=True)
        for s_index in df_img_scene.index.tolist():
            s_row_label = df_img.loc[s_index,s_row]
            s_col_label = df_img.loc[s_index,s_column]
            #s_scene = df_img.loc[s_index,'scene']
            #if len(d_crop[s_scene]) > 0:
            ax_num = ax_num + 1
            tu_crop = d_crop[s_scene]
            a_image=skimage.io.imread(s_index)
            s_label_img = df_img.loc[s_index,'marker']
            #crop according to dictionary
            a_crop = a_image[(tu_crop[1]):(tu_crop[1]+tu_dim[1]),(tu_crop[0]):(tu_crop[0]+tu_dim[0])]
            a_rescale = skimage.exposure.rescale_intensity(a_crop,in_range=(0,np.quantile(a_crop,0.98)+np.quantile(a_crop,0.98)/2))
            ax[ax_num].imshow(a_rescale,cmap='gray')
            ax[ax_num].set_title(s_label_img)
            ax[ax_num].set_ylabel(s_row_label)
            ax[ax_num].set_xlabel(s_col_label)
        plt.tight_layout()
        #fig.savefig(f'ROIS_{s_scene}.png')
    return(fig)

def load_meta(s_sample, s_path='./',type='Location'):
    """
    load rounds cycles table
    make sure to specify location for use with downstream functions
    make sure to add rows for any biomarkers used for analysis or processing
    types = ['Location','Csv','LocationCsv', and other being space delimited txt file]
    """
    #tab or space delimited
    if type == 'Location':
        print(f'metadata_{s_sample}_RoundsCyclesTable_location.txt')
        df_t = pd.read_csv(
            f'metadata_{s_sample}_RoundsCyclesTable_location.txt',
            delim_whitespace=True,
            header=None,
            index_col=False,
            names=['marker', 'rounds','color','minimum', 'maximum', 'exposure', 'refexp','location'],
            )
        df_t = df_t.set_index(f'{s_sample}_' + df_t.index.astype(str))
        df_t.replace({'Nucleus':'Nuclei'},inplace=True)
        df_t['marker_loc'] = df_t.marker + '_' + df_t.location
        df_t.set_index(keys='marker_loc',inplace=True)
    elif type == 'Csv':
        print(f'metadata_{s_sample}_RoundsCyclesTable.csv')
        df_t = pd.read_csv(
            f'metadata_{s_sample}_RoundsCyclesTable.csv',
            header=0,
            index_col=False,
            names=['marker', 'rounds','color','minimum', 'maximum', 'exposure', 'refexp','location'],
            )
        df_t = df_t.set_index(f'{s_sample}_' + df_t.index.astype(str))
        df_t.replace({'Nucleus':'Nuclei'},inplace=True)
    #
    elif type == 'LocationCsv':
        print(f'metadata_{s_sample}_RoundsCyclesTable_location.csv')
        df_t = pd.read_csv(
            f'metadata_{s_sample}_RoundsCyclesTable_location.csv',
            header=0,
            index_col=False,
            names=['marker', 'rounds','color','minimum', 'maximum', 'exposure', 'refexp','location'],
            )
        df_t = df_t.set_index(f'{s_sample}_' + df_t.index.astype(str))
        df_t.replace({'Nucleus':'Nuclei'},inplace=True)
        df_t['marker_loc'] = df_t.marker + '_' + df_t.location
        df_t.set_index(keys='marker_loc',inplace=True)
    else:
        print(f'metadata_{s_sample}_RoundsCyclesTable.txt')
        df_t = pd.read_csv(
            f'metadata_{s_sample}_RoundsCyclesTable.txt',
            delim_whitespace=True,
            header=None,
            index_col=False,
            names=['marker', 'rounds','color','minimum', 'maximum', 'exposure', 'refexp','location'],
            )
        df_t = df_t.set_index(f'{s_sample}_' + df_t.index.astype(str))
        df_t.replace({'Nucleus':'Nuclei'},inplace=True)
    return(df_t)

def custom_overlays_org(d_combos,s_dapi='R11_DAPI'):
    """
    starts with QI tissue compatible 8 bit filename images
    output custon multi page tiffs according to dictionary, with s_dapi as channel 1 in each overlay
    """
    os.chdir('./8bit')
    ls_image = os.listdir()
    ls_slide = [] #list of slides/scenes
    ls_image_org = [] #list of 8 bit single channel images
    ls_round = [] #list of rounds

    for s_image in ls_image:
        if s_image.find('8bit.tif') > -1:
            #make a list of slides/scenes
            #also make list of rounds
            s_slide = s_image.split('_')[2]
            ls_slide = ls_slide + [s_slide]
            ls_image_org = ls_image_org + [s_image]
            s_round = s_image.split('_')[0]
            ls_round = ls_round + [s_round]
        ls_slide = list(set(ls_slide))
        ls_round = list(set(ls_round))
    dd_images = {} # {slide/scene: {biomarker: image file name}}
    for s_slide in ls_slide:
        d_images = {}
        for s_image in ls_image_org:
            if s_image.find(s_slide) > -1:
                s_marker = s_image.split('_')[1]
                if s_marker != 'DAPI':
                    d_images.update({s_marker:s_image})

        dd_images.update({s_slide:d_images})
    #now make overlays
    for s_slide in ls_slide:
        print(f'Processing {s_slide}')
        #d_border = dd_borders[s_slide]
        d_image = dd_images[s_slide] #load dictionary of biomarker:image
        for s_type in d_combos:
            d_overlay = {}
            ls_combos = d_combos[s_type]
            for s_combo in ls_combos:
                d_overlay.update({s_combo:f'./{d_image[s_combo]}'})
            s_image_round = f'./{s_dapi}_{s_slide}_c1_8bit.tif'
            d_overlay.update({'AAADAPI':s_image_round})
            a_size = io.imread(s_image_round)
            a_overlay = np.zeros((len(d_overlay),a_size.shape[0],a_size.shape[1]),dtype=np.uint8)
            s_biomarker_all = ''
            i = -1 
            for s_color in sorted(d_overlay.keys()):
                i = i + 1
                s_overlay= d_overlay[s_color]
                s_biomarker = s_color.split('AAA')[0] + '.'
                s_biomarker_all = s_biomarker_all + s_biomarker
                a_channel = io.imread(s_overlay)
                a_overlay[i,:,:] = a_channel
            s_biomarker_all = s_biomarker_all[1:-1]
            #this works. Open in image j. use Image/Color/Make Composite. Then use 
            #Image/Color/Channels Tool to turn on and off channels
            #use Image/Adjust/Brightness/Contrast to adjust 
            with skimage.external.tifffile.TiffWriter(f'./{s_type}_{s_dapi.replace("_","")}.{s_biomarker_all}_{s_slide}_overlay.tiff', imagej=True) as tif:
                for i in range(a_overlay.shape[0]):
                    tif.save(a_overlay[i])
    os.chdir('..')

def overlay_by(df_img,d_crop,tu_dim,s_column='marker',ls_drop=['DAPI'],s_label='scene'):
    """
    This is a flexible function to make multipage tiffs to compare selected column across a label
    df_img = dataframe of images with columns ['rounds', 'color', 'imagetype', 'scene', 'marker']
        and index with image names
    d_crop = dictionary with {tissdue-scene-ID:upper left corner x y coordinates
    tu_dim = a tumple of x and y dimensinons of crop
    s_column = column to use to make each image (groups images together)
    ls_drop = columns to exclude
    s_label = column to use to make each page of tiff (images to compare)

    """
    ls_marker = list(set(df_img.loc[:,s_column]))
    for s_drop in ls_drop:
        ls_marker.remove(s_drop)

    for s_marker in ls_marker:
        df_overlay = df_img[(df_img.marker==s_marker)]
        for s_key,s_value in d_crop.items():
            ls_scene_id = []
            d_overlay={}
            df_scene = df_overlay[df_overlay.scene==s_key]
            df_scene = df_scene.sort_values(by=s_label,axis=0,ascending=False)
            for s_index in df_scene.index.tolist():
                a_image=skimage.io.imread(s_index)
                s_label_img = df_scene.loc[s_index,s_label]
                #crop according to dictionary
                tu_crop = d_crop[s_key]
                a_crop = a_image[(tu_crop[1]):(tu_crop[1]+tu_dim[1]),(tu_crop[0]):(tu_crop[0]+tu_dim[0])]
                a_rescale = skimage.img_as_ubyte(a_crop)
                d_overlay.update({f'{s_key}-{s_label_img}':a_rescale})
                ls_scene_id = ls_scene_id + [f'{s_label_img}']
            #print(len(d_overlay))
            with skimage.external.tifffile.TiffWriter(f'./overlay_{s_marker}_{s_key}_{".".join(list([item for item in ls_scene_id]))}.tiff', append=True) as tif:
                for i_key,a_value in d_overlay.items():
                #print(i_key)
                    tif.save(a_value)

def overlay_by_norm(df_img,d_crop,tu_dim,s_column='marker',ls_drop=['DAPI'],s_label='scene',s_norm='exposure'):
    """
    This is a flexible function to make multipage tiffs to compare selected column across a label, normalizing by exposure
    df_img = dataframe of images with columns ['rounds', 'color', 'imagetype', 'scene', 'marker']
        and index with image names
    d_crop = dictionary with {tissdue-scene-ID:upper left corner x y coordinates
    tu_dim = a tumple of x and y dimensinons of crop
    s_column = column to use to make each image
    ls_drop = columns to exclude
    s_label = column to use to make each page of tiff
    s_norm = exposure column to normalize to
    """
    ls_marker = list(set(df_img.loc[:,s_column]))
    for s_drop in ls_drop:
        ls_marker.remove(s_drop)

    for s_marker in ls_marker:
        print(s_marker)
        df_overlay = df_img[(df_img.marker==s_marker)]
        for s_key,s_value in d_crop.items():
            print(s_key)
            ls_scene_id = []
            d_overlay={}
            df_scene = df_overlay[df_overlay.scene==s_key]
            df_scene = df_scene.sort_values(by=s_label,axis=0,ascending=False)
            a_norm = df_scene.loc[:,s_norm].values
            i_min_norm = a_norm.min()
            for s_index in df_scene.index.tolist():
                print(s_index)
                a_image=skimage.io.imread(s_index)
                s_label_img = df_scene.loc[s_index,s_label]
                #crop according to dictionary
                tu_crop = d_crop[s_key]
                a_crop = a_image[(tu_crop[1]):(tu_crop[1]+tu_dim[1]),(tu_crop[0]):(tu_crop[0]+tu_dim[0])]
                #multiply by minumum exposure time divided by actual
                a_norm = (a_crop*(i_min_norm/df_scene.loc[s_index,s_norm])).astype(dtype='uint16')
                print(f'{s_index} scaled by {(i_min_norm/df_scene.loc[s_index,s_norm])}')
                a_rescale = skimage.img_as_ubyte(a_norm)
                d_overlay.update({f'{s_key}-{s_label_img}':a_rescale})
                ls_scene_id = ls_scene_id + [f'{s_label_img}']
                #'''
            #print(len(d_overlay))
            with skimage.external.tifffile.TiffWriter(f'./overlay-norm_{s_marker}_{s_key}_{".".join(list([item for item in ls_scene_id]))}.tiff', append=True) as tif:
                for i_key,a_value in d_overlay.items():
                    tif.save(a_value)

    '''
    from elliot
    overlay_colors = [
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)]

    overlay_markers = []

    #stack =  np.array (M,N,P), P is number of markers, M,N are height and width

    stackmax = stack.max(axis=0).max(axis=0)
    stackmin = stack.min(axis=0).min(axis=0)
    stack -= stackmin

    const = (255 / brightness_const)
    const_array = (stackmax - stackmin) * thresh_df.loc[(str(s), r), overlay_markers].to_numpy() / const

    stack = stack.astype(np.float)
    stack /= const_array.reshape((1, 1, -1))
    stack = np.clip(stack, 0, 255)
    stack = stack.astype(np.uint16)

    overlay = np.zeros(shape=(stack.shape[0], stack.shape[1], 3), dtype=np.uint16)

for i in range(stack.shape[2]):
    if not np.isnan(stack[0,0,i]):
        for j in np.flatnonzero(overlay_colors[i]):
            overlay[:,:,j] += stack[:,:,i]

overlay = np.clip(overlay, 0, 255).astype(np.uint8)
    '''