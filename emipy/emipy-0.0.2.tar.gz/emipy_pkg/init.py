# -*- coding: utf-8 -*-
"""
Created on Tue May  5 13:23:02 2020

@author: f-ove

script to try and use functions
"""
import time 
startTime = time.time()


import pandas as pd
import os
import numpy as np
import rawdata
# from .rawdata import pickle_rawdata
# from .rawdata import merge_frompickle


"""
for testing pickle and merge function
"""
# rawdata.pickle_rawdata(force_rerun=True)
# rawdata.merge_frompickle(force_rerun=True)


"""
load complete data
"""
data = rawdata.read_db()


"""
take a view at possible filter options
"""
# countrylist = rawdata.get_Countrylist()
# yearlist = rawdata.get_Yearlist()
# pollutantlist = rawdata.get_Pollutantlist()
# NACElist = rawdata.get_NACECode_filter_list()


"""
declaring filter
"""
# countryfilter = ['Germany','Spain','Belgium']
# yearfilter = [2016]
# mediumfilter = ['Air','Water']
pollutantfilter = ['Carbon dioxide (CO2)']
# NACEfilter = rawdata.get_NACECode_filter(group='chem')


"""
load data, with selected filters from above
"""
CO2 = rawdata.f_db(db=data,CountryName='Germany',PollutantName=pollutantfilter)
# CO2 = rawdata.f_db(nc=NACEfilter)


"""
get pollutant volume for chosen filters(all wanted filters have to be named in the input)
"""
# CO2 = rawdata.get_PollutantVolume(PollutantName=pollutantfilter,Table=False)
# CO2 = rawdata.get_PollutantVolume(PollutantName=pollutantfilter)


"""
plot pollutant volume for chosen filters(all wanted filters have to be named in the input)
"""
# rawdata.plot_PollutantVolume(CountryName=countryfilter,PollutantName=pollutantfilter,form=1)
# rawdata.plot_PollutantVolume(CountryName=countryfilter,PollutantName=pollutantfilter,ReportingYear=yearfilter,form=2)
# rawdata.plot_PollutantVolume(CountryName=countryfilter,PollutantName=pollutantfilter,ReportingYear=yearfilter,form=3)


print('The script took {0} second !'.format(time.time() - startTime))
