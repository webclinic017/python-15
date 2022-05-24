#!/usr/bin/env python
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import csv

df = yf.download('BNB-USD', start='2019-1-1')

#1D 2018-1-1
#for x in range(2,10):
#    for y in range(11,20):
#        for z in range (21,30)
#            
            
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        # interval = "1m",

#ema1=2 #min 3 max 200 HAS TO BE BIGGER THEN PREVIOUS
#ema2=3 #min 2 THESE TWO CANNOT BE THE SAME VALUE
#MACD_span=7 #min 2 max 500

print(df)

def computeRSI (data, time_window):
    diff = data.diff(1).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]
    
    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi


def stochastic(data, k_window, d_window, window):
    # input to function is one column from df
    # containing closing price or whatever value we want to extract K and D from
    min_val  = data.rolling(window=window, center=False).min()
    max_val = data.rolling(window=window, center=False).max()
    stoch = ( (data - min_val) / (max_val - min_val) ) * 100
    K = stoch.rolling(window=k_window, center=False).mean() 
    #K = stoch
    D = K.rolling(window=d_window, center=False).mean() 
    return K, D


def plot_price(df):
    # plot price
    plt.figure(figsize=(15,5))
    plt.plot(df['Adj Close'])
    plt.title('Price chart (Adj Close)')
    plt.show()
    return None

def plot_RSI(df):
    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(15,5))
    plt.title('RSI chart')
    plt.plot(df['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    plt.show()
    return None

def plot_stoch_RSI(df):
    # plot corresponding Stoch RSI values and significant levels
    plt.figure(figsize=(15,5))
    plt.title('stochRSI chart')
    plt.plot(df['K'])
    plt.plot(df['D'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    #plt.axhline(30, linestyle='--')

    #plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    plt.show()
    return None

def plot_all(df):
    plot_price(df)
    plot_RSI(df)
    plot_stoch_RSI(df)
    return None



#adds rsi to field at end 14 days close
df['RSI'] = computeRSI(df['Adj Close'], 14)
df['K'], df['D'] = stochastic(df['RSI'], 3, 3, 14)


print(df)
plot_all(df)





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
    for i in range(len(Sellprices)-1):
        Profitsrel.append(100*(Sellprices[i] - Buyprices[i])/Buyprices[i])       #in percentage return / loss
#        print("buy ",i," @ ", Buyprices[i])
#        print("sell ",i," @ ",Sellprices[i])
#        print("profits ",i," @ ",Profitsrel[i]*100, " %")
    print("EMA1 ",x,"EMA2",y,"Signal",z,"Return",sum(Profitsrel), " %", "EMA12 max ",df['EMA12'].max(),"EMA26 max ", df['EMA26'].max(), "signal max", df['signal'].max())
    f = open("macd-backtesting.csv", "a", newline="")
    tup1 = (x,y,z,sum(Profitsrel),df['EMA12'].max(),df['EMA26'].max(),df['signal'].max())
    writer = csv.writer(f)
    writer.writerow(tup1)
    f.close()
#
##works on ethbtc
#for x in range(1,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,x,y,z)
#
##doesnt work             
#for x in range(1,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,x,z,y)
##        
##works            
#for x in range(1,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,y,z,x)            
##  
##    doesnt work
#for x in range(1,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,y,x,z)
##
##    doesnt work
#for x in range(1,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,z,x,y)
#                        
#for x in range(1,10):
#    for y in range(11,20):
#        for z in range (21,30):
#            MACD(df,z,y,x)
            

#ETH - BTC 1h z = 2-

#best for eth-btc pair 1550% return
#1,60,4  360
    
#MACD(df,2,12,22)

          
#MACD(df,4,60,20)  

