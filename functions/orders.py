from binance.enums import *

import time
from datetime import datetime
import math

import numpy as np
import pandas as pd
import ccxt

from config import API_KEY, API_SECRET, client


##Conexión a ccxt
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    },
})

exchange.load_markets()



##Función para crear Long
def crear_long(QUANTITY, leverage, SYMBOL, quantityPrecision, fractal_long, close):

    quantity = round(((QUANTITY / close)*int(leverage)), quantityPrecision)

    # Abrir posición
    
    order = client.futures_create_order(
        symbol=SYMBOL,
        side=SIDE_BUY,
        positionSide = "LONG",
        type=ORDER_TYPE_MARKET,
        quantity=quantity,
    )

        # Calcular stop loss y take profit y hacerlos
    while True:
        positions = client.futures_account_trades(symbol = SYMBOL)
        last_position = positions[-1]
        time_lp = pd.to_datetime(last_position['time'], unit='ms')
        now = datetime.utcnow()
        different_time = str(now - time_lp)
        minutes = different_time[10]+different_time[11]
        print(different_time)
        if int(minutes) < 5:
            print("hecho")
            positions = client.futures_account_trades(symbol = SYMBOL)
            entryPrice = last_position['price']
            print(entryPrice)
            break
        else:
            time.sleep(1)


    


def sl_long(SYMBOL, fractal_long, quantityPrecision):
    trades = client.futures_account_trades(symbol = SYMBOL)
    quoteQty = float(trades[-1]['quoteQty'])
    quantity = round(quoteQty, quantityPrecision)    

    stop_loss = client.futures_create_order(
        symbol = SYMBOL,
        side = 'SELL',
        type = 'STOP_MARKET',
        quantity = quantity,
        positionSide = "LONG",
        stopPrice = fractal_long
    )


# Función para crear un Short
def crear_short(QUANTITY, leverage, SYMBOL, quantityPrecision, fractal_short, close):

    quantity = round(((QUANTITY / close)*int(leverage)), quantityPrecision)

    order = client.futures_create_order(
        symbol=SYMBOL,
        side=SIDE_SELL,
        positionSide = "SHORT",
        type=ORDER_TYPE_MARKET,
        quantity=quantity,
    )
      # Calcular stop loss y take profit y hacerlos
    while True:
        positions = client.futures_account_trades(symbol = SYMBOL)
        last_position = positions[-1]
        time_lp = pd.to_datetime(last_position['time'], unit='ms')
        now = datetime.utcnow()
        different_time = str(now - time_lp)
        minutes = different_time[10]+different_time[11]
        if int(minutes) < 5:
            print("hecho")
            positions = client.futures_account_trades(symbol = SYMBOL)
            entryPrice = last_position['price']
            print(entryPrice)
            break
        else:
            time.sleep(1)

    

def sl_short(SYMBOL, fractal_short, quantityPrecision):
    trades = client.futures_account_trades(symbol = SYMBOL)
    quoteQty = float(trades[-1]['quoteQty'])
    quantity = round(quoteQty, quantityPrecision)

    stop_loss = client.futures_create_order(
        symbol = SYMBOL,
        side = 'BUY',
        type = 'STOP_MARKET',
        quantity = quantity,
        positionSide = "SHORT",
        stopPrice = fractal_short
    )

## CERRAR ORDENES
def cerrar_long(SYMBOL,quantity):
           
    close_position = client.futures_create_order(
        symbol = SYMBOL,
        type = ORDER_TYPE_MARKET,
        positionSide = "LONG",
        side = SIDE_SELL,
        quantity = float(quantity)
    )
    

                

                
def cerrar_short(SYMBOL, quantity):

    close_position = client.futures_create_order(
        symbol = SYMBOL,
        type = ORDER_TYPE_MARKET,
        positionSide = "SHORT",
        side = SIDE_BUY,
        quantity = -float(quantity)
    )


def check_delete(SYMBOL, symbol_form):
    open_orders = client.futures_get_open_orders(symbol = SYMBOL)

    for order in open_orders:
        time = order['time']
        orderId = order['orderId']
        exchange.cancel_order(str(orderId), symbol_form)
