# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 11:32:51 2022

@author: Administrator
"""

import os
os.chdir("D:\\Study\\Marko Mine\\Concentration")

# Importing the libraries
#import numpy as np
import pandas as pd
import datetime as dt

station = 'EVO_HC1'#'FRO_KC1' OR 'FRO_HC1' OR 'EVO_HC1'
species = 'NO3'#'NO3' OR 'Se' OR 'SO4'

#load predict data
flowrate = pd.read_csv('.\\SF_flow_pred\\pred_whole_1980-2020_'+station+'_4Input.csv')
flowrate.columns = ['Date', 'flow']
flowrate['Datetime'] = pd.to_datetime(flowrate['Date'], format='%Y/%m/%d')
flowrate.drop('Date', 1, inplace=True)

concentration = pd.read_csv('pred_whole_'+species+'_conc_'+station+'_5Input.csv', header=None)
concentration.columns = ['Date', 'conc']
concentration['Datetime'] = pd.to_datetime(concentration['Date'], format='%Y/%m/%d')
concentration.drop('Date', 1, inplace=True)

# =============================================================================
# Accumulated by month
# =============================================================================
startDate = min(flowrate['Datetime'][0],concentration['Datetime'][0])#check every time
endDate = max(flowrate['Datetime'][len(flowrate)-1],concentration['Datetime'][len(concentration)-1])

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

#flow
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

#conc
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
            load.loc[i, 'load'] =  flow_avg.loc[i, 'avg_flow']*conc_avg.loc[j, 'avg_conc']#unit of load: grams/sec
            load.loc[i, 'month'] = flow_avg.loc[i, 'month']
            load.loc[i, 'year'] = flow_avg.loc[i, 'year']
            load.loc[i, 'Datetime'] = dt.date(int(flow_avg.loc[i, 'year']),int(flow_avg.loc[i, 'month']),15)
load.index = range(0,len(load))

for i in range(0, len(load)):
    if load.loc[i, 'month']==1 or load.loc[i, 'month']==3 or load.loc[i, 'month']==5 or load.loc[i, 'month']==7 or load.loc[i, 'month']==8 or load.loc[i, 'month']==10 or load.loc[i, 'month']==12:
        load.loc[i, 'load'] = load.loc[i, 'load']*60*60*24*31/1000#unit of loading: kg/month
    elif load.loc[i, 'month']==2:
        load.loc[i, 'load'] = load.loc[i, 'load']*60*60*24*28.25/1000
    else:
        load.loc[i, 'load'] = load.loc[i, 'load']*60*60*24*30/1000

# =============================================================================
# Accumulated by day
# =============================================================================
merge = pd.merge(flowrate, concentration, on=('Datetime'))

startDate = merge['Datetime'][0]
endDate = merge['Datetime'][len(merge)-1]

merge['flux'] = merge['flow']*merge['conc']
merge.dropna(inplace=True)

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

#flux
merge = pd.merge(datetime, merge, on=('Datetime'), how='left')
flux_deNaN = merge.loc[:, ['Datetime','month','year','flux']].dropna()
flux_deNaN.index = range(0,len(flux_deNaN))

n = 1
flux_avg = pd.DataFrame()
flux_acc = flux_deNaN.loc[0,'flux']
for i in range(0, len(flux_deNaN)-1):
    if flux_deNaN.loc[i,'year']==flux_deNaN.loc[i+1,'year'] and flux_deNaN.loc[i,'month']==flux_deNaN.loc[i+1,'month']:
        flux_acc = flux_acc + flux_deNaN.loc[i+1,'flux']
        n = n + 1
    else:
        flux_avg.loc[i, 'avg_flux'] = flux_acc/n
        flux_avg.loc[i, 'year'] = flux_deNaN.loc[i,'year']
        flux_avg.loc[i, 'month'] = flux_deNaN.loc[i,'month']
        flux_avg.loc[i, 'Datetime'] = flux_deNaN.loc[i,'Datetime']
        flux_acc = flux_deNaN.loc[i+1, 'flux']
        n = 1
flux_avg.loc[i, 'avg_flux'] = flux_acc/n
flux_avg.loc[i, 'year'] = flux_deNaN.loc[i,'year']
flux_avg.loc[i, 'month'] = flux_deNaN.loc[i,'month']
flux_avg.loc[i, 'Datetime'] = flux_deNaN.loc[i,'Datetime']
flux_avg.index = range(0,len(flux_avg))

load = pd.DataFrame(flux_avg)
for i in range(0, len(load)):
    load.loc[i, 'Datetime'] = dt.date(int(load.loc[i, 'year']),int(load.loc[i, 'month']),15)
    if load.loc[i, 'month']==1 or load.loc[i, 'month']==3 or load.loc[i, 'month']==5 or load.loc[i, 'month']==7 or load.loc[i, 'month']==8 or load.loc[i, 'month']==10 or load.loc[i, 'month']==12:
        load.loc[i, 'load'] = load.loc[i, 'avg_flux']*60*60*24*31/1000#unit of loading: kg/month
    elif load.loc[i, 'month']==2:
        load.loc[i, 'load'] = load.loc[i, 'avg_flux']*60*60*24*28.25/1000
    else:
        load.loc[i, 'load'] = load.loc[i, 'avg_flux']*60*60*24*30/1000

# =============================================================================
# Daily Load
# =============================================================================
merge = pd.merge(flowrate, concentration, on=('Datetime'))

startDate = merge['Datetime'][0]
endDate = merge['Datetime'][len(merge)-1]

merge['flux'] = merge['flow']*merge['conc']
merge['daily_load'] = merge['flux']*60*60*24/1000
merge.dropna(inplace=True)
