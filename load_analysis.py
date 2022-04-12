# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 09:09:16 2022

@author: Administrator
"""

import os
os.chdir("D:\\Study\\Marko Mine\\Flowrate")

#import numpy as np
import pandas as pd
import datetime as dt

station = 'FRO_KC1'#'FRO_KC1' OR 'FRO_HC1' OR 'EVO_HC1'
species = 'Se'#'NO3' OR 'Se' OR 'SO4'
outlier_conc = 300#For Se only: 100 for EVO_HC1, 300 and 50 for FRO_KC1 and FRO_HC1
outlier_flow = 8#8 for FRO_KC1, 15 and 8 for FRO_HC1 and EVO_HC1

startDate = '1981-01-01'#check every time
endDate = '2013-12-31'

datetime = pd.date_range(start=startDate, end=endDate, freq='D')
datetime = pd.DataFrame(datetime, columns=['Datetime'])

year = []
month = []
for i in range(0, len(datetime)):
    m = datetime['Datetime'][i].month
    y = datetime['Datetime'][i].year
    month.append(m)
    year.append(y)

datetime['month']=month
datetime['year']=year

#choose weather the flowrate data should be averaged or not
flowrate = pd.read_csv(station+'_.csv', usecols=[2, 3])
flowrate.columns = ['sample_date', 'flow']
# Converting date string to datetime
flowrate['Datetime'] = pd.to_datetime(flowrate['sample_date'], format='%Y/%m/%d')
flowrate = flowrate.drop('sample_date', 1)
#print(flowrate.describe())

os.chdir("D:\\Study\\Marko Mine\\Concentration")
#target
concentration = pd.read_csv('.\\conc_data_csv\\'+station+'_'+species+'.csv')#conc. in unit of mg/L
concentration.columns = ['sample_date', 'conc']
concentration['Datetime'] = pd.to_datetime(concentration['sample_date'], format='%Y/%m/%d')
concentration.drop('sample_date', 1, inplace=True)

#deleting outliers
for i in range(0, len(concentration)):
    if concentration['conc'][i] > outlier_conc:
        concentration.drop(i, 0, inplace=True)

for i in range(0, len(flowrate)):
    if flowrate['flow'][i] > outlier_flow:
        flowrate.drop(i, 0, inplace=True)

# =============================================================================
# Monthly load
# =============================================================================
merge = pd.merge(datetime, flowrate, on=('Datetime'), how='left')
flow_deNaN = merge.loc[:, ['Datetime','month','year','flow']].dropna()
flow_deNaN.index = range(0,len(flow_deNaN))

n = 1
flow_avg = pd.DataFrame()
flow_acc = flow_deNaN.loc[0,'flow']
for i in range(0, len(flow_deNaN)-1):
    if flow_deNaN.loc[i,'year']==flow_deNaN.loc[i+1,'year'] and flow_deNaN.loc[i,'month']==flow_deNaN.loc[i+1,'month']:
        flow_acc = flow_acc + flow_deNaN.loc[i+1,'flow']
        n = n + 1
    else:
        flow_avg.loc[i, 'avg_flow'] = flow_acc/n
        flow_avg.loc[i, 'year'] = flow_deNaN.loc[i,'year']
        flow_avg.loc[i, 'month'] = flow_deNaN.loc[i,'month']
        #flow_avg.loc[i, 'Datetime'] = flow_deNaN.loc[i,'Datetime']
        flow_acc = flow_deNaN.loc[i+1, 'flow']
        n = 1
flow_avg.loc[i, 'avg_flow'] = flow_acc/n
flow_avg.loc[i, 'year'] = flow_deNaN.loc[i,'year']
flow_avg.loc[i, 'month'] = flow_deNaN.loc[i,'month']
#flow_avg.loc[i, 'Datetime'] = flow_deNaN.loc[i,'Datetime']
flow_avg.index = range(0,len(flow_avg))

merge = pd.merge(datetime, concentration, on=('Datetime'), how='left')
conc_deNaN = merge.loc[:, ['Datetime','month','year','conc']].dropna()
conc_deNaN.index = range(0,len(conc_deNaN))

n = 1
conc_avg = pd.DataFrame()
conc_acc = conc_deNaN.loc[0,'conc']
for i in range(0, len(conc_deNaN)-1):
    if conc_deNaN.loc[i,'year']==conc_deNaN.loc[i+1,'year'] and conc_deNaN.loc[i,'month']==conc_deNaN.loc[i+1,'month']:
        conc_acc = conc_acc + conc_deNaN.loc[i+1,'conc']
        n = n + 1
    else:
        conc_avg.loc[i, 'avg_conc'] = conc_acc/n
        conc_avg.loc[i, 'year'] = conc_deNaN.loc[i,'year']
        conc_avg.loc[i, 'month'] = conc_deNaN.loc[i,'month']
        #conc_avg.loc[i, 'Datetime'] = conc_deNaN.loc[i,'Datetime']
        conc_acc = conc_deNaN.loc[i+1, 'conc']
        n = 1
conc_avg.loc[i, 'avg_conc'] = conc_acc/n
conc_avg.loc[i, 'year'] = conc_deNaN.loc[i,'year']
conc_avg.loc[i, 'month'] = conc_deNaN.loc[i,'month']
#conc_avg.loc[i, 'Datetime'] = conc_deNaN.loc[i,'Datetime']
conc_avg.index = range(0,len(conc_avg))

load = pd.DataFrame()
for i in range(0, len(flow_avg)):
    for j in range(0, len(conc_avg)):
        if flow_avg.loc[i, 'month']==conc_avg.loc[j, 'month'] and flow_avg.loc[i, 'year']==conc_avg.loc[j, 'year']:
            load.loc[i, 'flux'] =  flow_avg.loc[i, 'avg_flow']*conc_avg.loc[j, 'avg_conc']#unit of load: grams/sec
            load.loc[i, 'month'] = flow_avg.loc[i, 'month']
            load.loc[i, 'year'] = flow_avg.loc[i, 'year']
            load.loc[i, 'Datetime'] = dt.date(int(flow_avg.loc[i, 'year']),int(flow_avg.loc[i, 'month']),15)
load.index = range(0,len(load))


for i in range(0, len(load)):
    if load.loc[i, 'month']==1 or load.loc[i, 'month']==3 or load.loc[i, 'month']==5 or load.loc[i, 'month']==7 or load.loc[i, 'month']==8 or load.loc[i, 'month']==10 or load.loc[i, 'month']==12:
        load.loc[i, 'load'] = load.loc[i, 'flux']*60*60*24*31/1000#unit of loading: kg/month
    elif load.loc[i, 'month']==2:
        load.loc[i, 'load'] = load.loc[i, 'flux']*60*60*24*28.25/1000
    else:
        load.loc[i, 'load'] = load.loc[i, 'flux']*60*60*24*30/1000
#load is the target

# =============================================================================
# Daily load
# =============================================================================
merge = pd.merge(flowrate, concentration, on=('Datetime'))

startDate = merge['Datetime'][0]
endDate = merge['Datetime'][len(merge)-1]

merge['flux'] = merge['flow']*merge['conc']
merge['daily_load'] = merge['flux']*60*60*24/1000
merge.dropna(inplace=True)
#merge is the target
