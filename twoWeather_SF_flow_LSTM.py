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
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, GRU
from tensorflow.keras.constraints import max_norm
import tensorflow as tf

from tensorflow.keras.callbacks import ModelCheckpoint

# =============================================================================
# Choosing parameters
# =============================================================================
station = 'EVO_HC1'#'FRO_KC1' OR 'FRO_HC1' OR 'EVO_HC1'
species = 'NO3'#'NO3' OR 'Se' OR 'SO4'

target_type = 'conc'#choose 'load' OR 'conc'
recurrent_type = 'LSTM'#choose 'LSTM' OR 'GRU'

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

#target
concentration = pd.read_csv('.\\conc_data_csv\\'+station+'_'+species+'.csv')#conc. in unit of mg/L
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

#choose to predict load or concentration
if target_type == 'load':
    print('The target is set to be load.')
    merge['load'] = merge['flowrate']*merge['conc']
    merge.drop('conc', 1, inplace=True)
elif target_type == 'conc':
    print('The target is set to be concentration.')
else:
    print('Wrong target type, go with target as concentration anyway.')

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

X_train = X_scaled[:len(X_scaled)-test_size, :, :]
y_train = y_scaled[:len(X_scaled)-test_size]
y_train_not_scaled = y_not_scaled[:len(X_scaled)-test_size]
train_datetime = datetime_deNull[:len(X_scaled)+1-test_size]

X_test = X_scaled[len(X_scaled)-test_size:, :, :]
y_test = y_scaled[len(X_scaled)-test_size:]
y_test_not_scaled = y_not_scaled[len(X_scaled)-test_size:]
test_datetime = datetime_deNull[len(X_scaled)-test_size:]

# Deleting NaNs in samples
k = 0
for i in range(0, len(X_train)):
    if k>=len(X_train):
        break
    for j in X_train[k, :, :]:
        if np.isnan(j[0]) or np.isnan(j[1]) or np.isnan(j[2]) or np.isnan(j[3]) or np.isnan(j[4]):
            #print('k:', k)# for testing, print out which sample contains NaN
            X_train = np.r_[X_train[:k, :, :], X_train[k+1:, :, :]]
            y_train = np.r_[y_train[:k], y_train[k+1:]]
            y_train_not_scaled = np.r_[y_train_not_scaled[:k], y_train_not_scaled[k+1:]]
            train_datetime = np.r_[train_datetime[:k], train_datetime[k+1:]]
            k = k - 1
            break
    k = k + 1
# 259 available for training
k = 0
for i in range(0, len(X_test)):
    if k>=len(X_test):
        break
    for j in X_test[k, :, :]:
        if np.isnan(j[0]) or np.isnan(j[1]) or np.isnan(j[2]) or np.isnan(j[3]) or np.isnan(j[4]):
            #print('k:', k)
            X_test = np.r_[X_test[:k, :, :], X_test[k+1:, :, :]]
            y_test = np.r_[y_test[:k], y_test[k+1:]]
            y_test_not_scaled = np.r_[y_test_not_scaled[:k], y_test_not_scaled[k+1:]]
            test_datetime = np.r_[test_datetime[:k], test_datetime[k+1:]]
            k = k - 1
            break
    k = k + 1
# 13 available for testing

def rootMSE(y_test, y_pred):
    import math
    from sklearn.metrics import mean_squared_error
    rmse = math.sqrt(mean_squared_error(y_test, y_pred))
    print('RMSE = %2.2f' % rmse)
    print('Predicted results length:', y_pred.shape)
    y_test = np.array(y_test).reshape(-1, 1)
    print('Real results length:', y_test.shape)
    return rmse

#print(tf.__version__)
tf.keras.backend.clear_session()
tf.random.set_seed(seed)

opt = tf.keras.optimizers.Adam(learning_rate=0.001)#default lr=0.001
#@tf.function
def create_LSTM(neurons, dropoutRate, constraints):
    # Ignore the WARNING here, numpy version problem
    
    # Initializing the RNN
    regressor = Sequential()
    #regressor.add(Dropout(rate=0.2))
    '''
    # Adding the first layer of LSTM and some Dropout regularization (to prevent overfitting)
    regressor.add(LSTM(units=neurons, return_sequences=True, recurrent_dropout=dropoutRate, 
                       kernel_constraint=max_norm(constraints), recurrent_constraint=max_norm(constraints), 
                       bias_constraint=max_norm(constraints)))
    
    # Adding a second LSTM layer and some Dropout regulariazation
    regressor.add(LSTM(units=neurons, return_sequences=True, recurrent_dropout=dropoutRate, 
                       kernel_constraint=max_norm(constraints), recurrent_constraint=max_norm(constraints), 
                       bias_constraint=max_norm(constraints)))
    '''
    # Adding the last LSTM layer and some Dropout regulariazation
    regressor.add(LSTM(units=neurons, return_sequences=False, recurrent_dropout=dropoutRate,
                       kernel_constraint=max_norm(constraints), recurrent_constraint=max_norm(constraints), 
                       bias_constraint=max_norm(constraints)))
    '''
    # Adding ANN layer
    regressor.add(Dense(units=neurons, kernel_initializer='random_normal', activation='linear'))# Output layer do not need specify the activation function
    '''
    # Adding output layer
    regressor.add(Dense(units=1, kernel_initializer='random_normal', activation='relu'))# Output layer do not need specify the activation function
    
    # Compiling the RNN by usign right optimizer and right loss function
    regressor.compile(loss='mean_squared_error', optimizer=opt, metrics=['mse'])#adam to be changed
    return regressor

def create_GRU(neurons, dropoutRate, constraints):
    # Ignore the WARNING here, numpy version problem
    
    # Initializing the RNN
    regressor = Sequential()
    #regressor.add(Dropout(rate=0.2))
    '''
    # Adding the first layer of GRU and some Dropout regularization (to prevent overfitting)
    regressor.add(GRU(units=neurons, return_sequences=True, recurrent_dropout=dropoutRate, 
                       kernel_constraint=max_norm(constraints), recurrent_constraint=max_norm(constraints), 
                       bias_constraint=max_norm(constraints)))
    
    # Adding a second GRU layer and some Dropout regulariazation
    regressor.add(GRU(units=neurons, return_sequences=True, recurrent_dropout=dropoutRate, 
                       kernel_constraint=max_norm(constraints), recurrent_constraint=max_norm(constraints), 
                       bias_constraint=max_norm(constraints)))
    '''
    # Adding the last GRU layer and some Dropout regulariazation
    regressor.add(GRU(units=neurons, return_sequences=False, recurrent_dropout=dropoutRate,
                       kernel_constraint=max_norm(constraints), recurrent_constraint=max_norm(constraints), 
                       bias_constraint=max_norm(constraints)))
    '''
    # Adding ANN layer
    regressor.add(Dense(units=neurons, kernel_initializer='random_normal', activation='linear'))# Output layer do not need specify the activation function
    '''
    # Adding output layer
    regressor.add(Dense(units=1, kernel_initializer='random_normal', activation='relu'))# Output layer do not need specify the activation function
    
    # Compiling the RNN by usign right optimizer and right loss function
    regressor.compile(loss='mean_squared_error', optimizer=opt, metrics=['mse'])#adam to be changed
    return regressor

# Setting hyperparameters manually
best_neurons = 50
best_dropoutRate = 0.1
constraints = 99
batch_size = 4

early_epoch = 200
validation_freq = 1

print('The training stopped at epoch:', early_epoch)
print('Training the LSTM without monitoring the validation set...')

#2 choose 1 
#LSTM/GRU
if recurrent_type == 'LSTM':
    print('Creating LSTM...')
    regressor = create_LSTM(neurons=best_neurons,
                            dropoutRate=best_dropoutRate,
                            constraints=constraints)
    
    checkpoint = ModelCheckpoint('./Vanilla_LSTM results/'+station+'/'+species+'/5Input_conc_{epoch:02d}', 
                                 monitor='val_loss', verbose=1, 
                                 save_best_only=False, save_weights_only=True, 
                                 mode='auto', save_freq='epoch')
elif recurrent_type == 'GRU':
    print('Creating GRU...')
    regressor = create_GRU(neurons=best_neurons,
                            dropoutRate=best_dropoutRate,
                            constraints=constraints)

    checkpoint = ModelCheckpoint('./Vanilla_GRU results/'+station+'/'+species+'/5Input_conc_{epoch:02d}', 
                                 monitor='val_loss', verbose=1, 
                                 save_best_only=False, save_weights_only=True, 
                                 mode='auto', save_freq='epoch')
else:
    print('Wrong target type, go with LSTM anyway.')
    regressor = create_LSTM(neurons=best_neurons,
                            dropoutRate=best_dropoutRate,
                            constraints=constraints)
    
    checkpoint = ModelCheckpoint('./Vanilla_LSTM results/'+station+'/'+species+'/5Input_conc_{epoch:02d}', 
                                 monitor='val_loss', verbose=1, 
                                 save_best_only=False, save_weights_only=True, 
                                 mode='auto', save_freq='epoch')

r = regressor.fit(X_train, y_train, epochs=early_epoch, batch_size=batch_size, 
                  validation_data=(X_test, y_test), 
                  validation_freq=validation_freq, callbacks=[checkpoint])
regressor.summary()

plt.plot(range(1,early_epoch+1), r.history['loss'], label='loss')
plt.plot(np.linspace(0,early_epoch,int(early_epoch/validation_freq)+1,endpoint=True)[1:int(int(early_epoch/validation_freq)+1)], 
         r.history['val_loss'], label='val_loss')
loss_history = np.c_[r.history['loss'], r.history['val_loss']]
plt.legend()
plt.show()
print('epoch         loss         val_loss')
print(np.c_[range(1,early_epoch+1), loss_history])
#choose LSTM or GRU save history loss
if recurrent_type == 'GRU':
    np.savetxt('./Vanilla_GRU results/'+station+'/'+species+'/5Input_conc_loss_history.csv',np.c_[range(1,early_epoch+1), loss_history],fmt='%s',delimiter=',')
else:
    np.savetxt('./Vanilla_LSTM results/'+station+'/'+species+'/5Input_conc_loss_history.csv',np.c_[range(1,early_epoch+1), loss_history],fmt='%s',delimiter=',')

sc_flow = MinMaxScaler(feature_range=(0, 1), copy=True)
sc_flow.fit_transform(np.array(y_train_not_scaled).reshape(-1, 1))

# Sensitivity test
#X_test[:,:,1] = 1.2*X_test[:,:,0]#Year+-20%
#X_test[:,:,1] = 1.2*X_test[:,:,1]#Temp+-20%
#X_test[:,:,2] = 0.8*X_test[:,:,2]#Precip+-20%

#X_train[:,:,1] = 1.2*X_test[:,:,0]#Year+-20%
#X_train[:,:,1] = 1.2*X_train[:,:,1]#Temp+-20%
#X_train[:,:,2] = 0.8*X_train[:,:,2]#Precip+-20%

y_pred_scaled = regressor.predict(X_test)
y_pred = sc_flow.inverse_transform(y_pred_scaled)

y_pred_scaled_train = regressor.predict(X_train)
y_pred_train = sc_flow.inverse_transform(y_pred_scaled_train)

# Evaluation
rootMSE(y_test_not_scaled, y_pred)

# =============================================================================
# Plotting the training and test prediction
# =============================================================================
plt.plot(test_datetime, y_test_not_scaled, label='test')
plt.plot(test_datetime, y_pred, label='test pred')#x-label requires turning angle
plt.legend(loc='best')
plt.show()

plt.plot(train_datetime, y_pred_train, label='train pred')
plt.plot(train_datetime, y_train_not_scaled, label='train')
#plt.xticks(train_datetime, train_datetime, rotation = 'vertical')
plt.legend(loc='best')
plt.show()

# =============================================================================
# Saving the training results
# =============================================================================
# Saving prediction on test set
np.savetxt(station+'_'+species+'_Test_Data.csv',np.c_[test_datetime,y_test_not_scaled,y_pred],fmt='%s',delimiter=',')

# Saving prediction on train set
np.savetxt(station+'_'+species+'_Train_Data.csv',np.c_[train_datetime,y_train_not_scaled,y_pred_train],fmt='%s',delimiter=',')

# Restore the weights
best_epoch = 129
#choose load direction
if recurrent_type == 'GRU':
    regressor.load_weights('./Vanilla_GRU results/'+station+'/'+species+'/5Input_conc_'+str(best_epoch))#Skip compiling and fitting process
else:
    regressor.load_weights('./Vanilla_LSTM results/'+station+'/'+species+'/5Input_conc_'+str(best_epoch))#Skip compiling and fitting process

# =============================================================================
# Predicting on everyday weather data
# =============================================================================












