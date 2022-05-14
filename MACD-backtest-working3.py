#!/usr/bin/env python
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import csv

df = yf.download('ETH-BTC', start='2021-1-1', interval='1h')

#1D 2018-1-1
#for x in range(2,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            
            
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        # interval = "1m",

#ema1=2 #min 3 max 200 HAS TO BE BIGGER THEN PREVIOUS
#ema2=3 #min 2 THESE TWO CANNOT BE THE SAME VALUE
#MACD_span=7 #min 2 max 500

print(df)

def MACD(df,x,y,z):
    df ['EMA12'] = df.Close.ewm(span=x).mean()
    df ['EMA26'] = df.Close.ewm(span=y).mean()
    df ['MACD'] = df.EMA12 - df.EMA26
    df ['signal'] = df.MACD.ewm(span=z).mean()
    Buy, Sell = [], []    
   # print(df['MACD'].max())
#    for i in range(2, len(df)): #df(len) is last value of fram
    for i in range(1, len(df)): #df(len) is last value of fram
        if df.MACD.iloc[i] > df.signal.iloc[i] and df.MACD.iloc[i-1] < df.signal.iloc[i-1]:    #check if macd in every single row i, i is row in this case always
            Buy.append(i)  #append i (row) to the buy list
        elif df.MACD.iloc[i] < df.signal.iloc[i] and df.MACD.iloc[i-1] > df.signal.iloc[i-1]:    #check for opposite and put in sell list
            Sell.append(i)      
#    Realbuys = [i+1 for i in Buy]
#    Realsells = [i+1 for i in Sell]
    Realbuys = [i for i in Buy]
    Realsells = [i for i in Sell]
    Buyprices = df.Open.iloc[Realbuys]
    Sellprices = df.Open.iloc[Realsells]
#    if Sellprices.index[0] < Buyprices.index[0]:
#        Sellprices = Sellprices.drop(Sellprices.index[0])
#    elif Buyprices.index[-1] < Sellprices.index[-1]:
#        Buyprices = Buyprices.drop(Buyprices.index[-1])
    Profitsrel = []
    for i in range(len(Sellprices)):
        Profitsrel.append((Sellprices[i] - Buyprices[i])/Buyprices[i])       #in percentage return / loss
        print("buy ",i," @ ", Buyprices[i])
        print("sell ",i," @ ",Sellprices[i])
        print("profits ",i," @ ",Profitsrel[i]*100, " %")
    print("EMA1 ",x,"EMA2",y,"Signal",z,"Return",sum(Profitsrel), " %", "EMA12 max ",df['EMA12'].max(),"EMA26 max ", df['EMA26'].max(), "signal max", df['signal'].max())
    f = open("macd-backtesting.csv", "a", newline="")
    tup1 = (x,y,z,sum(Profitsrel),df['EMA12'].max(),df['EMA26'].max(),df['signal'].max())
    writer = csv.writer(f)
    writer.writerow(tup1)
    f.close()

##works on ethbtc
#for x in range(2,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,x,y,z)
#
##doesnt work             
#for x in range(2,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,x,z,y)
##        
##works            
#for x in range(2,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,y,z,x)            
##  
##    doesnt work
#for x in range(2,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,y,x,z)
##
##    doesnt work
#for x in range(2,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,z,x,y)
#                        
#for x in range(2,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,z,y,x)
            

#ETH - BTC 1h z = 2-

#best for eth-btc pair 1550% return
#1,60,4  360
    
MACD(df,2,12,22)

          
#MACD(df,4,60,20)  

