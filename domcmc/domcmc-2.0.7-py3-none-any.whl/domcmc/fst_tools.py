"""
A module for quickly reading data from files in the in CMC "standard" format.
Basically everything is done through the **get_data** function.



"""

from typing import Callable, Iterator, Union, Optional, List, Iterable, MutableMapping
import datetime

def get_data(file_name:     Optional[str]=None,
             dir_name:      Optional[str]=None,
             prefix:        Optional[str]='',
             suffix:        Optional[str]='',
             var_name:      str=None,
             datev:         Optional[Union[int,datetime.datetime]]=None,
             ip1:           Optional[Union[List[int],int]]=None,
             ip2:           Optional[int]=None,
             ip3:           Optional[int]=None,
             ig1:           Optional[int]=None,
             ig2:           Optional[int]=None,
             ig3:           Optional[int]=None,
             typvar:        Optional[str]=None,
             etiquette:     Optional[str]=None,
             latlon:        Optional[bool]=False,
             pres_from_var: Optional[bool]=False,
             pres_levels:   Optional[Iterable[int]]=None,
             tmp_dir:       Optional[str]=None) :


    """ Read data from CMC 'standard' files 

       - Entries with same validity date but different IP1s get sorted, concatenated and are output as a 3D array.
       - 2D latitudes and longitudes associated with the requested data are optionally outputted
       - Pressure values associated with requested data are optionally outputted
       - Vertical interpolation on pressure levels is supported 
       - Option to search valid entry in all standard files located within a directory 

    Args:
       file_name:     /path/to/fst/file.fst
       dir_name:      /path/to/a/directory/containing/fst/files/
                      Search all standard files within a directory for a match
                      with search criteria.
                      Searching all files in large directories can take a while,
                      use prefix and suffix to constrain search.
                      Note that file_name superseeds dir_name
       prefix:        In combination with dir_name; prefix of files to search
       suffix:        In combination with dir_name; suffix of files to search
       var_name:      Name of variable to read in fst file  eg:   UU, VV, TT, MPQC, etc.
       pres_from_var: Flag to output pressure associated with returned data
       datev:         Cmc timestamp for validity date of retrieved data
       ip1:           Criterion for choosing what data will be read.
                      A list of ip1s can be provided to read a number of levels
                      in one function call.
       ip2:           Criterion for choosing what data will be read
       ip3:           Criterion for choosing what data will be read
       ig1:           Criterion for choosing what data will be read
       ig2:           Criterion for choosing what data will be read
       ig3:           Criterion for choosing what data will be read
       typvar:        Criterion for choosing what data will be read
       etiquette:     Criterion for choosing what data will be read
       latlon:        Flag to output 2D grids of latitude and longitudes associated with data
       pres_levels:   List of pressure levels [hPa] onto which data is desired   eg [850,700,500]
       tmp_dir:       /path/to/a/temporary/work/directory/   Only used for interpolation to pressure levels
                      if None, $TMPDIR is used; may run out of space when large fields are interpolated

    Returns:
        {
            'values':   (ndarray) 2D or 3D array containing data  k=0 -> lowest level

            'meta':     (dict) meta data of the first matching entry in fst file

            'grid':     (dict) hgrid as returned by readGrid of rpn python

            'toctoc':   (dict) toctoc (!!) entry associated with data as returned by fstlir of rpn python

            'ip1_list': (list) ip1s for each level being returned

            'lev_list': (list) levels corresponding to the ip1s in ip1_list

            'lat':      (ndarray) 2D latitudes of data grid (conditional on latlon=True)

            'lon':      (ndarray) 2D longitudes of data grid (conditional on latlon=True)

            'pressure': (ndarray) 2D or 3D array of pressure (conditional on pres_levels)

        }


    Examples:

       Get first matching entry of P0 as a 2D ndarray. 

       >>> import domcmc.fst_tools as fst_tools
       >>> fst_file = '/home/dja001/shared_stuff/files/python_test_data/2016081200_006_0001'
       >>> p0 = fst_tools.get_data(file_name=fst_file, var_name='P0')
       >>> print(p0.keys())
       dict_keys(['values', 'meta', 'grid', 'toctoc', 'ip1_list', 'lev_list'])
       >>> print(p0['values'].shape)
       (328, 278)


       Get P0 at a different validity date:

       >>> import domcmc.fst_tools as fst_tools
       >>> import datetime
       >>> fst_file = '/home/dja001/shared_stuff/files/python_test_data/2016081200_006_0001'
       >>> #
       >>> #directly with a datetime object
       >>> dt = datetime.datetime(2016, 8, 12, 6, 10, 0, tzinfo=datetime.timezone.utc)
       >>> p0 = fst_tools.get_data(file_name=fst_file, var_name='P0', datev=dt)
       >>> print(p0.keys())
       dict_keys(['values', 'meta', 'grid', 'toctoc', 'ip1_list', 'lev_list'])
       >>> print(p0['values'].shape)
       (328, 278)
       >>> #
       >>> #with a CMC timestamp
       >>> p0 = fst_tools.get_data(file_name=fst_file, var_name='P0', datev=412062350)
       >>> print(p0.keys())
       dict_keys(['values', 'meta', 'grid', 'toctoc', 'ip1_list', 'lev_list'])
       >>> print(p0['values'].shape)
       (328, 278)


       Get UU as a 3D ndarray. 
       Output 'lat' and 'lon' as 2D numpy arrays of latitudes and longitudes associated with the grid of UU

       >>> import domcmc.fst_tools as fst_tools
       >>> fst_file = '/home/dja001/shared_stuff/files/python_test_data/2016081200_006_0001'
       >>> uu = fst_tools.get_data(file_name=fst_file, var_name='UU', latlon=True)
       >>> print(uu.keys())
       dict_keys(['values', 'meta', 'grid', 'toctoc', 'ip1_list', 'lev_list', 'lat', 'lon'])
       >>> print(uu['values'].shape)
       (328, 278, 81)
       >>> print(uu['lat'].shape, uu['lon'].shape)
       (328, 278) (328, 278)

       Get VV as a 3D ndarray given by the input of ip1 list. 
       Also output latitudes and longitudes associated with the grid of VV 

       >>> import domcmc.fst_tools as fst_tools
       >>> fst_file = '/home/dja001/shared_stuff/files/python_test_data/2016081200_006_0001'
       >>> ip1_input = [75597472, 95258609, 95237745, 95011105, 94859092, 94831040]
       >>> vv = fst_tools.get_data(file_name=fst_file, var_name='VV', ip1=ip1_input, latlon=True)
       >>> print(vv.keys())
       dict_keys(['values', 'meta', 'grid', 'toctoc', 'ip1_list', 'lev_list', 'lat', 'lon'])
       >>> print(vv['values'].shape)
       (328, 278, 6)
       >>> print(vv['ip1_list'])
       [75597472, 95258609, 95237745, 95011105, 94859092, 94831040]
       >>> print(vv['lat'].shape, vv['lon'].shape)
       (328, 278) (328, 278)
       >>>
       >>> #note that even with a list of ip1s, output levels get sorted 
       >>> #from lowest to highest
       >>> ip1_input = [ 95258609, 94859092, 95011105, 95237745, 94831040, 75597472]
       >>> vv = fst_tools.get_data(file_name=fst_file, var_name='VV', ip1=ip1_input, latlon=True)
       >>> print(vv['ip1_list'])
       [75597472, 95258609, 95237745, 95011105, 94859092, 94831040]


       Get first matching entries of HU as 3D numpy array. 
       Output pressure associated with HU

       >>> import domcmc.fst_tools as fst_tools
       >>> fst_file = '/home/dja001/shared_stuff/files/python_test_data/2016081200_006_0001'
       >>> hu = fst_tools.get_data(file_name=fst_file, var_name='HU', pres_from_var=True)
       >>> print(hu.keys())
       dict_keys(['values', 'meta', 'grid', 'toctoc', 'ip1_list', 'lev_list', 'pressure'])
       >>> print(hu['values'].shape)
       (328, 278, 81)
       >>> print(hu['pressure'].shape)
       (328, 278, 81)


       Get TT field interpolated at 800, 500 and 200 hPa.
       returned 'values' is a 3D array where k=0 indicates the lowest level (here 800 hPa)
       pxs2pxt must be available in environment
       https://wiki.cmc.ec.gc.ca/wiki/Pxs2pxt

       >>> import domcmc.fst_tools as fst_tools
       >>> fst_file = '/home/dja001/shared_stuff/files/python_test_data/2016081200_006_0001'
       >>> # if the fst file is large, you may run out of space in $TMPDIR and 
       >>> # get weird errors. 
       >>> # In this case use tmp_dir=/path/to/big/temporary/directory/ in your call to get_data
       >>> tt = fst_tools.get_data(file_name=fst_file, var_name='TT', pres_levels=[800,500,200])
       >>> print(tt.keys())
       dict_keys(['values', 'meta', 'grid', 'toctoc', 'ip1_list', 'lev_list'])
       >>> print(tt['values'].shape)
       (328, 278, 3)

       It is often the case that a directory will contain many standard files, each containing entries
       at different validity times. Because of the different naming conventions found at the CMC, it
       then becomes cumbersome to figure out which file contains the desired entries at a given validity 
       time. To address this problem, use the dir_name option. All standard files will be searched
       for the desired entry. 

       >>> import domcmc.fst_tools as fst_tools
       >>> import datetime
       >>> fst_dir = '/home/dja001/shared_stuff/files/python_test_data/'
       >>> dt = datetime.datetime(2016, 8, 12, 6, 20, 0, tzinfo=datetime.timezone.utc)
       >>> pr = fst_tools.get_data(dir_name=fst_dir, var_name='PR', datev=dt)
       >>> print(pr.keys())
       dict_keys(['values', 'meta', 'grid', 'toctoc', 'ip1_list', 'lev_list'])
       >>> print(pr['values'].shape)
       (324, 274)
       >>> # For large directories containing many standard files, use the prefix and/or suffix arguments to 
       >>> # restrict the search and speedup things
       >>> # in the following example, only files matching 2016081200*0001 will be searched.
       >>> pr2 = fst_tools.get_data(dir_name=fst_dir, prefix='2016081200', suffix='0001', var_name='PR', datev=dt)
       >>> print(pr2.keys())
       dict_keys(['values', 'meta', 'grid', 'toctoc', 'ip1_list', 'lev_list'])
       >>> print(pr2['values'].shape)
       (324, 274)

       The Yin-Yang grid can be represented in different ways in standard files. 
       
       Sometimes, both the Yin and Yang grids are combined and appear as single entries in 
       standard files. 
       In these cases, the *get_data* method will separate the Yin and Yang grids for you. 
       In the following example, look for the "yin" and "yang" entries that appear in the output 
       dictionary. Each comes with its own values, meta data and lat/lon. 

       For convenience, the "regular" values, meta data and lat/lon are set to those of the Yin grid. 
       
       >>> import domcmc.fst_tools as fst_tools
       >>> import datetime
       >>> fst_file = '/home/dja001/shared_stuff/files/python_test_data/2016122900_yinyang_example.fst'
       >>> dt = datetime.datetime(2016, 12, 29, 0, 0, 0, tzinfo=datetime.timezone.utc)
       >>> pr = fst_tools.get_data(file_name=fst_file, var_name='PR', datev=dt, latlon=True)
       >>> # Note the yin and yang entries in this dictionary
       >>> # "values", "lat" and "lon" are those of the Yin grid
       >>> print(pr.keys())
       dict_keys(['values', 'meta', 'grid', 'toctoc', 'ip1_list', 'lev_list', 'yin', 'yang', 'lat', 'lon'])
       >>> #data on the Yin grid
       >>> print(pr['yin'].keys())
       dict_keys(['meta', 'toctoc', 'ip1_list', 'lev_list', 'grid', 'values', 'lat', 'lon'])
       >>> #data on the Yang grid
       >>> print(pr['yang'].keys())
       dict_keys(['meta', 'toctoc', 'ip1_list', 'lev_list', 'grid', 'values', 'lat', 'lon'])



    """

    import numpy as np
    import os
    import warnings
    import glob
    import subprocess
    import copy
    import rpnpy.librmn.all as rmn
    import rpnpy.utils.fstd3d as fstd3d
    import rpnpy.vgd.all as vgd
    from   rpnpy.rpndate import RPNDate
    import datetime

    #was varname specified
    if var_name is None :
        raise ValueError('var_name: must be set to a fst variable name eg P0, UU, TT, etc')

    #get cmc_timestamp from datev
    if datev is None :
        cmc_timestamp=None
    else:
        if isinstance(datev, datetime.datetime):
            date_obj = RPNDate(datev)
            cmc_timestamp = date_obj.datev
        else:
            #assume a cmc timestamp is passed
            try:
                cmc_timestamp=int(datev)
            except:
                raise ValueError('datev can only a datetime.datetime object OR a an integer representing a CMC timestamp')

    #use file_name or find file with matching entry
    if file_name is not None :
        #if file_name was provided use this
        if not os.path.isfile(file_name) :
            #files does not exist, throw a warning and return None
            warnings.warn('file_name: ' + file_name + ' does not exist')
            return None
        #by default input file is the file that will be read
        file_to_read = file_name
    else :
        if dir_name is not None :
            #iterate over files in dir_name and check which one match the search criterion
            #non FST files are skipped
            if not os.path.isdir(dir_name) :
                raise ValueError('dir_name: ' + file_name + ' is not a valid path')
            #get a list of files in there
            file_list = glob.glob(dir_name + '/' + prefix + '*' + suffix)
            if len(file_list) == 0 :
                raise RuntimeError('no files in :' + dir_name + '/' + prefix + '*' + suffix)
            file_to_read = None
            for this_file in file_list :
                found_file = None
                if pres_levels is not None :
                    #entries necessary for vertical interpolation
                    p0 = _get_var(this_file, 'P0',
                                  datev=cmc_timestamp,
                                  ip1=None, ip2=None, ip3=None,
                                  ig1=ig1,  ig2=ig2,  ig3=ig3,
                                  typvar=typvar, etiquette=etiquette,
                                  meta_only=True, verbose=0,
                                  skip_non_fst=True)
                    var = _get_var(this_file, var_name,
                                   datev=p0['meta']['datev'],
                                   ip1=None, ip2=None, ip3=None,
                                   ig1=ig1,  ig2=ig2,  ig3=ig3,
                                   typvar=typvar, etiquette=etiquette,
                                   meta_only=True, verbose=0,
                                   skip_non_fst=True)
                    if (p0 is not None) and (var is not None) :
                        #this file contains all necessary data
                        found_file = this_file
                else :
                    #entry necessary for normal retrieval
                    var = _get_var(this_file, var_name,
                                   datev=cmc_timestamp,
                                   ip1=ip1, ip2=ip2, ip3=ip3,
                                   ig1=ig1, ig2=ig2, ig3=ig3,
                                   typvar=typvar, etiquette=etiquette,
                                   meta_only=True, verbose=0,
                                   skip_non_fst=True)
                    if var is not None :
                        #this file contains all necessary data
                        found_file = this_file

                    #endif

                if found_file is not None :
                    if file_to_read is not None :
                        raise RuntimeError('search criterion matched in two different files:'+file_to_read+'   '+this_file)
                    else:
                        file_to_read = this_file
            #endfor

            #if no match found after iterating over all files, return None
            if file_to_read is None :
                return None
    
        else :
            raise ValueError('Please provide one of file_name or dir_name arguments')

    #a random number for temporary files
    rand = np.round(np.random.rand(1)*1e7).astype('int')
    rand_str = '{:07d}'.format(rand[0])

    #temporary dir for this session
    if tmp_dir is None :
        tmp_dir = os.environ['TMPDIR']
    #valid dir
    if not os.path.exists(tmp_dir) :
        raise ValueError('tmp_dir: ' + tmp_dir + ' is not a valid path ')

    #vertical interpolation  to pressure levels is desired
    remove_interpolated = False
    if pres_levels is not None :
        remove_interpolated = True

        #comma separated string with list of levels [hPa]
        level_str = ''
        for thisLevel in pres_levels :
            level_str += '{:07.2f}'.format(thisLevel)+','
        level_str = level_str.rstrip(',')

        #code for type of interpolation eg CUB_UU
        #CUB_    CUBIC   
        #CUBP_   CUBIC   Clip negative values
        #LIN_    LINEAR  
        #NOI_    NO INTERPOLATION    Use for surface or 2D  variables only 
        var_str= 'CUB_' + var_name


        #get info on P0 and desired variable
        p0 = _get_var(file_name, 'P0',
                      datev=cmc_timestamp,
                      ip1=None, ip2=None, ip3=None,
                      ig1=ig1,  ig2=ig2,  ig3=ig3,
                      typvar=typvar, etiquette=etiquette)
        if p0 is None:
            raise ValueError('P0 is necessary for vertical interpolation')

        var = _get_var(file_name, var_name,
                       datev=p0['meta']['datev'],
                       ip1=None, ip2=None, ip3=None,
                       ig1=ig1,  ig2=ig2,  ig3=ig3,
                       typvar=typvar, etiquette=etiquette,
                       meta_only=True)
        if var is None:
            raise ValueError(var_name + 'not found in source fst file')
         
        #files necessary for vertical interpolation
        pxs_file        = tmp_dir + '/' + rand_str + 'tempPxsFile.fst'
        interp_file     = tmp_dir + '/' + rand_str + 'interplated.fst'

        #check that variable and p0 are on same grid
        if (p0['meta']['ig1'] == var['meta']['ig1']) and (p0['meta']['ig2'] == var['meta']['ig2']) :
            #P0 and var are on the same grid

            #first step is to get P0 in the pxs file
            try:
               iunit = rmn.fstopenall(pxs_file,rmn.FST_RW)
            except:
               raise rmn.FSTDError("File not found/readable: %s" % pxs_file)
             
            try:
               # Write P0 record + grid identifiers
               p0_entry = p0['meta']
               p0_entry['d'] = np.asfortranarray(p0['values'],dtype='float32')
               rmn.fstecr(iunit, p0_entry)
               rmn.writeGrid(iunit, p0['grid'])
               rmn.fstecr(iunit, p0['toctoc'])
            except:
               raise RuntimeError('something went wrong writing P0 fst file')
            finally:
                # always close file
                rmn.fstcloseall(iunit)
        else:
            #interpolate p0 to variable grid
            #   Not sure this is needed anymore.... 
            raise RuntimeError('hinterp with P0 on a different grid not yet implemented')

        #Do the interpolation
        #make sure interpolation package is loaded
        try:
            path = subprocess.check_output(["which", "d.pxs2pxt"])
        except:
            raise RuntimeError('you must load pxs2pxt:   . ssmuse-sh -d eccc/cmd/cmdn/pxs2pxt/3.16.6/default')
        
        cmd= ['d.pxs2pxt', '-s'    , file_name,
                           '-datev', '{:07d}'.format(p0['meta']['datev']),
                           '-d'    , interp_file,
                           '-pxs'  , pxs_file,
                           '-plevs', level_str,
                           '-var'  , var_str]
        try:
            subprocess.run(cmd)
        except:
            raise RuntimeError('Something went wrong with pxs2pxt')

        #cleanup
        os.remove(pxs_file)

        #change file_to_read to interpolated data file
        file_to_read = interp_file

    #END vertical interpolation if statement --------------------------------

    #get fst data for output
    var = _get_var(file_to_read, var_name,
                   datev=cmc_timestamp,
                   ip1=ip1, ip2=ip2, ip3=ip3,
                   ig1=ig1, ig2=ig2, ig3=ig3,
                   typvar=typvar, etiquette=etiquette)

    #get 3D pressure if requested
    if (var is not None) and pres_from_var :

        #error trapping done by _get_var above
        iunit = rmn.fstopenall(file_to_read,rmn.FST_RO)

        try:
            #linked ip1/ig1 ip2/ig2
            vgrid = vgd.vgd_read(iunit, ip1=var['meta']['ig1'], ip2=var['meta']['ig2'])
        except:
            rmn.fstcloseall(iunit)
            raise RuntimeError('something went wrong getting vertical grid descriptor')

        try:
            this_datev = cmc_timestamp if cmc_timestamp is not None else -1
            press = fstd3d.get_levels_press(iunit, vgrid, var['values'].shape[0:2], var['ip1_list'],
                                            datev=this_datev)
        except:
            raise RuntimeError('something went wrong with pressure retrieval')
        finally:
            rmn.fstcloseall(iunit)

        #add pressure to output dictionary
        var['pressure'] = press['phPa']


    #handle yin-yang grid in one record
    # optionally output lat/lon information
    if (var is not None):

        if 'nsubgrids' not in var['grid']:
            ngrids = 1
        else:
            ngrids = var['grid']['nsubgrids']

        if ngrids == 1 and latlon == True :
	    #single grid -> not yin-yang
            ll_dict = rmn.gdll(var['grid'])
            var['lat'] = ll_dict['lat']
            var['lon'] = ll_dict['lon']

        elif ngrids == 2: 
	    #two grids -> yin-yang
	    #In this case, the outdict is modified to output data on the two grids
            #with the "unnamed" defaut output refering to the yin grid.

            #links to common entries in var dict
            var['yin']  = {'meta':     var['meta'],
                           'toctoc':   var['toctoc'],
                           'ip1_list': var['ip1_list'],
                           'lev_list': var['lev_list']}
            var['yang'] = {'meta':     var['meta'],
                           'toctoc':   var['toctoc'],
                           'ip1_list': var['ip1_list'],
                           'lev_list': var['lev_list']}

            #yin grid 
            var['yin']['grid']  = copy.deepcopy(var['grid']['subgrid'][0])
            #yang grid 
            var['yang']['grid'] = copy.deepcopy(var['grid']['subgrid'][1])
            #grid in var dict is a link to yin grid
            var['grid'] = var['yin']['grid']

            #temp copy of values
            yy_values = copy.deepcopy(var['values'])
            nx, ny = yy_values.shape
            half_ny = int(ny/2)
            #yin values 
            var['yin']['values']  = copy.deepcopy(yy_values[:,:half_ny])
            #yang values 
            var['yang']['values'] = copy.deepcopy(yy_values[:,half_ny:])
            #values in var is a link to yin values
            var['values'] = var['yin']['values']

            #outout latlon if desired
            if latlon == True :
                #yin
                ll_yin  = rmn.gdll(var['yin']['grid'])
                var['yin']['lat'] = copy.deepcopy(ll_yin['lat'])
                var['yin']['lon'] = copy.deepcopy(ll_yin['lon'])
                #yang
                ll_yang = rmn.gdll(var['yang']['grid'])
                var['yang']['lat'] = copy.deepcopy(ll_yang['lat'])
                var['yang']['lon'] = copy.deepcopy(ll_yang['lon'])
                #latlon in var are those of the yin grid
                var['lat'] = var['yin']['lat']
                var['lon'] = var['yin']['lon']

    #remove fst file containing interpolated data
    if remove_interpolated:
        os.remove(interp_file)

    return var

#end of get_data





def _get_var(file_name, var_name,
             datev=None,  #input
             ip1=None, ip2=None, ip3=None,
             ig1=None, ig2=None, ig3=None,
             typvar=None, etiquette=None,
             meta_only=False, verbose=0, skip_non_fst=False) :
    """
    get variable in fst file

        Search can be restricted to certain ip123, ig123, typvar and etiquette.

        It is also possible to obtain a subset of vertical levels by providing a 
        list of desired ip1s
        
        If the keyword **ip1** is not specified fst entries with the 
        the same meta but different ip1s will be concatenated into a 3d array for output

        The smallest k index will correspond to the lowest vertical level.

        if meta_only=True the routine returns the meta data for the first entry and stops

    """
    import numpy as np
    import rpnpy.librmn.all as rmn
    import warnings

    if not rmn.isFST(file_name) :
        if skip_non_fst == False :
            #default behaviour is to abort on non FST files
            raise rmn.FSTDError("Not an FSTD file: %s " % file_name)
        else :
            #with skip_non_fst=True, None is returned without error
            return None
     
    # Open
    try:
        iunit = rmn.fstopenall(file_name, rmn.FST_RO)
    except:
        raise rmn.FSTDError("File not found/readable: %s" % file_name)
     
    #look for first entry matching search criteria 
    if type(ip1) is list :
        for myip1 in ip1 :
            key_dict = _my_fstinf(iunit, datev=datev, etiket=etiquette,
                                  ip1=myip1, ip2=ip2, ip3=ip3,
                                  ig1=ig1, ig2=ig2, ig3=ig3,
                                  typvar=typvar, nomvar=var_name)
            if key_dict is not None:
            # found at least one record
                break
    else:
        key_dict = _my_fstinf(iunit, datev=datev, etiket=etiquette,
                              ip1=ip1, ip2=ip2, ip3=ip3,
                              ig1=ig1, ig2=ig2, ig3=ig3,
                              typvar=typvar, nomvar=var_name)

    if key_dict is None :
        nz = 0
        is_there = False
        rmn.fstcloseall(iunit)
        if verbose > 0 :
            print('Did not find anything in:')
            print(file_name)
            print('with:')
            print('var_name=', var_name)
            print('datev='   , datev)
            if datev is not None:
                try:
                    (yyyymmdd, hhmmsshh) = rmn.newdate(rmn.NEWDATE_STAMP2PRINT, int(datev))
                except rmn.RMNBaseError:
                    print('Invalid CMC datestamp')
                print('       yyyymmdd hhmmss: ', yyyymmdd, hhmmsshh)
            print('ip1='         , ip1)
            print('ip2='         , ip2)
            print('ip3='         , ip3)
            print('ig1='         , ig1)
            print('ig2='         , ig2)
            print('ig3='         , ig3)
            print('typvar='      , typvar)
            print('etiquette='   , etiquette)

    else:
        #there is at least one good entry

        #get meta for this entry
        nz = 1
        ref_meta = rmn.fstprm(key_dict['key'])
        (rp1, rp2, rp3) = rmn.DecodeIp(ref_meta['ip1'],ref_meta['ip2'],ref_meta['ip3'])
        #get grid
        try:
            grid     = rmn.readGrid(iunit, ref_meta)
        except:
            warnings.warn('rmn.readGrid encountered a problem, setting grid to None')
            grid = None
        #get vgrid
        try:
            toctoc   = rmn.fstlir(iunit,nomvar='!!',ip1=ref_meta['ig1'],ip2=ref_meta['ig2'])
        except:
            warnings.warn('No !! entry found in file, setting toctoc to None')
            toctoc = None

        if meta_only :
            rmn.fstcloseall(iunit)
            return {'meta':ref_meta,'grid':grid,'toctoc':toctoc}

        if ip1 is None :
            #ip1 keyword not provided
            #try to find matching entries for 3D field
            #with same meta but different ip1

            #save ip1, and key for later
            key_list = [key_dict['key']]
            ip1_list = [ref_meta['ip1']]
            lev_list = [rp1.v1]

            key_dict, keep_this_one = _my_fstinfx(key_dict, iunit, datev=ref_meta['datev'], etiket=ref_meta['etiket'],
                                                  ip1=None, ip2=ref_meta['ip2'], ip3=ref_meta['ip3'],
                                                  ig1=ref_meta['ig1'], ig2=ref_meta['ig2'], ig3=ref_meta['ig3'],
                                                  typvar=ref_meta['typvar'], nomvar=ref_meta['nomvar'])

            while (key_dict is not None) :

                if keep_this_one :
                    #we have a valid entry save info for later
                    nz += 1
                    meta = rmn.fstprm(key_dict['key'])
                    (rp1, rp2, rp3) = rmn.DecodeIp(meta['ip1'],meta['ip2'],meta['ip3'])
                    #save ip1, and key for later
                    key_list.append(key_dict['key'])
                    ip1_list.append(meta['ip1'])
                    lev_list.append(rp1.v1)

                #check if there are entries with same meta but different ip1
                key_dict, keep_this_one = _my_fstinfx(key_dict, iunit, datev=ref_meta['datev'], etiket=ref_meta['etiket'],
                                                      ip1=None,            ip2=ref_meta['ip2'], ip3=ref_meta['ip3'],
                                                      ig1=ref_meta['ig1'], ig2=ref_meta['ig2'], ig3=ref_meta['ig3'],
                                                      typvar=ref_meta['typvar'], nomvar=ref_meta['nomvar'])
        elif type(ip1) is list :
            nz = 0
            key_list = []
            ip1_list = []
            lev_list = []
            for myip1 in ip1:
                #check if there are entries with same meta 
                key_dict = _my_fstinf(iunit, datev=ref_meta['datev'], etiket=ref_meta['etiket'],
                                      ip1=myip1,           ip2=ref_meta['ip2'], ip3=ref_meta['ip3'],
                                      ig1=ref_meta['ig1'], ig2=ref_meta['ig2'], ig3=ref_meta['ig3'],
                                      typvar=ref_meta['typvar'], nomvar=ref_meta['nomvar'])

                if key_dict is not None :
                    #we have a valid entry save info for later
                    nz += 1
                    meta = rmn.fstprm(key_dict['key'])
                    (rp1, rp2, rp3) = rmn.DecodeIp(meta['ip1'],meta['ip2'],meta['ip3'])
                    #save ip1, and key for later
                    key_list.append(key_dict['key'])
                    ip1_list.append(meta['ip1'])
                    lev_list.append(rp1.v1)
                else:
                    raise ValueError('No entries in fst file with ip1: '+str(myip1))

    #read data 
    if nz == 0 :
        return None
    else:

        #desired output to numpy
        key_arr = np.array(key_list)
        ip1_arr = np.array(ip1_list)
        lev_arr = np.array(lev_list)

        #sorted unique indices
        dum, inds = np.unique(lev_arr, return_index=True)
        #reverse order      hyb=1. is the lowest level
        rev_inds = np.flip(inds)

        #raise error if there are non-unique levels represented
        if ip1_arr.shape != rev_inds.shape:
            warnings.warn('Found more than one entry in fst file with same meta; this may or may not be bad... ; adjusting nz')
            nz = len(rev_inds)

        #sorted arrays
        key_arr = key_arr[rev_inds]
        ip1_arr = ip1_arr[rev_inds]
        lev_arr = lev_arr[rev_inds]

        #read output
        shape =  (ref_meta['shape'][0],ref_meta['shape'][1],nz)
        values = np.zeros(shape, order='F', dtype='float32')
        for kk in range(nz):
            dum = rmn.fstluk(key_arr[kk].item())
            values[:,:,kk] = dum['d']

    # Close file
    rmn.fstcloseall(iunit)
    return {'values':np.squeeze(values), 
            'meta':ref_meta,
            'grid':grid,
            'toctoc':toctoc,
            'ip1_list':ip1_arr.tolist(),
            'lev_list':lev_arr.tolist()}

#end _get_var---------------------------


def _my_fstinf(iunit, datev=None, etiket=None,
               ip1=None, ip2=None, ip3=None,
               ig1=None, ig2=None, ig3=None,
               typvar=None, nomvar=None):
    """
    Wrapper for fstinf that allow :
        - parameters to have the None value
        - filtering with the IGs
    """
    import rpnpy.librmn.all as rmn

    #defaults for fstinf
    if datev        is None : datev=-1
    if ip1          is None : ip1=-1
    if ip2          is None : ip2=-1
    if ip3          is None : ip3=-1
    if typvar       is None : typvar=' '
    if etiket       is None : etiket=' '

    key_dict = rmn.fstinf(iunit, datev=datev, etiket=etiket,
                          ip1=ip1, ip2=ip2, ip3=ip3,
                          typvar=typvar, nomvar=nomvar)

    if (key_dict is not None) and ( (ig1 is not None) or (ig2 is not None) or (ig3 is not None) ) :

        #get meta
        meta = rmn.fstprm(key_dict['key'])

        #extra filtering of the IGs
        #   key is set to None if no match
        if ig1 is not None:
            if ig1 != meta['ig1']:
                key_dict = None
        if ig2 is not None:
            if ig2 != meta['ig2']:
                key_dict = None
        if ig3 is not None:
            if ig3 != meta['ig3']:
                key_dict = None

    return key_dict


def _my_fstinfx(key, iunit, datev=None, etiket=None,
                ip1=None, ip2=None, ip3=None,
                ig1=None, ig2=None, ig3=None,
                typvar=None, nomvar=None):
    """
    Wrapper for fstinfx that allow :
        - parameters to have the None value
        - filtering with the IGs

    Returns
    key         as usual
    keep_this_one   a flag to indicate that a match was not found with the provided IGs
    """
    import rpnpy.librmn.all as rmn

    #defaults for fstinfx
    if datev        is None : datev=-1
    if ip1          is None : ip1=-1
    if ip2          is None : ip2=-1
    if ip3          is None : ip3=-1
    if typvar       is None : typvar=' '
    if etiket       is None : etiket=' '

    keep_this_one=True
    key_dict = rmn.fstinfx(key, iunit, datev=datev, etiket=etiket,
                           ip1=ip1, ip2=ip2, ip3=ip3,
                           typvar=typvar, nomvar=nomvar)

    if (key_dict is not None) and ( (ig1 is not None) or (ig2 is not None) or (ig3 is not None) ) :

        #get meta
        meta = rmn.fstprm(key_dict['key'])

        #extra filtering of the IGs
        #   key is set to None if no match
        if ig1 is not None:
            if ig1 != meta['ig1']:
                keep_this_one=False
        if ig2 is not None:
            if ig2 != meta['ig2']:
                keep_this_one=False
        if ig3 is not None:
            if ig3 != meta['ig3']:
                keep_this_one=False

    return key_dict, keep_this_one

if __name__ == '__main__' :
    #when called as main run tests
    import rpnpy.librmn.all as rmn
    import doctest
    rmn.fstopt(rmn.FSTOP_MSGLVL, rmn.FSTOPI_MSG_ERROR)
    doctest.testmod()

else :
    import rpnpy.librmn.all as rmn

    #less verbose outputs on import
    #   this is not a great option but it will only print
    #    "c_fstopi option MSGLVL set to 6"
    #   once
    rmn.fstopt(rmn.FSTOP_MSGLVL, rmn.FSTOPI_MSG_ERROR)



