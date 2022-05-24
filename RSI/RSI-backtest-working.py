#!/usr/bin/env python

import indicators

df = indicators.yf.download('BTC-USD', start='2020-10-1')

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

#data = adj close data




#adds rsi to field at end 14 days close
df = df.dropna()
df['K'], df['RSI']= indicators.computeRSI(df['Adj Close'],10, 1, 3, 19)
#df['K'], df['D'], df['RSI']= indicators.computeRSI(df['Adj Close'],10, 1, 3, 19)

#df = df.dropna()


print(df)
#print(df.W)jy



#df['K Weekly'], df['D Weekly'], df['RSI Weekly'] = indicators.computeWeeklyStochasticRSI(df['Adj Close'],14,3,3,14)
#agg_dict = {'Open': 'first',
#          'High': 'max',
#          'Low': 'min',
#          'Close': 'last',
#          'Adj Close': 'last',
#          'Volume': 'mean',
#          'K': 'mean',
#          'D': 'mean',
#          'RSI': 'mean'}
#df = df.resample('W').agg(agg_dict)
#df['RSI W'] = indicators.computeRSI(df['Adj Close'],14,3,3,14)
#df['K W'], df['D W'] = indicators.computeRSI(df['RSI W'], 14,3,3,14)

#print(df)


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

