#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:32:55 2022

@author: bronx
"""

#https://www.youtube.com/watch?v=wvmnlIsAzok&t=

import pandas as pd
import numpy as np
from binance import Client #install pip3 install python-binance, not just binance
import matplotlib.pyplot as plt

client=Client()


def getdata(symbol, interval2, lookback2): #back 400 hours, these settings are default values, so pass any value you need for this 
    lookback2 = str(lookback2)
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval2, lookback2+'hours UTC'))
    frame = frame.iloc[:,0:6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame.set_index('Time', inplace=True)
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    ##take the max of last 15 days rolling and define the upper band of trend price
    frame['rollhigh'] = df.High.rolling(15).max()
    frame['rolllow'] = df.Low.rolling(15).min()
    frame['mid'] = (df.rollhigh + df.rolllow)/2
    
    #define the lever of price approaching the upper band by 0.4% or nearly 99.6% close to high band
    frame['approach_high'] = np.where(df.Close > df.rollhigh * 0.996, 1, 0)    
    #sets 1 if yes approaching high and 0 if not in range of the upper band
    
    frame['price_above_mid'] = np.where(df.Close > df.mid, 1, 0)
    #1 if price is above midline or 0 if below, use this to calculate the crossing of midline 0->1 or 1->0
    
    #to find out the crossing through midline, check if the difference b/w this close and previous is 1, if its zero then this and prev are the same
    frame['price_cross'] = frame.price_above_mid.diff() == 1
    #this will set 1 to when the price crosses the mid line ie when diff in price_above_mid changes from 0 to 1

    #---------------------------------------------
    #analysis section
    #set initial position to false ie no crypto held, and create empty buy and sell dates
    in_position = False
    buydates, selldates = [],[] 
    
    for i in range(len(df)):
    #buying part of function
        if not in_position: #if no crypto not held 
            if df.iloc[i].price_above_mid: #if price_cross is 1/True which means sell
                buydates.append(df.iloc[i+1].name) #add event to buy date, buy point
                #the name is the name of the date just type df.iloc[0].name to see it
                #the '+1' is added to avoid the forward looking bias, ie the buy is on the next day not immediate
            in_position = True # you now bought and holding crypto so in position is true
        #now for the selling part
        if in_position: #if you hold crypto and testing for sell signal
            if df.iloc[i].approach_high: #if high approach signal is 1 or true (signal is near the upper band)
                selldates.append(df.iloc[i+1].name)
                in_position = False
            
    print(buydates)
    #print(df)
    plt.figure(figsize=(20,10))
    plt.plot(df[['Close','rollhigh','rolllow','mid']])
    plt.scatter(buydates, df.loc[buydates].Open, marker='^', color='g', s=200)
    plt.scatter(selldates, df.loc[selldates].Open, marker='v', color='r', s=200)
    
    plt.style.use('dark_background')
    plt.figure(figsize=(20,10))
    plt.plot(df[['Close','rollhigh','rolllow','mid']])
    plt.scatter(buydates, df.loc[buydates].Open, marker='^', color='g', s=200)
    plt.scatter(selldates, df.loc[selldates].Open, marker='v', color='r', s=200)
    return frame

df=getdata('BTCUSDT','1h','200')
print(df)








##you can pass custom variables to the function 
##eg:
#ef=getdata('ETHUSDT','4h')
#print(ef)
#
#bf=getdata('ETHUSDT','4h', '400')
#print(bf)

#was put into the function
#df['rollhigh'] = df.High.rolling(15).max()
#df['rolllow'] = df.Low.rolling(15).min()
#df['mid'] = (df.rollhigh + df.rolllow)/2





#EXAMPLES
##print where price_cross is not zero
#print(df.price_cross[df.price_cross == False])
##print as above but print every column in the data frame 
#print(df[df.price_cross == True])




#in this example
#buy position if price approaces the upper band
#sell position if price crosses the mid line on its way downwards ie if 'price_cross'=True




    