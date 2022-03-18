from flask import Flask, request, abort, render_template, jsonify
import json, jinja2
from binance.enums import *
from bson.json_util import dumps

import pandas as pd
from datetime import datetime

from csv_files.db import *

from functions.orders import *
from config import *

import threading, ccxt

#Conexión a ccxt
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    },
})

exchange.load_markets()


app = Flask(__name__)

# Vistas del index
@app.route('/')
def index():
    # Recoger balance actual
    account_balance = client.futures_account_balance()
    for asset in account_balance:
        if asset['asset'] == "USDT":
            actual_balance = round(float(asset['balance']), 2)

            total_gains = round(actual_balance - BALANCE_START, 2)
            if total_gains <= 0:
                simbolo = ''
            if total_gains > 0:
                simbolo = '+'


    # Add data for the chart    
    lista = pd.read_csv('csv_files/balances.csv')
    index_lista = lista.index
    number_of_rows_lista = len(index_lista)
    rows_lista = int(number_of_rows_lista-5)

    list = pd.read_csv('csv_files/balances.csv', skiprows=rows_lista)

    labels = [list.values[i][0] for i in range(5)]
    values = [list.values[i][1] for i in range(5)]

    # Add the logs
    all_logs = pd.read_csv('csv_files/logs.csv')
    index_logs = all_logs.index
    number_of_rows_logs = len(index_logs)
    rows_logs = int(number_of_rows_logs-5)

    logs = pd.read_csv('csv_files/logs.csv', skiprows = rows_logs)
    

    #To pay
    if total_gains*percentage <= 0:
        to_pay = 0
    else:
        to_pay = total_gains*percentage

    # Add transactions
    transaction = client.futures_account_trades(symbol = SYMBOL)

    # Add orders
    order = client.futures_get_all_orders(symbol = SYMBOL)
    
    # More data from config
    return render_template('index.html', order=order, transaction=transaction, name=name, labels=labels, logs=logs,
    values=values, symbol=SYMBOL, last_balance=actual_balance, total_gains=total_gains, simbolo=simbolo, to_pay=to_pay)



    

#Route to receive webhook
@app.route('/webhook', methods=['POST'])
def webhook():

    data = json.loads(request.data)

    # Indiciador Long
    if data['passhprase'] == "LONG":
        close = data['close']
        fractal_long = data['fractal_long']
        
        # Aquí irá la creación de una posición y SL 'SIEMPRE QUE NO HAYA UN LONG ABIERTO'
        ## Chequear si hay alguna posición abierta
         #Recoger posiciones
        open_positions = exchange.fetch_balance()['info']['positions']

        for position in open_positions:
            # Si hay un SHORT:
            if (position['entryPrice'] > '0.00') & (position['positionSide'] == "SHORT"):
                if position['symbol'] == SYMBOL:
                    quantity = position['positionAmt']
                    cerrar_short(SYMBOL, quantity)
                    check_delete(SYMBOL, symbol_form)

                    add_logs("closed the last position with the order")
                    add_balance()

                    crear_long(QUANTITY, leverage, SYMBOL, quantityPrecision, fractal_long, close) 
                    sl_long(SYMBOL, fractal_long, quantityPrecision)

                    add_logs("opened a new Long position")

                    break        


            # Si hay un long
            if (position['entryPrice'] > '0.00') & (position['positionSide'] == "LONG"):
                if position['symbol'] == SYMBOL:
                    break

            # Si no hay ninguna posición
            else:
                
                crear_long(QUANTITY, leverage, SYMBOL, quantityPrecision, fractal_long, close) 
                sl_long(SYMBOL, fractal_long, quantityPrecision)

                add_balance()
                add_logs("opened a new Long position")

                break

        return{
            "code":"long succesful"
        }

    
    # Indicador Short
    if data['passhprase'] == "SHORT":
        close = data['close']
        fractal_short = data['fractal_short']
        # Aquí irá la creación de una posición y SL 'SIEMPRE QUE NO HAYA UN SHORT ABIERTO'
        ## Chequear si hay alguna posición abierta
         #Recoger posiciones
        open_positions = exchange.fetch_balance()['info']['positions']

        for position in open_positions:
            if (position['entryPrice'] > '0.00') & (position['positionSide'] == "LONG"):
                if position['symbol'] == SYMBOL:
                    quantity = position['positionAmt']
                    cerrar_long(SYMBOL, quantity)
                    check_delete(SYMBOL, symbol_form)

                    add_logs("closed the last position with the order")


                    crear_short(QUANTITY, leverage, SYMBOL, quantityPrecision, fractal_short, close)
                    sl_short(SYMBOL, fractal_short,quantityPrecision)

                    add_logs("opened a new Short position")

                    add_balance()
                    

                    break

            # Si hay un Short
            if (position['entryPrice'] > '0.00') & (position['positionSide'] == "SHORT"):
                if position['symbol'] == SYMBOL:
                    break


            # Si no hay ninguna posición
            else:

                crear_short(QUANTITY, leverage, SYMBOL, quantityPrecision, pricePrecision, close)
                sl_short(SYMBOL, fractal_short, quantityPrecision)

                add_logs("opened a new Short position")

                add_balance()
                

                break

        return{
            "code":"short succesful"
        }



    # Cambio de Fractal
    if data['passhprase'] == "FR-Long":
        fractal_long = data['value']
        # Aquí irá el cambio de SL para el LONG 'SIEMPRE QUE HAYA UN LONG ABIERTO'
        ## Chequear si hay alguna posición abierta
         #Recoger posiciones
        open_positions = exchange.fetch_balance()['info']['positions']

        for position in open_positions:
            if (position['entryPrice'] > '0.00') & (position['positionSide'] == "LONG"):
                if position['symbol'] == SYMBOL:
                # Si hay un long
                    orders = client.futures_get_open_orders()
                    for order in orders:
                        if order['symbol'] == SYMBOL:

                            check_delete(SYMBOL, symbol_form)

                
                                     
                    sl_long(SYMBOL, fractal_long, quantityPrecision)   

                    add_logs("changed the last SL")


        return{
            "code":"fr-long succesful"
        }


    # Cambio de fractal
    if data['passhprase'] == "FR-Short":
        fractal_short = data['value']
        # Aquí irá el cambio de SL para el SHORT 'SIEMPRE QUE HAYA UN SHORT ABIERTO'
        ## Chequear si hay alguna posición abierta
         #Recoger posiciones
        open_positions = exchange.fetch_balance()['info']['positions']

        for position in open_positions:
            if (position['entryPrice'] > '0.00') & (position['positionSide'] == "SHORT"):
                if position['symbol'] == SYMBOL:
                # Si hay un short
                    orders = client.futures_get_open_orders()
                    for order in orders:
                        if order['symbol'] == SYMBOL:

                            check_delete(SYMBOL, symbol_form)

            

                    sl_short(SYMBOL, fractal_short, quantityPrecision)  

                    add_logs("changed the last SL")

        return{
            "code":"fr-short succesful"
        }



    # VOl 80 Long
    if data['passhprase'] == "VOL-Long":
       # Aquí irá el cambio de SL para el LONG 'SIEMPRE QUE HAYA UN LONG ABIERTO'
        ## Chequear si hay alguna posición abierta
         #Recoger posiciones
        open_positions = exchange.fetch_balance()['info']['positions']

        for position in open_positions:
            if position['symbol'] == SYMBOL:
                # Si hay un long
                if (position['entryPrice'] > '0.00') & (position['positionSide'] == "LONG"):

                    orders = client.futures_get_open_orders()
                    for order in orders:
                        if order['symbol'] == SYMBOL:

                            check_delete(SYMBOL, symbol_form)

                
                    #Recoger fractal
                    fractal_long = data['value']

                    
                    sl_long(SYMBOL, fractal_long, quantityPrecision)  

                    add_logs("changed the last SL for overbought") 


        return{
            "code":"vol-long succesful"
        }



    # VOl 80 Short
    if data['passhprase'] == "VOL-Short":
         # Aquí irá el cambio de SL para el SHORT 'SIEMPRE QUE HAYA UN SHORT ABIERTO'
        ## Chequear si hay alguna posición abierta
         #Recoger posiciones
        open_positions = exchange.fetch_balance()['info']['positions']

        for position in open_positions:
            if position['symbol'] == SYMBOL:
                # Si hay un short
                if (position['entryPrice'] > '0.00') & (position['positionSide'] == "SHORT"):
                    
                    orders = client.futures_get_open_orders()
                    for order in orders:
                        if order['symbol'] == SYMBOL:

                            check_delete(SYMBOL, symbol_form)

                
                    #Recoger fractal
                    fractal_short = data['value']

                    sl_short(SYMBOL, fractal_short, quantityPrecision)  

                    add_logs("changed the last SL for oversold")

        return{
            "code":"vol-short succesful"
        }


                
    
    else:
        return{
            "code": "nice try but no"
        }

        


if __name__ == '__main__':
    app.run(debug=True, port=8000)