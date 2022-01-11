# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 10:41:42 2021

@author: Administrator
"""

import os
os.chdir("D:\\Study\\Marko Mine\\Concentration")

# Importing the libraries
import numpy as np
import pandas as pd

# =============================================================================
# Choosing parameters
# =============================================================================
station = 'FR_HC1'#'FR_KC1' OR 'FR_HC1' OR 'EV_HC1'

raw_data_upper = pd.read_csv('.\\Raw Data\\Marko_All_Analytes_1972-2013_upper.csv', usecols=[1, 3, 16, 17, 20, 21])#with Nulls
raw_data_lower = pd.read_csv('.\\Raw Data\\Marko_All_Analytes_1972-2013_lower.csv', usecols=[1, 3, 16, 17, 20, 21])

raw_data_upper['sample_date'] = pd.to_datetime(raw_data_upper['sample_date'], format='%m/%d/%Y')
raw_data_lower['sample_date'] = pd.to_datetime(raw_data_lower['sample_date'], format='%Y/%m/%d')

raw_data = np.array(np.r_[raw_data_upper, raw_data_lower])

data_FR_KC1, data_FR_HC1, data_EV_HC1 = [], [], []
for i in range(0, len(raw_data)):
    if raw_data[i][0] == 'FR_KC1':
        data_FR_KC1.append(raw_data[i])
    if raw_data[i][0] == 'FR_HC1':
        data_FR_HC1.append(raw_data[i])
    if raw_data[i][0] == 'EV_HC1':
        data_EV_HC1.append(raw_data[i])
data_FR_KC1, data_FR_HC1, data_EV_HC1 = np.array(data_FR_KC1), np.array(data_FR_HC1), np.array(data_EV_HC1)

#variables_list = list(set(list(np.r_[data_FR_KC1[:,3], data_FR_HC1[:,3], data_EV_HC1[:,3]])))#all measurable variables
variables_list_FR_KC1 = list(set(list(data_FR_KC1[:,3])))#all measurable variables
variables_list_FR_HC1 = list(set(list(data_FR_HC1[:,3])))#all measurable variables
variables_list_EV_HC1 = list(set(list(data_EV_HC1[:,3])))#all measurable variables

# =============================================================================
# Sort variables for each station
# =============================================================================
#pH
pH_FR_KC1 = []
for i in range(0, len(data_FR_KC1)):
    if data_FR_KC1[i][3] == 'pH, LAB' or data_FR_KC1[i][3] == 'pH, In House Lab' or data_FR_KC1[i][3] == 'pH, Field':
        pH_FR_KC1.append(data_FR_KC1[i])
pH_FR_KC1 = np.array(pH_FR_KC1)

pH_FR_HC1 = []
for i in range(0, len(data_FR_HC1)):
    if data_FR_HC1[i][3] == 'pH, LAB' or data_FR_HC1[i][3] == 'pH, In House Lab' or data_FR_HC1[i][3] == 'pH, Field':
        pH_FR_HC1.append(data_FR_HC1[i])
pH_FR_HC1 = np.array(pH_FR_HC1)

pH_EV_HC1 = []
for i in range(0, len(data_EV_HC1)):
    if data_EV_HC1[i][3] == 'pH, LAB' or data_EV_HC1[i][3] == 'pH, In House Lab' or data_EV_HC1[i][3] == 'pH, Field':
        pH_EV_HC1.append(data_EV_HC1[i])
pH_EV_HC1 = np.array(pH_EV_HC1)

#Conductivity
cond_FR_KC1 = []
for i in range(0, len(data_FR_KC1)):
    if data_FR_KC1[i][3] == 'CONDUCTIVITY, LAB' or data_FR_KC1[i][3] == 'CONDUCTIVITY, In House Lab' or data_FR_KC1[i][3] == 'CONDUCTIVITY, Field':
        cond_FR_KC1.append(data_FR_KC1[i])
cond_FR_KC1 = np.array(cond_FR_KC1)

cond_FR_HC1 = []
for i in range(0, len(data_FR_HC1)):
    if data_FR_HC1[i][3] == 'CONDUCTIVITY, LAB' or data_FR_HC1[i][3] == 'CONDUCTIVITY, In House Lab' or data_FR_HC1[i][3] == 'CONDUCTIVITY, Field':
        cond_FR_HC1.append(data_FR_HC1[i])
cond_FR_HC1 = np.array(cond_FR_HC1)

cond_EV_HC1 = []
for i in range(0, len(data_EV_HC1)):
    if data_EV_HC1[i][3] == 'CONDUCTIVITY, LAB' or data_EV_HC1[i][3] == 'CONDUCTIVITY, In House Lab' or data_EV_HC1[i][3] == 'CONDUCTIVITY, Field':
        cond_EV_HC1.append(data_EV_HC1[i])
cond_EV_HC1 = np.array(cond_EV_HC1)

#Hardness, Total or Dissolved CaCO3
hard_FR_KC1 = []
for i in range(0, len(data_FR_KC1)):
    if data_FR_KC1[i][3] == 'Hardness, Total or Dissolved CaCO3':
        hard_FR_KC1.append(data_FR_KC1[i])
hard_FR_KC1 = np.array(hard_FR_KC1)

hard_FR_HC1 = []
for i in range(0, len(data_FR_HC1)):
    if data_FR_HC1[i][3] == 'Hardness, Total or Dissolved CaCO3':
        hard_FR_HC1.append(data_FR_HC1[i])
hard_FR_HC1 = np.array(hard_FR_HC1)

hard_EV_HC1 = []
for i in range(0, len(data_EV_HC1)):
    if data_EV_HC1[i][3] == 'Hardness, Total or Dissolved CaCO3':
        hard_EV_HC1.append(data_EV_HC1[i])
hard_EV_HC1 = np.array(hard_EV_HC1)

#NITRATE NITROGEN (NO3), AS N
NO3_FR_KC1 = []
for i in range(0, len(data_FR_KC1)):
    if data_FR_KC1[i][3] == 'NITRATE NITROGEN (NO3), AS N':
        NO3_FR_KC1.append(data_FR_KC1[i])
NO3_FR_KC1 = np.array(NO3_FR_KC1)

NO3_FR_HC1 = []
for i in range(0, len(data_FR_HC1)):
    if data_FR_HC1[i][3] == 'NITRATE NITROGEN (NO3), AS N':
        NO3_FR_HC1.append(data_FR_HC1[i])
NO3_FR_HC1 = np.array(NO3_FR_HC1)

NO3_EV_HC1 = []
for i in range(0, len(data_EV_HC1)):
    if data_EV_HC1[i][3] == 'NITRATE NITROGEN (NO3), AS N':
        NO3_EV_HC1.append(data_EV_HC1[i])
NO3_EV_HC1 = np.array(NO3_EV_HC1)


