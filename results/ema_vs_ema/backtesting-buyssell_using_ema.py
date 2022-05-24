#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:32:55 2022

@author: bronx
"""

#https://www.youtube.com/watch?v=wvmnlIsAzok&t=

import pandas as pd
# import numpy as np
from binance import Client #install pip3 install python-binance, not just binance
import matplotlib.pyplot as plt
import csv
import indicators
import talib
from datetime import timedelta

client=Client()

#uses binance to import price for backtrade testing eg : 
#df,symbol,interval,lookback,rollback=getdata('ETHUSDT','1h', '150', 15)
#df,symbol,interval,lookback,rollback=getdata('ETHBTC','1h', '1000', 35)
#returns the dataframe symbol/hr interval,lookback period, rollback so it can be used 
def getdata(symbol, interval, lookback, sma_slow, sma_fast): #back 400 hours, these settings are default values, so pass any value you need for this 
    lookback = str(lookback) #convert the passed lookback value to integer since its being added to something HOURS UTC
#    rollback = int(rollback) #convert to int
    #original line
#    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+'hours UTC')) 
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+'hours UTC'))
    
    #just gets the first 6 fields from the looked up data frame : time, open, high, low, close, volume
    frame = frame.iloc[:,0:6]

       
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame.set_index('Time', inplace=True)
       
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    # ##take the max of last 15 days rolling and define the upper band of trend price
    # frame['rollhigh'] = frame.High.rolling(rollback).max()
       
    # frame['rolllow'] = frame.Low.rolling(rollback).min()
       
    # frame['mid'] = (frame.rollhigh + frame.rolllow)/2
    
    # #define the lever of price approaching the upper band by 0.4% or nearly 99.6% close to high band
    # frame['approach_high'] = np.where(frame.Close > frame.rollhigh * approach_high_in, 1, 0) #make this variable
    # #sets 1 if yes approaching high and 0 if not in range of the upper band
    # frame['approach_low'] = np.where(frame.Close < frame.rolllow * approach_low_in, 1, 0) #make this variable
    # #1 if price is above midline or 0 if below, use this to calculate the crossing of midline 0->1 or 1->0
    
    # #to find out the crossing through midline, check if the difference b/w this close and previous is 1, if its zero then this and prev are the same
    # frame['price_cross_mid'] = frame.approach_low.diff() == 1
    # #this will set 1 to when the price crosses the mid line ie when diff in approach_low changes from 0 to 1
    
#    #get 200sma from talib and put it into the frame
#    frame['SMA200']=indicators.talib.SMA(frame.Close, timeperiod=200) #make this variable
#    frame['SMA100']=indicators.talib.SMA(frame.Close, timeperiod=100) #make this variable
    frame['DEMA50']=indicators.talib.DEMA(frame.Close, timeperiod=sma_slow) #make this variable
    frame['DEMA21']=indicators.talib.DEMA(frame.Close, timeperiod=sma_fast) #make this variable
#    https://www.youtube.com/watch?v=hTDVTH8umR8 
    # frame.dropna() //this may cause a index out of bounds error if frames are dropped
#    #stochastic RSI
#    frame['fastk'], frame['fastd'] = indicators.talib.STOCHRSI(frame.Close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
#    
#    #RSI
    # frame['RSI'] = talib.RSI(frame.Close, timeperiod=14)
#    
#    #directional movement index DX
#    frame['DX'] = talib.DX(frame.High, frame.Low, frame.Close, timeperiod=14)
#    
    # frame['ADX'] = talib.ADX(frame.High, frame.Low, frame.Close, timeperiod=14)
#    
#    #MACD
    # frame['MACD'],frame['MACDsig'],frame['MACDhist'] = talib.MACD(frame.Close, fastperiod=12, slowperiod=26, signalperiod=9)
    
    
    #PARABOLIC SAR
    # frame['SAR'] = talib.SAR(frame.High, frame.Low, acceleration=21, maximum=1)
    
#    frame['BBupper'], frame['BBMid'], frame['BBlow'] = talib.BBANDS(frame.Close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    # print(frame)
    in_position = False
    buydates, selldates = [],[]
    
    for i in range(len(frame)):
    #buying part of function
        if not in_position: #if no crypto not held 
            # if frame.iloc[i].approach_low: #if price_cross is 1/True which means sell
            # if frame.iloc[i].approach_low and (frame.iloc[i].RSI<45) and (frame.MACD.iloc[i-1] > frame.MACDsig.iloc[i-1]): #if price_cross is 1/True which means sell
            if  frame.DEMA21[i-1]<frame.DEMA50[i-1] and frame.DEMA21[i]>frame.DEMA50[i]: #if price_cross is 1/True which means sell
                buydates.append(frame.iloc[i].name) #add event to buy date, buy point
                # print("buying at ",frame.iloc[i].Close)           
                #the name is the name of the date just type df.iloc[0].name to see it
                #the '+1' is added to avoid the forward looking bias, ie the buy is on the next day not immediate
                in_position = True # you now bought and holding crypto so in position is true
        #now for the selling part
        if  in_position: #if you hold crypto and testing for sell signal
            # if frame.iloc[i].approach_high: #if high approach signal is 1 or true (signal is near the upper band)
            # if frame.iloc[i].approach_high and (frame.iloc[i].RSI>55) and (frame.MACD.iloc[i-1] < frame.MACDsig.iloc[i-1]) : #if high approach signal is 1 or true (signal is near the upper band)
            # last_sale_open = frame.loc[buydates[len(buydates) - 1]].Open
            # last_sale_time = frame.loc[buydates[len(buydates) - 2]].name
            # this_sale_time = frame.loc[buydates[len(buydates) - 1]].name
            # difference = this_sale_time - last_sale_time
            # time_diff = timedelta(days = 0, hours = hours_held)
            # print("this time, last time, diff, time diff", this_sale_time,last_sale_time,difference,time_diff)
            if  frame.DEMA21[i-1]>frame.DEMA50[i-1] and frame.DEMA21[i]<frame.DEMA50[i]: #if price_cross is 1/True which means sell#if high approach signal is 1 or true (signal is near the upper band)
                # last_sale = frame.loc[buydates[len(buydates) - 1]].Open
                # print("-----current price and last buy price", frame.iloc[i], last_sale)    
                # print("-----current price and last buy price", frame.iloc[i].Close, last_sale_open)    
                # print("-----SAR", frame.SAR[i], last_sale_open)
                # print("this sale time", this_sale_time)
                # print("last sale time", last_sale_time)
                # print("sale held for days ", difference)
                selldates.append(frame.iloc[i].name)
                in_position = False
    # print("buy", len(buydates))
    # print("sell", len(selldates))
    #make a drades data frame aranspose it with the .T
    tradesdf = pd.DataFrame([buydates, selldates, frame.loc[buydates].Open, frame.loc[selldates].Open]).T
    #rename the columns
    tradesdf.columns = ['buy', 'sell', 'buy_price', 'sell_price']
    #add a tally of profit gained for each buy/sell date into a seperate column
    tradesdf['profits_rel'] = (tradesdf.sell_price - tradesdf.buy_price)/tradesdf.buy_price 
    # tradesdf = tradesdf.dropna()
    #binance trading fee is 0.075% per trade, for buy and sell there are 2 x 0.075% fees
    #since the above prices are out of 1 where 1 = 100%, we need to divide 2x0.75% = 0.150 by 100 = 0.0015
    #so we take off the 0.0015% from the relative profit table and put it into 'net_profit' table
    tradesdf['net_profit']=tradesdf.profits_rel - 0.0015
    # tradesdf = tradesdf.dropna()
    # print(tradesdf)
            
    #print("buydates", buydates)
    #print("selldates", selldates)
    print("crypto", symbol)
    print("time interval", interval)
    print("lookback perdiod", lookback)
    # print("rollback stat", rollback)
    # print("appraoch_high_in", approach_high_in)          
    # print("approach_low_in", approach_low_in)
    # print("days held", hours_held)
    print("sma slow", sma_slow)
    print("sma fast", sma_fast)
    print("buy transactions",len(buydates))
    print("sell transactions",len(selldates))
    print("total return in %",((tradesdf.net_profit + 1).prod() - 1 ) * 100)
    
    f = open("DEMA_vs_DEMA.csv", "a", newline="")
    tup1 = (interval,lookback, sma_slow, sma_fast, len(buydates),len(selldates),((tradesdf.net_profit + 1).prod() - 1 ) * 100)
    writer = csv.writer(f)
    writer.writerow(tup1)
    f.close()
    # plt.figure(figsize=(20,10))
    # plt.plot(frame[['Close','DEMA21','DEMA50']])
    # plt.scatter(buydates, frame.loc[buydates].Open, marker='^', color='g', s=200)
    # plt.scatter(selldates, frame.loc[selldates].Open, marker='v', color='r', s=200)
#    plt.figure(figsize=(20,10))
#    plt.plot(frame[['fastk','fastd']]) 
    return frame, symbol, interval, lookback





# rollback_in = 15

#pass data working
#getdata(TICKER, time interval, period back, rollback statistics average sample)
# df,symbol,interval,lookback,rollback=getdata('ETHBTC','1h', '20000', rollback_in)



# approach_high_in = 0.980
# approach_low_in = 1.020

# while (approach_high_in < 1.020):
#     while (approach_low_in > 0.980):
#         approach_low_in = approach_low_in - 0.001
#         print ("appr",approach_high_in)
#         approach_high_in = approach_high_in + 0.001
#         print("app high", approach_low_in)
        


# f = 0.990
# t = 0.999
# a = 0.001


# while (f < t):
#     print ("f",f)
#     df,symbol,interval,lookback,rollback=getdata('ETHBTC','1h', '40000', rollback_in, f, 1.02)
#     f = f + a
# for rollback_in in range(35,50):
# sma_slow_in = 50
# sma_fast_in = 1

# done 
for sma_slow_in in range (15,30):
    for sma_fast_in in range (1,10):
        df,symbol,interval,lookback=getdata('ETHBTC','1h', '20000', sma_slow_in, sma_fast_in)
# df,symbol,interval,lookback=getdata('ETHBTC','1h', '2000', 45, 9)

# indicators.plot_mixed(df)

#print(df)


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




    