# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:57:50 2022

@author: Administrator
"""

import os
os.chdir("D:\\Study\\Marko Mine\\Concentration")

import pandas as pd
import numpy as np
#import datetime as dt

from scipy.interpolate import interp1d

station = 'FRO_KC1'#'FRO_KC1' OR 'FRO_HC1' OR 'EVO_HC1'
species = 'Se'#'NO3' OR 'Se' OR 'SO4'

load_pred = pd.read_csv('.\\loading_data\\'+species+'\\'+station+'_pred.csv').dropna()#loading in unit of kg for NO3, g for Se
load_real = pd.read_csv('.\\loading_data\\'+species+'\\'+station+'_real.csv').dropna()#loading in unit of kg for NO3, g for Se

load_pred['Datetime'] = pd.to_datetime(load_pred['Datetime'], format='%Y/%m/%d')
load_real['Datetime'] = pd.to_datetime(load_real['Datetime'], format='%Y/%m/%d')

#choose the start and end year of annual loading calculation
start_year = max(load_pred['Datetime'][0], load_real['Datetime'][0]).year+1
#end_year = min(load_pred['Datetime'][len(load_pred)-1], load_real['Datetime'][len(load_real)-1]).year-1
#start_year = 1980
end_year = 2019

#the first and last year may not be complete, close interval
delta_year = end_year-start_year+1
print('Total number of annual loading:', delta_year)

#convert the date to int numbers
def timestampToNum(series_time):
    num_date = []
    for i in range (0, len(series_time)):
        num_date.append(int(series_time[i].timestamp()))
    num_date = np.array(num_date)
    return num_date

#extract the number of the year of the time series
def timestampToYear(series_time):
    num_year = []
    for i in range (0, len(series_time)):
        num_year.append(int(series_time[i].year))
    num_year = np.array(num_year)
    return num_year

f_pred = interp1d(timestampToNum(load_pred['Datetime']), load_pred['daily_load'])

#generate continuous date from the start year to the end year (both included)
date_series = pd.date_range(start=str(start_year)+"-01-01",end=str(end_year)+"-12-31").to_pydatetime().tolist()

load_pred_con = f_pred(timestampToNum(date_series))

loading = pd.DataFrame()
loading['date'] = date_series
loading['year'] = timestampToYear(date_series)
loading['load_pred_con'] = load_pred_con

#annual_load is the target of this script
annual_load = pd.DataFrame()
annual_load['Annual_load_pred'] = loading.groupby('year')['load_pred_con'].sum()#loading in unit of kg, Se loading in unit of g
#annual_load['year'] = annual_load.index

# =============================================================================
# Real annual loading calculation
# =============================================================================
end_year = min(load_pred['Datetime'][len(load_pred)-1], load_real['Datetime'][len(load_real)-1]).year-1
date_series = pd.date_range(start=str(start_year)+"-01-01",end=str(end_year)+"-12-31").to_pydatetime().tolist()
f_real = interp1d(timestampToNum(load_real['Datetime']), load_real['daily_load'])
load_real_con = f_real(timestampToNum(date_series))

loading = pd.DataFrame()
loading['date'] = date_series
loading['year'] = timestampToYear(date_series)

loading['load_real_con'] = load_real_con
annual_load['Annual_load_real'] = loading.groupby('year')['load_real_con'].sum()#NO3 loading in unit of kg, Se loading in unit of g
