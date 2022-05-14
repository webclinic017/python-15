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
from talib import MA_Type

df = yf.download('BTC-USD', start='2020-10-1')




#smooth moving average





df['ADX'] = talib.ADX(df.High, df.Low, df.Close, timeperiod=14)

#can also use df.Close like below
#df['BBupper'], df['BBmiddle'], df['BBlower'] = talib.BBANDS(df.Close, matype=MA_Type.T3)
df['BBupper'], df['BBmiddle'], df['BBlower'] = talib.BBANDS(df['Close'], matype=MA_Type.T3)


engulfing = talib.CDLENGULFING(df.Open, df.High, df.Low, df.Close)

df['Engulfing'] = engulfing

engulfing_days = df[df['Engulfing'] != 0]
engulfing_bullish = df[df['Engulfing'] == 100]
englufing_bearish = df[df['Engulfing'] == -100]

print(engulfing_days)

#print(engulfing_bullish)
#
#print(englufing_bearish)



#print (talib.get_functions())
#
#print (talib.get_function_groups())
##make 100 random closes
#close = numpy.random.random(100)


