import pandas as pd
import numpy as np

import csv
from dateutil.relativedelta import relativedelta
from datetime import datetime
import time

import csv
import math

from binance.enums import *

from config import API_KEY, API_SECRET, client



def round_decimals_down(number:float, decimals:int=2):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return np.floor(number)

    factor = 10 ** decimals
    return np.floor(number * factor) / factor



def start(symbol, number):
    # PRimero calcular los candlesticks
    df = pd.DataFrame(client.futures_historical_klines(symbol=symbol, interval="1h", start_str="2021-03-24", end_str=None))

    # crop unnecessary columns
    df = df.iloc[:, :6]
    # ascribe names to columns
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    # convert timestamp to date format and ensure ohlcv are all numeric
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col])
    df.head()

    #Calculate the Short/Fast Exponential Moving Average
    ShortEMA = df.close.ewm(span=4, adjust=False).mean() #AKA Fast moving average
    df['short'] = round_decimals_down(ShortEMA, number)
    #Calculate the Middle Exponential Moving Average
    MiddleEMA = df.close.ewm(span=9, adjust=False).mean() #AKA Middle-Slow moving average
    df['middle'] = round_decimals_down(MiddleEMA, number)
    #Calculate the Long/Slow Exponential Moving Average
    LongEMA = df.close.ewm(span=18, adjust=False).mean() #AKA Slow moving average
    df['long'] = round_decimals_down(LongEMA, number)

    n=1
    df = df.head(-n)

    df.to_csv('token.csv', index=False, encoding='utf-8')    


def actualizar_csv(symbol, number):
    while True:
        try:
            ##VALORES
            df1 = pd.read_csv('token.csv')
            # Eliminar última línea ya que no se va a cerrar con esos valores:
            n=1
            df1 = df1.head(-n)

            #Definir el tiempo de START
            #last_date = df1['date'].values[-1]
            df1.to_csv('token.csv', index = False, encoding='utf-8')
            
            last_date = df1['date'].values[-1]
            last_date_form = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')
            new_date = str(last_date_form + relativedelta(minutes=5))

            #PRimero calcular los candlesticks
            df = pd.DataFrame(client.futures_historical_klines(symbol=symbol, interval="1h", start_str=new_date, end_str=None))

            # Eliminar columnas innecesarias
            df = df.iloc[:, :6]
            # # ascribe names to columns
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            # Convertir el tiempo a fecha formateada y asegurar que sea un número
            df['date'] = pd.to_datetime(df['date'], unit='ms')
            for col in df.columns[1:]:
                df[col] = pd.to_numeric(df[col])
            df.head()

            # Merge de los datos viejos y los nuevos
            df = pd.concat([df1,df])

            #Calculate the Short/Fast Exponential Moving Average
            ShortEMA = df.close.ewm(span=4, adjust=False).mean() #AKA Fast moving average
            df['short'] = round_decimals_down(ShortEMA, number)
            #Calculate the Middle Exponential Moving Average
            MiddleEMA = df.close.ewm(span=9, adjust=False).mean() #AKA Middle-Slow moving average
            df['middle'] = round_decimals_down(MiddleEMA, number)
            #Calculate the Long/Slow Exponential Moving Average
            LongEMA = df.close.ewm(span=18, adjust=False).mean() #AKA Slow moving average
            df['long'] = round_decimals_down(LongEMA, number)
            #print(df1)
            #print(df)

            # Actualizar el CSV con los nuevos valores recogidos
            df.to_csv('token.csv', index=False, encoding='utf-8')
            
            print("CSV Actualizado")
            
            break
        
        except Exception as e:
            print(e)
            time.sleep(10)
            actualizar_csv(symbol, number)
            break