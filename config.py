from binance.client import Client

API_KEY = ""
API_SECRET = ""

client = Client(API_KEY, API_SECRET, tld='com')

SYMBOL = "SRMUSDT"
symbol_form = "SRM/USDT"
QUANTITY = 5
BALANCE_START = 45.00
leverage = 20
percentage = 0.15

client.futures_change_leverage(symbol = SYMBOL, leverage = leverage)


exInfo = client.futures_exchange_info()
symbolsExInfo = exInfo['symbols']
for simbolo in symbolsExInfo:
    if simbolo['symbol'] == SYMBOL:
        quantityPrecision = simbolo['quantityPrecision']
        pricePrecision = simbolo['pricePrecision']

name = "Miguel Payá"
