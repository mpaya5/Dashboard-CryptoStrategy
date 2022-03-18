import pandas as pd
import time, datetime
import csv
from binance.client import Client

API_KEY = "k400uR1YOiTOqyuv93pTtCwlrSUZu3qYL04WDDemcoUGnMxzCOH9N6TyygfYjjGH"
API_SECRET = "ppTHWC6Htqsjm0r7KETuQphzPqizXewGAInBtaPPmPANQNaJDFmeWUtJZgYYFagf"

client = Client(API_KEY, API_SECRET, tld='com')


# Función para crear logs
def add_logs(message):
    time = datetime.datetime.utcnow()
    year = str(time.year)
    month = str(time.month)
    day = str(time.day)
    hour = str(time.hour)

    log = f"At "+hour+" of the day "+day+"/"+month+" of "+year+" the bot have "+message

    miDato = [log]
    miArchivo = open('csv_files/logs.csv', 'a+')
    writer = csv.writer(miArchivo)
    writer.writerow(miDato)
    miArchivo.close()

# Función para añadir balance
def add_balance():
    account_balance = client.futures_account_balance()
    for acbalance in account_balance:
        if acbalance['asset'] == "USDT":
            balance_to = float(acbalance['balance'])
            balance = round(balance_to, 2)

    time = datetime.datetime.utcnow()
    year = str(time.year)
    month = str(time.month)
    day = str(time.day)
    time_fr = year+"-"+month+"-"+day
    time_fr_pt = datetime.datetime.strptime(time_fr, '%Y-%m-%d')    
    df = pd.read_csv('csv_files/balances.csv')
    last_time = datetime.datetime.strptime(df['time'].values[-1], '%Y-%m-%d')


    if time_fr_pt > last_time:
        miDato = [time_fr,balance]
        miArchivo = open('csv_files/balances.csv', 'a+')
        writer = csv.writer(miArchivo)
        writer.writerow(miDato)
        miArchivo.close()   

    else:
        pass
    
