# wrapper functions for codex image processing

from mplex_image import preprocess, mpimage, getdata, process, analyze, cmif
import os
import pandas as pd
import math
import skimage

def convert_dapi(debugdir,regdir,b_mkdir=True):
    '''
    convert dapi to tif, rename to match Guillaumes pipeline requirements
    '''
    cwd = os.getcwd()
    os.chdir(debugdir)
    for s_dir in sorted(os.listdir()):
        if s_dir.find('R-1_')== 0:
            os.chdir(s_dir)
            for s_file in sorted(os.listdir()):
                if s_file.find('bleach')==-1:
                    s_round = s_file.split("Cycle(")[1].split(").ome.tif")[0]
                    print(f'stain {s_round}')
                    s_dir_new = s_dir.split('_')[2] + '-Scene-0' + s_dir.split('F-')[1]
                    s_tissue_dir = s_dir.split('_F-')[0]
                    if b_mkdir:
                        preprocess.cmif_mkdir([f'{regdir}/{s_tissue_dir}'])
                    a_dapi = skimage.io.imread(s_file)
                    #rename with standard name (no stain !!!!)
                    with skimage.external.tifffile.TiffWriter(f'{regdir}/{s_tissue_dir}/{s_dir_new}_R{s_round}_DAPI_V0_c1_ORG_5.0.tif') as tif:
                        tif.save(a_dapi)
            os.chdir('..')
    os.chdir(cwd)

def convert_channels(processdir, regdir, b_rename=True, testbool=True):
    '''
    convert channels to tif, select one exposure time of three, rename to match Guillaumes pipeline requirements
    '''
    cwd = os.getcwd()
    os.chdir(processdir)
    for s_dir in sorted(os.listdir()):
        if s_dir.find('R-1_')== 0:
            os.chdir(s_dir)
            if b_rename:
                d_rename = {'autofluorescencePE_P':'autofluorescencePE_V0_P',
                'autofluorescenceFITC_F':'autofluorescenceFITC_V0_F',
                '000_DAPIi':'extra000_DAPIi',
                '000_DAPIf':'extra000_DAPIf',
                'extraextraextra':'extra',
                'extraextra':'extra',
                '_FITC_':'_c2_ORG_',
                '_PE_':'_c3_ORG_',}
                preprocess.dchange_fname(d_rename,b_test=testbool)
                
            #parse file names
            else:
                ls_column = ['rounds','marker','dilution','fluor','ORG','exposure','expdecimal','imagetype1','imagetype']
                df_img = mpimage.parse_img(s_end =".tif",s_start='0',s_sep1='_',s_sep2='.',ls_column=ls_column,b_test=False)
                df_img['exposure'] = df_img.exposure.astype(dtype='int')
                ls_marker = sorted(set(df_img.marker))
                for s_marker in ls_marker:
                    df_marker = df_img[df_img.marker==s_marker]
                    df_sort = df_marker.sort_values(by=['exposure'],ascending=False,inplace=False)
                    for idx in range(len(df_sort.index)):
                        s_index = df_sort.index[idx]
                        a_img = skimage.io.imread(s_index)
                        df_file = df_sort.loc[s_index,:]
                        print(a_img.max())
                        if idx < len(df_sort.index) - 1:
                            if a_img.max() < 65535:
                                print(f'Selected {df_file.exposure} for {df_file.marker}')
                                s_dir_new = s_dir.split('_')[2] + '-Scene-0' + s_dir.split('F-')[1]
                                s_tissue_dir = s_dir.split('_F-')[0]
                                s_index_new = s_index.split(".ome.tif")[0]
                                with skimage.external.tifffile.TiffWriter(f'{regdir}/{s_tissue_dir}/{s_dir_new}_R{s_index_new}.tif') as tif:
                                    tif.save(a_img)
                                break
                            else:
                                print('Try lower exposure time')
                        elif idx == len(df_sort.index) - 1:
                            print(f'Selected as the lowest exposure time {df_file.exposure} for {df_file.marker}')
                            s_dir_new = s_dir.split('_')[2] + '-Scene-0' + s_dir.split('F-')[1]
                            s_tissue_dir = s_dir.split('_F-')[0]
                            s_index_new = s_index.split(".ome.tif")[0]
                            with skimage.external.tifffile.TiffWriter(f'{regdir}/{s_tissue_dir}/{s_dir_new}_R{s_index_new}.tif') as tif:
                                tif.save(a_img)
                        else:
                            print('/n /n /n /n Error in finding exposure time')
        
            os.chdir('..')

def parse_converted(regdir):
        '''
        parse the converted miltenyi file names,
        regdir contains the images
        '''
        s_dir = os.getcwd()
        df_img = mpimage.filename_dataframe(s_end = ".tif",s_start='G',s_split='_')
        df_img.rename({'data':'scene'},axis=1,inplace=True)
        df_img['rounds'] = [item[1] for item in [item.split('_') for item in df_img.index]]
        df_img['marker'] = [item[2] for item in [item.split('_') for item in df_img.index]]
        df_img['dilution'] = [item[3] for item in [item.split('_') for item in df_img.index]]
        df_img['color'] = [item[4] for item in [item.split('_') for item in df_img.index]]
        df_img['scene_int'] = [item.split('Scene-')[1] for item in df_img.scene]
        df_img['scene_int'] = df_img.scene_int.astype(dtype='int')
        df_img['exposure'] = [item[6].split('.')[0] for item in [item.split('_') for item in df_img.index]]
        df_img['path'] = [f'{regdir}/{s_dir}/{item}' for item in df_img.index]
        df_img['tissue'] = s_dir
        return(df_img)

def parse_converted_dirs(regdir):
    '''
    parse the converted miltenyi file names,
    regdir is the master folder containing subfolders with ROIs/gates
    '''
    os.chdir(regdir)
    df_img_all = pd.DataFrame()
    for idx, s_dir in enumerate(sorted(os.listdir())):
        os.chdir(s_dir)
        s_sample = s_dir
        print(s_sample)
        df_img = parse_converted(s_dir)
        df_img_all = df_img_all.append(df_img)
        os.chdir('..')
    return(df_img_all)

def count_images(df_img,b_tile_count=True):
    """
    count and list slides, scenes, rounds
    """
    df_count = pd.DataFrame(index=sorted(set(df_img.scene)),columns=sorted(set(df_img.color)))
    for s_sample in sorted(set(df_img.tissue)):
        print(f'ROI {s_sample}')
        df_img_slide = df_img[df_img.tissue==s_sample]
        print('tiles')
        [print(item) for item in sorted(set(df_img_slide.scene))]
        print(f'Number of images = {len(df_img_slide)}')
        print(f'Rounds:')
        [print(item) for item in sorted(set(df_img_slide.rounds))]
        print('\n')
        if b_tile_count:
            for s_scene in sorted(set(df_img_slide.scene)):
                df_img_scene = df_img_slide[df_img_slide.scene==s_scene]
                for s_color in sorted(set(df_img_scene.color)):
                    print(f'{s_scene} {s_color} {len(df_img_scene[df_img_scene.color==s_color])}')
                    df_count.loc[s_scene,s_color] = len(df_img_scene[df_img_scene.color==s_color])
    return(df_count)

def visualize_reg_images(regdir,qcdir,color='c1',tu_array=(3,2)):
    """
    array registered images to check tissue identity, focus, etc.
    """
    #check registration
    preprocess.cmif_mkdir([f'{qcdir}/RegisteredImages'])
    cwd = os.getcwd()
    os.chdir(regdir)
    for idx, s_dir in enumerate(sorted(os.listdir())):
        os.chdir(s_dir)
        s_sample = s_dir
        print(s_sample)
        df_img = parse_converted(s_dir)
        ls_scene = sorted(set(df_img.scene))
        for s_scene in ls_scene:
            print(s_scene)
            df_img_scene = df_img[df_img.scene == s_scene]
            df_img_stain = df_img_scene[df_img_scene.color==color]
            df_img_sort = df_img_stain.sort_values(['rounds'])
            i_sqrt = math.ceil(math.sqrt(len(df_img_sort)))
            #array_img(df_img,s_xlabel='color',ls_ylabel=['rounds','exposure'],s_title='marker',tu_array=(2,4),tu_fig=(10,20))
            if color == 'c1':
                fig = mpimage.array_img(df_img_sort,s_xlabel='marker',ls_ylabel=['rounds','exposure'],s_title='rounds',tu_array=tu_array,tu_fig=(16,14))
            else:
                fig = mpimage.array_img(df_img_sort,s_xlabel='color',ls_ylabel=['rounds','exposure'],s_title='marker',tu_array=tu_array,tu_fig=(16,12))
            fig.savefig(f'{qcdir}/RegisteredImages/{s_scene}_registered_{color}.png')
        os.chdir('..')
    os.chdir(cwd)
    #return(df_img)

def rename_files(d_rename,dir,b_test=True):
    """
    change file names
    """
    cwd = os.getcwd()
    os.chdir(dir)
    for idx, s_dir in enumerate(sorted(os.listdir())):
        s_path = f'{dir}/{s_dir}'
        os.chdir(s_path)
        print(s_dir)
        df_img = mpimage.filename_dataframe(s_end = ".tif",s_start='reg',s_split='_')
        df_img.rename({'data':'scene'},axis=1,inplace=True)
        df_img['rounds'] = [item[1] for item in [item.split('_') for item in df_img.index]]
        df_img['color'] = [item[2] for item in [item.split('_') for item in df_img.index]]
        df_img['marker'] = [item[3].split('.')[0] for item in [item.split('_') for item in df_img.index]]
        if b_test:
            print('This is a test')
            preprocess.dchange_fname(d_rename,b_test=True)
        elif b_test==False:
            print('Changing name - not a test')
            preprocess.dchange_fname(d_rename,b_test=False)
        else:
            pass

def rename_fileorder(s_sample, dir, b_test=True):
    """
    change file names
    """
    cwd = os.getcwd()
    os.chdir(dir)
    for idx, s_dir in enumerate(sorted(os.listdir())):
        s_path = f'{dir}/{s_dir}'
        os.chdir(s_path)
        print(s_dir)
        df_img = mpimage.filename_dataframe(s_end = ".tif",s_start='Scene',s_split='_')
        df_img.rename({'data':'scene'},axis=1,inplace=True)
        df_img['rounds'] = [item[1] for item in [item.split('_') for item in df_img.index]]
        df_img['color'] = [item[2] for item in [item.split('_') for item in df_img.index]]
        df_img['marker'] = [item[3].split('.')[0] for item in [item.split('_') for item in df_img.index]]
        for s_index in df_img.index:
            s_round = df_img.loc[s_index,'rounds']
            s_scene= f"{s_sample}-{df_img.loc[s_index,'scene']}"
            s_marker = df_img.loc[s_index,'marker']
            s_color = df_img.loc[s_index,'color']
            s_index_rename = f'{s_round}_{s_scene}_{s_marker}_{s_color}_ORG.tif'
            d_rename = {s_index:s_index_rename}
            if b_test:
                print('This is a test')
                preprocess.dchange_fname(d_rename,b_test=True)
            elif b_test==False:
                print('Changing name - not a test')
                preprocess.dchange_fname(d_rename,b_test=False)
            else:
                pass


def copy_files(dir,dapi_copy, marker_copy,testbool=True,type='codex'):
    """
    copy and rename files if needed as dummies
    need to edit
    """
    os.chdir(dir)
    for idx, s_dir in enumerate(sorted(os.listdir())):
        s_path = f'{dir}/{s_dir}'
        os.chdir(s_path)
        #s_sample = s_dir.split('-Scene')[0]
        df_img = mpimage.filename_dataframe(s_end = ".tif",s_start='Scene',s_split='_')
        df_img.rename({'data':'scene'},axis=1,inplace=True)
        df_img['rounds'] = [item[1] for item in [item.split('_') for item in df_img.index]]
        df_img['color'] = [item[2] for item in [item.split('_') for item in df_img.index]]
        df_img['marker'] = [item[3].split('.')[0] for item in [item.split('_') for item in df_img.index]]
        print(s_dir)
        #if b_test:
        for key, dapi_item in dapi_copy.items():
                df_dapi = df_img[(df_img.rounds== key.split('_')[1]) & (df_img.color=='c1')]
                s_dapi = df_dapi.loc[:,'marker'][0]
                preprocess.copy_dapis(s_r_old=key,s_r_new=f'_cyc{dapi_item}_',s_c_old='_c1_',
                 s_c_new='_c2_',s_find=f'_c1_{s_dapi}_ORG.tif',b_test=testbool,type=type)
        i_count=0
        for idx,(key, item) in enumerate(marker_copy.items()):
                preprocess.copy_markers(df_img, s_original=key, ls_copy = item,
                 i_last_round= dapi_item + i_count, b_test=testbool,type=type)
                i_count=i_count + len(item)

def segmentation_thresholds(regdir,qcdir, d_segment):
    """
    visualize binary mask of segmentaiton threholds
    need to edit
    """
    preprocess.cmif_mkdir([f'{qcdir}/Segmentation'])
    os.chdir(regdir)
    for idx, s_dir in enumerate(sorted(os.listdir())):
        s_path = f'{regdir}/{s_dir}'
        os.chdir(s_path)
        df_img = mpimage.filename_dataframe(s_end = ".tif",s_start='Scene',s_split='_')
        df_img.rename({'data':'scene'},axis=1,inplace=True)
        df_img['rounds'] = [item[1] for item in [item.split('_') for item in df_img.index]]
        df_img['color'] = [item[2] for item in [item.split('_') for item in df_img.index]]
        df_img['marker'] = [item[3].split('.')[0] for item in [item.split('_') for item in df_img.index]]
        s_sample = s_dir
        print(s_sample)
        d_seg = preprocess.check_seg_markers(df_img,d_segment, i_rows=1, t_figsize=(6,6)) #few scenes
        for key, fig in d_seg.items():
            fig.savefig(f'{qcdir}/Segmentation/{s_dir}_{key}_segmentation.png')


def segmentation_inputs(s_sample,regdir,segdir,d_segment,b_start=False):
    """
    make inputs for guillaumes segmentation
    """
    os.chdir(regdir)
    for idx, s_dir in enumerate(sorted(os.listdir())):
        s_path = f'{regdir}/{s_dir}'
        os.chdir(s_path)
        df_img = mpimage.filename_dataframe(s_end = ".tif",s_start='R',s_split='_')
        df_img.rename({'data':'rounds'},axis=1,inplace=True)
        #df_img['rounds'] = [item[1] for item in [item.split('_') for item in df_img.index]]
        df_img['color'] = [item[3] for item in [item.split('_') for item in df_img.index]]
        df_img['marker'] = [item[2] for item in [item.split('_') for item in df_img.index]]
        #s_sample = s_dir
        #s_sample = s_dir.split('-Scene')[0]
        print(s_sample)
        df_marker = df_img[df_img.color!='c1']
        df_marker = df_marker.sort_values(['rounds','color'])
        df_dapi = pd.DataFrame(index = [df_marker.marker.tolist()],columns=['rounds','colors','minimum','maximum','exposure','refexp','location'])
        df_dapi['rounds'] = df_marker.loc[:,['rounds']].values
        df_dapi['colors'] = df_marker.loc[:,['color']].values
        df_dapi['minimum'] = 1003
        df_dapi['maximum'] = 65535
        df_dapi['exposure'] = 100
        df_dapi['refexp'] = 100
        df_dapi['location'] = 'All'
        for s_key,i_item in d_segment.items():
            df_dapi.loc[s_key,'minimum'] = i_item
        df_dapi.to_csv('RoundsCyclesTable.txt',sep=' ',header=False)
        df_dapi.to_csv(f'metadata_{s_sample}_RoundsCyclesTable.csv',header=True)
        #create cluster.java file
        preprocess.cluster_java(s_dir=f'JE{idx}',s_sample=s_sample,imagedir=f'{s_path}',segmentdir=segdir,type='exacloud',b_segment=True,b_TMA=False)
        if b_start:
            os.chdir(f'/home/groups/graylab_share/Chin_Lab/ChinData/Work/engje/exacloud/JE{idx}') #exacloud
            print(f'JE{idx}')
            os.system('make_sh')
