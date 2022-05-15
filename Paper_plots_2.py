# -*- coding: utf-8 -*-
"""
Created on Fri May  6 11:44:14 2022

@author: Administrator
"""

import os
os.chdir("D:\\Study\\Marko Mine\\Concentration")

# Importing the libraries
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import DateFormatter, YearLocator

station = 'EVO_HC1'
species = 'Se'#'NO3' OR 'Se' 
regression = pd.read_csv('./Visualization/Data/'+station+'_'+species+'_Data.csv')
#threshold = 1.2#1.2, 1.7, and 0.7 for FRO_KC1, FRO_HC1, and EVO_HC1
waste_rock_vol = pd.read_csv('./Visualization/Data/waste_rock_volume.csv')

fontdict_exmt = {'size':12, 'color':'r', 'family':'Times New Roman'}
fontdict_ctrl = {'size':12, 'color':'g', 'family':'Times New Roman'}
titlefontdic = {'size':16, 'color':'k', 'family':'Times New Roman'}
text_font = {'size':'22', 'color':'black', 'weight':'bold', 'family':'Times New Roman'}
font1={'family': 'Times New Roman', 'weight': 'light', 'size': 14}
font2={'family': 'Times New Roman', 'weight': 'light', 'size': 18}

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# =============================================================================
# Scatter plot with line
# =============================================================================
x1 = list(regression['Date'])
x1 = [datetime.datetime.strptime(d, '%Y/%m/%d').date() for d in x1]
y1 = list(regression['Real'])
y2 = list(regression['Pred'])

fig, ax = plt.subplots(figsize=(18,5), dpi=300)
plt.rcParams['axes.unicode_minus'] = False#使用上标小标小一字号
plt.rcParams['font.sans-serif']=['Times New Roman']
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
#plt.rcParams['font.sans-serif']=['SimHei']
#wight为字体的粗细，可选 ‘normal\bold\light’等
#size为字体大小
#plt.title(station,fontdict=font2, pad=14)#Title
plt.scatter(x1, y1, edgecolors=None, c='magenta', s=15, marker='s', label='Measured')#red/green for NO3, magenta/blue for Se
plt.plot(x1, y2,'b-', lw=2.0, label="Model Output")#Line
plt.axvline(x=datetime.date(2013,1,1), ls='--', c='black', lw=1.0)
plt.ylabel('Selenium Concentration (μg/L)',fontdict=font2)#$\mathregular{min^{-1}}$label的格式,^{-1}为上标
plt.xlabel('Time',fontdict=font2)
plt.legend(loc="upper left",scatterpoints=1,prop=font1,shadow=True,frameon=False)#添加图例,
ax.set_xlim(datetime.date(2003,1,1), datetime.date(2014,1,1))
ax.set_ylim(0.0, 300.0)#NO3: 140, 12, 6 for station 1 2 and 3; Se: 300, 50, 50
# Major ticks every 12 months.
fmt_whole_year = YearLocator(1, month=1, day=1)
ax.xaxis.set_major_locator(fmt_whole_year)
date_form = DateFormatter("%Y")#only display year here, capital means 4 digits
ax.xaxis.set_major_formatter(date_form)
#plt.xticks(rotation = 45)
#ax.set_xticks(np.arange(datetime.date(1992,1,1), datetime.date(2014,1,2), step=datetime.timedelta(days=365.25)))
#plt.xticks(np.arange(datetime.date(1992,1,1), datetime.date(2014,1,2), step=datetime.timedelta(days=365.25)), rotation=45)
#ax.set_yticks(np.arange(datetime.date(1992,1,1), datetime.date(2014,1,1), step=365))
plt.text(0.48, 0.94, 'Train', fontdict=font2, transform = ax.transAxes)
plt.text(0.95, 0.94, 'Test', fontdict=font2, transform = ax.transAxes)#x=0.95, 0.97 for NO3 station 3

#plt.text(0.91, 0.92, '(a)', fontdict=text_font, transform = ax.transAxes)
#plt.text(0.91, 0.92, '(b)', fontdict=text_font, transform = ax.transAxes)
plt.text(0.82, 0.94, 'Station 1', fontdict=font2, transform = ax.transAxes)
plt.show()

# =============================================================================
# Bar chat with line
# =============================================================================
#plotting_1
daily_load = pd.read_csv('./Visualization/Data/daily_loading_'+station+'_'+species+'_Data.csv')#unit: kg for NO3, g for Se
annual_load = pd.read_csv('./Visualization/Data/annual_loading_'+station+'_'+species+'_Data.csv')#unit: kg for NO3, g for Se
#annual_load_real = pd.read_csv('./Visualization/Data/annual_loading_real_'+station+'_'+species+'_Data.csv')
annual_load.dropna(inplace=True)

daily_load['Datetime'] = pd.to_datetime(daily_load['Datetime'], format='%Y/%m/%d')
daily_load.index = daily_load['Datetime']
annual_load['Datetime'] = [datetime.date(int(year), 6, 15) for year in annual_load['year']]
annual_load['Datetime'] = pd.to_datetime(annual_load['Datetime'], format='%Y/%m/%d')
annual_load.index = annual_load['Datetime']
#annual_load_real['Datetime'] = [datetime.date(int(year), 6, 15) for year in annual_load_real['year']]

#start_date = str(int(annual_load['year'][0]))+'-01-01'
#end_date = str(int(annual_load['year'][len(annual_load)+1]))+'-12-31'
start_date = '2002-01-01'
end_date = '2020-01-01'

x1 = list(daily_load['Datetime'].loc[start_date : end_date])
y1 = list(daily_load['daily_load'].loc[start_date : end_date]/1000)#NO3 in the unit of tonne, Se in kg
x2 = list(annual_load['Datetime'].loc[start_date : end_date])
y2 = list(annual_load['Annual_load_pred'].loc[start_date : end_date]/1e6)#NO3 in the unit of thousand tonne, Se in tonne
#x3 = list(annual_load_real['Datetime'])
#y3 = list(annual_load_real['Annual_load_real']/1000)#NO3 in the unit of tonne, Se in kg

fig = plt.figure(figsize=(18,5), dpi=300)
plt.rcParams['axes.unicode_minus'] = False#使用上标小标小一字号
plt.rcParams['font.sans-serif']=['Times New Roman']
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
fmt_whole_year = YearLocator(1, month=1, day=1)
date_form = DateFormatter("%Y")#only display year here, capital means 4 digits

#annual loading
ax2 = fig.add_subplot(111)   #组合图必须加这个
plt.plot(x2, y2, '-o', markersize=10, lw=2.0, label="Annual Loading Prediction", color='magenta')#red/blue for NO3, magenta/green for Se
#plt.plot(x3, y3, '-s', markersize=10, lw=1.0, label="Annual Loading Estimation", color='orange')
plt.ylabel('Selenium Annual Loading (tonnes)',fontdict=font2)#$\mathregular{min^{-1}}$label的格式,^{-1}为上标
ax2.set_xlabel('Time',fontdict=font2)
#plt.xlabel('Time',fontdict=font2)
ax2.set_ylim(0.0, 1.0)#NO3: 140, 12, 6 for station 1 2 and 3; Se: 300, 50, 50
#plt.axvline(x=datetime.date(2013,1,1), ls='--', c='black', lw=1.0)
ax2.xaxis.set_major_locator(fmt_whole_year)
ax2.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper left',frameon=False,prop=font2)

#daily loading
ax1 = ax2.twinx()
ax1.bar(x = x1, height=y1, color='green', 
        label='Daily Loading Prediction')
ax1.set_ylabel('Selenium Daily Loading (kilograms)',fontdict=font2)#$\mathregular{min^{-1}}$label的格式,^{-1}为上标
#ax1.set_xlabel('Time',fontdict=font2)
ax1.set_xlim(datetime.datetime.strptime(start_date,'%Y-%m-%d'), datetime.datetime.strptime(end_date,'%Y-%m-%d'))
ax1.set_ylim(0.0, 10)#NO3: 140, 12, 6 for station 1 2 and 3; Se: 300, 50, 50
plt.legend(loc='upper right',frameon=False,prop=font2)

plt.text(0.45, 0.94, 'Station 3', fontdict=font2, transform = ax2.transAxes)

#ax.xaxis.set_major_locator(fmt_whole_year)
#ax.xaxis.set_major_formatter(date_form)
plt.show()

'''
daily_load['Datetime'] = pd.to_datetime(daily_load['Datetime'], format='%Y/%m/%d')
daily_load.index = daily_load['Datetime']
annual_load['Datetime'] = [datetime.date(int(year), 1, 1) for year in annual_load['year']]
annual_load_real['Datetime'] = [datetime.date(int(year), 1, 1) for year in annual_load_real['year']]

start_date = str(int(annual_load['year'][0]))+'-01-01'
end_date = str(int(annual_load['year'][len(annual_load)+1]))+'-12-31'

x1 = list(daily_load['Datetime'].loc[start_date : end_date])
y1 = list(daily_load['daily_load'].loc[start_date : end_date]/1000)#in the unit of tonne
x2 = list(annual_load['Datetime'])
y2 = list(annual_load['Annual_load_pred']/1000)#in the unit of tonne
x3 = list(annual_load_real['Datetime'])
y3 = list(annual_load_real['Annual_load_real']/1000)#in the unit of tonne

fig = plt.figure(figsize=(18,8), dpi=300)
plt.rcParams['axes.unicode_minus'] = False#使用上标小标小一字号
plt.rcParams['font.sans-serif']=['Times New Roman']
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
fmt_whole_year = YearLocator(1, month=1, day=1)
date_form = DateFormatter("%Y")#only display year here, capital means 4 digits

#daily loading
ax1 = fig.add_subplot(211)
ax1.bar(x = x1, height=y1, color='blue', 
        label='Daily Loading Prediction')
ax1.set_ylabel('Nitrate Daily Loading (tonne)',fontdict=font2)#$\mathregular{min^{-1}}$label的格式,^{-1}为上标
#ax1.set_xlabel('Time',fontdict=font2)
ax1.set_xlim(datetime.datetime.strptime(start_date,'%Y-%m-%d'), datetime.datetime.strptime(end_date,'%Y-%m-%d'))
ax1.set_ylim(0.0, 40.0)#NO3: 140, 12, 6 for station 1 2 and 3; Se: 300, 50, 50
plt.legend(loc='upper left',frameon=False,prop=font2)

#annual loading
ax2 = plt.subplot(212, sharex = ax1)   #组合图必须加这个
plt.plot(x2, y2, '-o', markersize=10, lw=1.0, label="Annual Loading Prediction", color='brown')
plt.plot(x3, y3, '-s', markersize=10, lw=1.0, label="Annual Loading Estimation", color='orange')
plt.ylabel('Nitrate Annual Loading (tonne)',fontdict=font2)#$\mathregular{min^{-1}}$label的格式,^{-1}为上标
ax2.set_xlabel('Time',fontdict=font2)
#plt.xlabel('Time',fontdict=font2)
ax2.set_ylim(0.0, 4000.0)#NO3: 140, 12, 6 for station 1 2 and 3; Se: 300, 50, 50
#plt.axvline(x=datetime.date(2013,1,1), ls='--', c='black', lw=1.0)
ax2.xaxis.set_major_locator(fmt_whole_year)
ax2.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper left',frameon=False,prop=font2)

plt.text(0.45, 2.1, 'Station 1', fontdict=font2, transform = ax2.transAxes)

#ax.xaxis.set_major_locator(fmt_whole_year)
#ax.xaxis.set_major_formatter(date_form)
plt.show()
'''

# =============================================================================
# Waste rock volume
# =============================================================================
x1 = list(waste_rock_vol['Date'])
x1 = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in x1]
y1 = list(waste_rock_vol['FRO_KC']/1e9)#unit: million m^3
y2 = list(waste_rock_vol['FRO_HC']/1e9)
y3 = list(waste_rock_vol['EVO_HC']/1e9)

fig, ax = plt.subplots(figsize=(12,5), dpi=300)
plt.rcParams['axes.unicode_minus'] = False#使用上标小标小一字号
plt.rcParams['font.sans-serif']=['Times New Roman']
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
#plt.rcParams['font.sans-serif']=['SimHei']
#wight为字体的粗细，可选 ‘normal\bold\light’等
#size为字体大小
#plt.title(station,fontdict=font2, pad=14)#Title
plt.plot(x1, y1,'b-', lw=2.0, label="Station 1")#Line
plt.plot(x1, y2,'r-', lw=2.0, label="Station 2")#Line
plt.plot(x1, y3,'g-', lw=2.0, label="Station 3")#Line
plt.axvline(x=datetime.date(2013,1,1), ls='--', c='black', lw=1.0)#past/future
plt.ylabel('Waste Rock Volume (billion $\mathregular{m^{3}}$)',fontdict=font2)#$\mathregular{min^{-1}}$label的格式,^{-1}为上标
plt.xlabel('Time',fontdict=font2)
plt.legend(loc="upper left",scatterpoints=1,prop=font1,shadow=True,frameon=False)#添加图例,
ax.set_xlim(datetime.date(1975,1,1), datetime.date(2035,1,1))
ax.set_ylim(0.0, 1.75)#NO3: 140, 12, 6 for station 1 2 and 3; Se: 300, 50, 50
# Major ticks every 12 months.
fmt_whole_year = YearLocator(5, month=1, day=1)
ax.xaxis.set_major_locator(fmt_whole_year)
date_form = DateFormatter("%Y")#only display year here, capital means 4 digits
ax.xaxis.set_major_formatter(date_form)
#plt.xticks(rotation = 45)
#ax.set_xticks(np.arange(datetime.date(1992,1,1), datetime.date(2014,1,2), step=datetime.timedelta(days=365.25)))
#plt.xticks(np.arange(datetime.date(1992,1,1), datetime.date(2014,1,2), step=datetime.timedelta(days=365.25)), rotation=45)
#ax.set_yticks(np.arange(datetime.date(1992,1,1), datetime.date(2014,1,1), step=365))
plt.text(0.50, 0.93, 'Historical', fontdict=font2, transform = ax.transAxes)
plt.text(0.66, 0.93, 'Projected', fontdict=font2, transform = ax.transAxes)#x=0.95, 0.97 for NO3 station 3

#plt.text(0.91, 0.92, '(a)', fontdict=text_font, transform = ax.transAxes)
#plt.text(0.91, 0.92, '(b)', fontdict=text_font, transform = ax.transAxes)
#plt.text(0.82, 0.94, 'Station 1', fontdict=font2, transform = ax.transAxes)
plt.show()
