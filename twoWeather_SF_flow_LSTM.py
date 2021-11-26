# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 17:44:43 2021

@author: Administrator
"""

import os
os.chdir("D:\\Study\\Marko Mine\\Concentration")

# Importing the libraries
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

# =============================================================================
# Choosing parameters
# =============================================================================
station = 'FRO_KC1'#'FRO_KC1' OR 'FRO_HC1' OR 'EVO_HC1'
species = 'NO3'#'NO3' OR 'Se' OR 'SO4'

avg_days = 6#average days for LSTM input
time_step = 10
gap_days = 0#No. of days between the last day of input and the predict date
seed = 99#seed gave the best prediction result for FRO KC1 station, keep it

train_startDate = '1980-01-01'
test_startDate = '2013-01-01'
endDate = '2013-12-31'



# =============================================================================
# Loading datasets
# =============================================================================
#2 choose 1
weather = pd.read_csv('.\\Weather\\weather_1980-2020_avg_'+str(avg_days)+'.csv')#with Nulls
#weather = pd.read_csv('.\\Weather\\Weather_long_filled_avg_'+str(avg_days)+'.csv')#Null-filled

weather['Datetime'] = pd.to_datetime(weather['Date/Time'], format='%Y/%m/%d')
weather.drop('Date/Time', 1, inplace=True)

SF_output = pd.read_csv('.\\SF_flow_pred\\pred_SF_whole_1980-2020_'+station+'.csv')
SF_output.columns = ['Date', 'Output_SF']
SF_output['Datetime'] = pd.to_datetime(SF_output['Date'], format='%Y/%m/%d')
SF_output.drop('Date', 1, inplace=True)

flowrate = pd.read_csv('.\\SF_flow_pred\\pred_whole_1980-2020_'+station+'_4Input.csv')
flowrate.columns = ['Date', 'flowrate']
flowrate['Datetime'] = pd.to_datetime(flowrate['Date'], format='%Y/%m/%d')
flowrate.drop('Date', 1, inplace=True)

#Target
concentration = pd.read_csv('.\\conc_data_csv\\'+station+'_'+species+'.csv')
concentration.columns = ['sample_date', 'conc']
concentration['Datetime'] = pd.to_datetime(concentration['sample_date'], format='%Y/%m/%d')
concentration.drop('sample_date', 1, inplace=True)

#merge
merge = pd.merge(weather, flowrate, on=('Datetime'), how='left')
merge = pd.merge(merge, SF_output, on=('Datetime'), how='left')
merge = pd.merge(merge, concentration, on=('Datetime'), how='left')
merge = np.array(merge)




