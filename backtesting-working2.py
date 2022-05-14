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
import csv

client=Client()


def getdata(symbol, interval, lookback, rollback): #back 400 hours, these settings are default values, so pass any value you need for this 
    lookback = str(lookback) #convert the passed lookback value to integer since its being added to something HOURS UTC
    rollback = int(rollback) #convert to int
    #original line
#    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+'hours UTC')) 
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+'hours UTC'))
        
    frame = frame.iloc[:,0:6]
       
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame.set_index('Time', inplace=True)
       
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    ##take the max of last 15 days rolling and define the upper band of trend price
    frame['rollhigh'] = frame.High.rolling(rollback).max()
       
    frame['rolllow'] = frame.Low.rolling(rollback).min()
       
    frame['mid'] = (frame.rollhigh + frame.rolllow)/2
    
    #define the lever of price approaching the upper band by 0.4% or nearly 99.6% close to high band
    frame['approach_high'] = np.where(frame.Close > frame.rollhigh * 0.996, 1, 0)    
    #sets 1 if yes approaching high and 0 if not in range of the upper band
       
    frame['price_above_mid'] = np.where(frame.Close > frame.mid, 1, 0)
    #1 if price is above midline or 0 if below, use this to calculate the crossing of midline 0->1 or 1->0
        
    #to find out the crossing through midline, check if the difference b/w this close and previous is 1, if its zero then this and prev are the same
    frame['price_cross'] = frame.price_above_mid.diff() == 1
    #this will set 1 to when the price crosses the mid line ie when diff in price_above_mid changes from 0 to 1

    return frame, symbol, interval, lookback, rollback



def with_range(x1,y1,x2,y2):
    for j in range(x1,y1):
        for k in range(x2, y2):
            #pass data working
            #getdata(TICKER, time interval, period back, rollback statistics average sample)
            df,symbol,interval,lookback,rollback=getdata('ETHUSDT','1h', k , j)
            #print(df)        
            #---------------------------------------------
            #strategy section
            #set initial position to false ie no crypto held, and create empty buy and sell dates
            in_position = False
            buydates, selldates = [],[] 
            #
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
    
            #make a drades data frame aranspose it with the .T
            tradesdf = pd.DataFrame([buydates, selldates, df.loc[buydates].Open, df.loc[selldates].Open]).T
            #rename the columns
            tradesdf.columns = ['buy', 'sell', 'buy_price', 'sell_price']
            #add a tally of profit gained for each buy/sell date into a seperate column
            tradesdf['profits_rel'] = (tradesdf.sell_price - tradesdf.buy_price)/tradesdf.buy_price 
            #binance trading fee is 0.075% per trade, for buy and sell there are 2 x 0.075% fees
            #since the above prices are out of 1 where 1 = 100%, we need to divide 2x0.75% = 0.150 by 100 = 0.0015
            #so we take off the 0.0015% from the relative profit table and put it into 'net_profit' table
            tradesdf['net_profit']=tradesdf.profits_rel - 0.0015
            
            print(tradesdf)
                    
            #print("buydates", buydates)
            #print("selldates", selldates)
            print("crypto", symbol)
            print("time interval", interval)
            print("lookback perdiod", lookback)
            print("rollback stat", rollback)          
            print("buy transactions",len(buydates))
            print("sell transactions",len(selldates))
            print("total return in %",((tradesdf.net_profit + 1).prod() - 1 ) * 100)
            
            f = open("backtesting-working.csv", "a", newline="")
            tup1 = (interval,lookback,rollback,len(buydates),len(selldates),((tradesdf.net_profit + 1).prod() - 1 ) * 100)
            writer = csv.writer(f)
            writer.writerow(tup1)
            f.close()

with_range(30,31,1000,1001)

#print(df)
#plt.figure(figsize=(20,10))
#plt.plot(df[['Close','rollhigh','rolllow','mid']])
#plt.scatter(buydates, df.loc[buydates].Open, marker='^', color='g', s=200)
#plt.scatter(selldates, df.loc[selldates].Open, marker='v', color='r', s=200)
    



#calculate the cumilative profit in percentage 

#if the answer is above 1.02, then the percetage gain is 2%
#if the answer is 




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




    