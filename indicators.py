#!/usr/bin/env python3


import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import csv
import copy
import talib


pd.options.mode.chained_assignment = None #dont show all the warnings
pd.set_option('display.max_columns', None) #show all the columns wide view

#----------------------------------TALIB INDICATORS----------------------------------
#talib indicators from talib technical library eg https://www.youtube.com/watch?v=0XQjgmChtE4&t=496s

#SMA examples
#moving_average = indicators.talib.SMA(df.Close, timeperiod=10) then print
#print("moving average", moving_average[10:20]) #print only from instance 10 to 20 since Na values until 10

#RSI examples
#stochastic RSI
#fastk, fastd = indicators.talib.STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)


#ADX examples
#if ADX > 25 then its a strong trend, if ADX < 25 you cant rely on the trend as its a weak or untradable unpredictable trend
#if you are using momentum strategy eg stoch RSI and ADX > 50 then dont exit the market as its highly likely to continue
#https://www.youtube.com/watch?v=pAFJmmjY9K8





#------------------------------------------------------------------------------------



def BUYD(df):
    df ['EMA1'] = copy.deepcopy(df.Close.ewm(span=3).mean())
    df ['EMA11'] = copy.deepcopy(df.Close.ewm(span=11).mean())
    df ['MACD'] = copy.deepcopy(df.EMA1 - df.EMA11)
    df ['signal'] = copy.deepcopy(df.MACD.ewm(span=21).mean())
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
    Expensesrel = []
    print(Profitsrel)
    for i in range(len(Sellprices)-1):
        Profitsrel.append(100*(Sellprices[i] - Buyprices[i])/Buyprices[i])       #in percentage return / loss
        print("buy ",i," @ ", Buyprices[i])
        print("sell ",i," @ ",Sellprices[i])
        print("profits ",i," @ ", Profitsrel[i] , " %")
        print("Purchase fee ",Buyprices[i]*.001)
        print("Sales fee ",Sellprices[i]*.001)
        Expensesrel.append(Sellprices[i]-Buyprices[i]-Buyprices[i]*.001 + Sellprices[i]*.001)
        print("total fee ",Buyprices[i]*.001 + Sellprices[i]*.001)
        print("money made on trade",i," is ",Sellprices[i]-Buyprices[i]-(Buyprices[i]*.001 + Sellprices[i]*.001))
        print("total percent at ",i," @ ",sum(Profitsrel)," %")
        print("total money made so far",i," is ", sum(Expensesrel))
    print("Return",sum(Profitsrel), " %, RSI ", df.RSI[i]) 
    f = open("RSI-backtesting.csv", "a", newline="")
    tup1 = (sum(Profitsrel),df.RSI[i])
    writer = csv.writer(f)
    writer.writerow(tup1)
    f.close()

def computeRSI (data, time_window,k_window, d_window, window):

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

#stochastic function below, window might be diff then above
#    data, k_window, d_window, window):
    # input to function is one column from df
    # containing closing price or whatever value we want to extract K and D from
    min_val  = data.rolling(window=window, center=False).min()
    max_val = data.rolling(window=window, center=False).max()
    stoch = ( (data - min_val) / (max_val - min_val) ) * 100
    K, D = [],[]
    K.append(stoch.rolling(window=k_window, center=False).mean())
    K = stoch
    D.append(K.rolling(window=d_window, center=False).mean())
    
#    Buy, Sell = [], []  
#    for i in range(1, len(data)): #df(len) is last value of fram
#        if K.iloc[i] < D.iloc[i] and K.iloc[i-1] > D.iloc[i-1]:    #check if macd in every single row i, i is row in this case always
#            Sell.append(i)  #append i (row) to the buy list
#        elif K.iloc[i] > D.iloc[i] and K.iloc[i-1] > K.iloc[i-1]:    #check for opposite and put in sell list
#            Buy.append(i)
#    Realbuys = [i for i in Buy]
#    Realsells = [i for i in Sell]
#    Buyprices = data.Open.iloc[Realbuys]
#    Sellprices = data.Open.iloc[Realsells]
#    Profitsrel = []
#    Expensesrel = []
#    print(Profitsrel)
#    for i in range(len(Sellprices)-1):
#        Profitsrel.append(100*(Sellprices[i] - Buyprices[i])/Buyprices[i])       #in percentage return / loss
#        print("buy ",i," @ ", Buyprices[i])
#        print("sell ",i," @ ",Sellprices[i])
#        print("profits ",i," @ ", Profitsrel[i] , " %")
#        print("Purchase fee ",Buyprices[i]*.001)
#        print("Sales fee ",Sellprices[i]*.001)
#        Expensesrel.append(Sellprices[i]-Buyprices[i]-Buyprices[i]*.001 + Sellprices[i]*.001)
#        print("total fee ",Buyprices[i]*.001 + Sellprices[i]*.001)
#        print("money made on trade",i," is ",Sellprices[i]-Buyprices[i]-(Buyprices[i]*.001 + Sellprices[i]*.001))
#        print("total percent at ",i," @ ",sum(Profitsrel)," %")
#        print("total money made so far",i," is ", sum(Expensesrel))
#    print("Return",sum(Profitsrel), " %, RSI ", data.RSI[i]) 
#    f = open("RSI-backtesting.csv", "a", newline="")
#    tup1 = (sum(Profitsrel),data.RSI[i])
#    writer = csv.writer(f)
#    writer.writerow(tup1)
#    f.close() 
    
    return K, rsi



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
    plot_weekly_stoch_RSI(df)
    return None

def plot_weekly_stoch_RSI(df_res):
    # WEEKLY plot corresponding Stoch RSI values and significant levels
    plt.figure(figsize=(15,5))
    plt.title('WEEKLY stochRSI chart')

    df_res = df_res.reset_index()
    plt.plot(df_res['Date'], df_res['K'].fillna(0))   # NaN to zeros so plot is in scale
    plt.plot(df_res['Date'], df_res['D'].fillna(0))   # NaN to zeros so plot is in scale

    #df_res.reset_index().plot(x='Date', y='K', figsize=(15,5))
    #df_res.reset_index().plot(x='Date', y='D', figsize=(15,5))

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    #plt.axhline(30, linestyle='--')

    #plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    plt.show()
    return None

def plot_mixed(df, df_res):
    plot_price(df)
    plot_RSI(df)    
    plot_weekly_stoch_RSI(df_res)
    return None

