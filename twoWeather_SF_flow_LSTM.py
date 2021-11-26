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

from sklearn.preprocessing import MinMaxScaler

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

#Choose weather the flowrate data should be averaged or not
flowrate = pd.read_csv('.\\SF_flow_pred\\pred_whole_1980-2020_'+station+'_4Input.csv')
flowrate.columns = ['Date', 'flowrate']
flowrate['Datetime'] = pd.to_datetime(flowrate['Date'], format='%Y/%m/%d')
flowrate.drop('Date', 1, inplace=True)

#Target
concentration = pd.read_csv('.\\conc_data_csv\\'+station+'_'+species+'.csv')
concentration.columns = ['sample_date', 'conc']
concentration['Datetime'] = pd.to_datetime(concentration['sample_date'], format='%Y/%m/%d')
concentration.drop('sample_date', 1, inplace=True)

# =============================================================================
# Pre-processing
# =============================================================================
#merge
merge = pd.merge(weather, flowrate, on=('Datetime'), how='left')
merge = pd.merge(merge, SF_output, on=('Datetime'), how='left')
merge = pd.merge(merge, concentration, on=('Datetime'), how='left')
merge = np.array(merge)
merge = pd.DataFrame(merge, index=merge[:, 8])

#train/test separation
test = merge.loc[test_startDate : endDate].drop(8,1).drop(2,1).values#drop date and datetime columns
train = merge.loc[train_startDate : test_startDate].drop(8,1).drop(2,1).values#Changed

#feature selection
train = np.c_[train[:, 0], train[:, 2], train[:, 5], train[:, 7:]]#year, temp, precip, flow, SF, conc
test = np.c_[test[:, 0], test[:, 2], test[:, 5], test[:, 7:]]

datetime_test = merge.loc[test_startDate : endDate].index[:].strftime('%Y-%m-%d')
datetime_train = merge.loc[train_startDate : test_startDate].index[:].strftime('%Y-%m-%d')

#scaling
scaler = MinMaxScaler(feature_range=(0, 1), copy=True)
scaled_train = scaler.fit_transform(train)
scaled_test = scaler.transform(test)

scaled = np.r_[scaled_train, scaled_test]
original = np.r_[train, test]
datetime = np.r_[datetime_train, datetime_test]

#construct 3-D input matrix
print('Below are results for time_step:', time_step)
X_scaled, y_scaled, y_not_scaled= [], [], []
datetime_deNull = []#target deNull

for i in range(time_step, len(scaled)):
    if scaled[i][-1]>=0:
        sample_input = []
        for j in range(0, time_step):
            sample_input.append(scaled[i-gap_days-(time_step-1-j)*avg_days, :-1])
        X_scaled.append(sample_input)
        y_scaled.append(scaled[i, -1])
        y_not_scaled.append(original[i, -1])
        datetime_deNull.append(datetime[i])
X_scaled, y_scaled, y_not_scaled = np.array(X_scaled), np.array(y_scaled), np.array(y_not_scaled)
datetime_deNull = np.array(datetime_deNull)

test_size = len(pd.DataFrame(test).dropna())#Number of valid test size

X_train = X_scaled[:len(X_scaled)+1-test_size, :, :]
y_train = y_scaled[:len(X_scaled)+1-test_size]
y_train_not_scaled = y_not_scaled[:len(X_scaled)+1-test_size]
train_datetime = datetime_deNull[:len(X_scaled)+1-test_size]

X_test = X_scaled[len(X_scaled)+1-test_size:, :, :]
y_test = y_scaled[len(X_scaled)+1-test_size:]
y_test_not_scaled = y_not_scaled[len(X_scaled)+1-test_size:]
test_datetime = datetime_deNull[len(X_scaled)+1-test_size:]

# Deleting NaNs in samples







