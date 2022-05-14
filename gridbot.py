#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 17:05:13 2022

@author: bronx
"""

import ccxt, config, time, sys

exchange = ccxt.ftx({
        'apiKey': config.API_KEY,
        'secret': config.SECRET_KEY
        })

ticker = exchange.fetch_ticker(config.SYMBOL)




buy_orders = []
sell_orders = []

def initiate_program():
    for i in range(config.NUM_BUY_GRID_LINES):
        price = ticker['bid'] - (GRID_SIZE * (i+1))
        print("submitting market limit buy order at {}".format(price))
        order = exchange.create_limit_buy_order(config.SYMBOL, POSITION_SIZE, price) 
        buy_orders.append(order['info'])

    for i in range(config.NUM_SELL_GRID_LINES):
        price = ticker['bid'] + (GRID_SIZE * (i+1))
        print("submitting market limit sell order at {}".format(price))
        order = exchange.create_limit_sell_order(config.SYMBOL, POSITION_SIZE, price)
        sell_orders.append(order['info'])
    


        

def check_ticker_info():
    print("****************************************************************")
    print("1hr change : ", ticker['info']['change1h'])
    print("24hr change : ", ticker['info']['change24h'])
    print("24hr max price : ",ticker['info']['priceHigh24h'],config.SYMBOL)
    print("24hr min price : ",ticker['info']['priceLow24h'],config.SYMBOL)
    max = float(ticker['info']['priceHigh24h'])
    min = float(ticker['info']['priceLow24h'])
    median = (max + min)/2
    print("24hr median price : ", median, config.SYMBOL)
    GRID_SIZE = ticker['bid'] * 0.03
    print("current 3% grid size is : ", GRID_SIZE)
    print("set invest size to :", config.INVEST_SIZE)
    POSITION_SIZE = config.INVEST_SIZE / ticker['bid']
    print("position size for : $", config.INVEST_SIZE*config.NUM_SELL_GRID_LINES, "is ", POSITION_SIZE, config.SYMBOL)
    print("you need to buy : $", config.INVEST_SIZE * config.NUM_SELL_GRID_LINES, config.SYMBOL)
    print("which is :", config.INVEST_SIZE * config.NUM_SELL_GRID_LINES/ticker['bid'], config.SYMBOL)
    print("****************************************************************")    
    

#gets price right now and adds 3% grids above and below the current price
def get_grid_size():
    #grid size is 3% from current bid
    GRID_SIZE = ticker['bid'] * 0.03
    POSITION_SIZE = config.INVEST_SIZE / ticker['bid']
    return GRID_SIZE, POSITION_SIZE





GRID_SIZE, POSITION_SIZE = get_grid_size()

#this initiates the first buy orders
#initiate_program()
    
#while True:
#    GRID_SIZE, POSITION_SIZE = get_grid_size()
#    
#    closed_order_ids = []
#
#    for buy_order in buy_orders:
#        print("checking buy order {}".format(buy_order['id']))
#        try:
#            order = exchange.fetch_order(buy_order['id'])
#        except Exception as e:
#            print("request failed, retrying")
#            continue
#            
#        order_info = order['info']
#
#        if order_info['status'] == config.CLOSED_ORDER_STATUS:
#            closed_order_ids.append(order_info['id'])
#            print("buy order executed at {}".format(order_info['price']))
#            new_sell_price = float(order_info['price']) + GRID_SIZE
#            print("creating new limit sell order at {}".format(new_sell_price))
#            new_sell_order = exchange.create_limit_sell_order(config.SYMBOL, POSITION_SIZE, new_sell_price)
#            sell_orders.append(new_sell_order)
#
#        time.sleep(config.CHECK_ORDERS_FREQUENCY)
#
#    for sell_order in sell_orders:
#        print("checking sell order {}".format(sell_order['id']))
#        try:
#            order = exchange.fetch_order(sell_order['id'])
#        except Exception as e:
#            print("request failed, retrying")
#            continue
#            
#        order_info = order['info']
#
#        if order_info['status'] == config.CLOSED_ORDER_STATUS:
#            closed_order_ids.append(order_info['id'])
#            print("sell order executed at {}".format(order_info['price']))
#            new_buy_price = float(order_info['price']) - GRID_SIZE
#            print("creating new limit buy order at {}".format(new_buy_price))
#            new_buy_order = exchange.create_limit_buy_order(config.SYMBOL, POSITION_SIZE, new_buy_price)
#            buy_orders.append(new_buy_order)
#
#        time.sleep(config.CHECK_ORDERS_FREQUENCY)
#
#    for order_id in closed_order_ids:
#        buy_orders = [buy_order for buy_order in buy_orders if buy_order['id'] != order_id]
#        sell_orders = [sell_order for sell_order in sell_orders if sell_order['id'] != order_id]
#
#    if len(sell_orders) == 0:
#        sys.exit("stopping bot, nothing left to sell")    
        
check_ticker_info()

#print (exchange.fetch_balance(params = {"info": "USD"}))


currency = exchange.currency('USD')
print(currency)
print(currency['id'])

balance = exchange.fetch_balance({'currency': currency['id']})
print(balance['total'])


balance = exchange.fetch_balance({'currency': currency['id']})
print("Ballance Totals", balance['total'])

balance = exchange.fetch_balance({'currency': currency['id']})
print("Ballance Free", config.SYMBOL2, "is",balance['free'][config.SYMBOL2])

balance = exchange.fetch_balance({'currency': currency['id']})
print("Ballance Free", config.SYMBOL1, "is",balance['free'][config.SYMBOL1])

balance = exchange.fetch_balance({'currency': currency['id']})
print("Ballance Free FTM", balance['free']['FTM'])


if config.SYMBOL1 < config.SYMBOL2:
    print("bigger") 
    





#print(GRID_SIZE, POSITION_SIZE)

#print(ticker['info'])
#print(ticker['info']['change1h'])
#print(ticker['info']['change1h'])
