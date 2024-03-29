from binance.client import Client
from binance.enums import *
import pandas as pd
import datetime
import json, ccxt, csv

SYMBOL = "SRMUSDT"
symbol_form = "SRM/USDT"

client = Client(API_KEY, API_SECRET, tld='com')

exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    },
})

exchange.load_markets()

transaction = client.futures_account_trades(symbol = SYMBOL)
print(transaction)
# Add orders
order = client.futures_get_all_orders(symbol = SYMBOL)

        


# exchange = ccxt.binance({
#     'apiKey': API_KEY,
#     'secret': API_SECRET,
#     'enableRateLimit': True,
#     'options': {
#         'defaultType': 'future'
#     },
# })

