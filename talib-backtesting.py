#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 01:27:28 2022

@author: bronx
"""

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy
import talib
import matplotlib
from talib import MA_Type
from detecta import detect_peaks
import numpy as np


#%matplotlib inline


df = yf.download('BTC-USD', interval='1h', start='2022-4-20')


#smooth moving average


#adx
df['ADX'] = talib.ADX(df.High, df.Low, df.Close, timeperiod=14)

#can also use df.Close like below
#df['BBupper'], df['BBmiddle'], df['BBlower'] = talib.BBANDS(df.Close, matype=MA_Type.T3)
df['BBupper'], df['BBmiddle'], df['BBlower'] = talib.BBANDS(df['Close'], matype=MA_Type.T3)



#will return engulfing days, both positive (100) or negative (-100) 0 value means no engulfing pattern detected
def get_engulfing(df):    
    engulfing = talib.CDLENGULFING(df.Open, df.High, df.Low, df.Close)
    df['Engulfing'] = engulfing
    engulfing_days = df[df['Engulfing'] != 0]
#    engulfing_bullish = df[df['Engulfing'] == 100]
#    englufing_bearish = df[df['Engulfing'] == -100]
    print(engulfing_days)
    return engulfing_days
    

#will return 100 if positive hammer, -100 if negative hammer and 0 if no hammer pattern detected
# will make a hammer field
def get_hammer(df):
    hammer = talib.CDLHAMMER(df.Open, df.High, df.Low, df.Close)
    df['Hammer'] = hammer
    hammer_days = df[df['Hammer'] != 0]
    print(hammer_days)
    #return hammer

def get_sma(df, tp):
    moving_average = talib.SMA(df, timeperiod=tp)
    return moving_average

#tp is time period in days
def get_rsi(df, tp):
    rsi = talib.RSI(df, timeperiod=tp)
    return rsi

def get_stoch_rsi(df):
    fastk, fastd = talib.STOCHRSI(df.Close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

def get_rocp(df):
    rocp = talib.ROCP(df.Close, timeperiod=10)
    print(rocp)
    return rocp
    
#trend indicator parabolic sar must be combined with a long term indicator that can detect a long term trend to 
# confirm that you are not trading against the long term trend eg 200 EMA
#if parabolic sar is above 200 ema then the trend is up, if below the trend is down
#1) if par sar is below 200 ema, wait for downword movement to short or 
#2) if par sar is above the 200 ema, wait for upward trend then long upwards to go with the trend

#mph is minimum peak height, mpd is minimum peak distance
#    edge ({None, 'rising', 'falling', 'both'}, optional (default = 'rising')) – for a flat peak
#    keep only the rising edge (‘rising’), only the falling edge (‘falling’), both edges (‘both’),
#    or don’t detect a flat peak (None).
#    valley (bool, optional (default = False)) – if True (1), detect valleys (local minima) instead of peaks.
def get_peaks(df,mph):
    ind = detect_peaks(df['Close'], edge='both', mph=mph, mpd=10, valley=False, show=True) 
    print(ind)


df['SMA200'] = get_sma(df['Close'],200)
df['RSI'] = get_rsi(df['Close'],14)
df = df.dropna()
df['ADX_PTC'] = df.ADX.pct_change()
print(df)

#get_hammer(df)
#get_rocp(df)
get_peaks(df,0)


#peak detection algorithm

#plt.plot(df.RSI, df.Close)


#print(engulfing_bullish)
#
#print(englufing_bearish)



#print (talib.get_functions())
#
#print (talib.get_function_groups())
##make 100 random closes
#close = numpy.random.random(100)


