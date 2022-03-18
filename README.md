# base-cw-bot
## TODO

First install all the packages of requirements.txtpi

Add one line to transactions.csv and orders.csv
ORDERS
```
ordenes = client.futures_get_all_orders(symbol = SYMBOL)
for i in range(20):
    if ordenes[-i]['type'] == 'STOP_MARKET':
        order_id = ordenes[-i]['orderId']
        position_side = ordenes[-i]['positionSide']
        status = ordenes[-i]['status']
        stop_price = ordenes[-i]['stopPrice']
        time = ordenes[-i]['time']
        date = pd.to_datetime(time, unit='ms')

        miDato = [order_id,position_side,status,stop_price,date]
        miArchivo = open('csv_files/orders.csv', 'a+')
        writer = csv.writer(miArchivo)
        writer.writerow(miDato)
        miArchivo.close() 
```

TRANSACTIONS

```
transactions = client.futures_account_trades()
for i in range(5):
    if transactions[-i]['symbol'] == "SRMUSDT":        
        transaction_id = transactions[-i]['orderId']
        side = transactions[-i]['side']
        price = transactions[-i]['price']
        quantity = transactions[-i]['qty']
        commission = transactions[-i]['commission']
        position_side = transactions[-i]['positionSide']
        time = transactions[-i]['time']
        date = pd.to_datetime(time, unit='ms')

        miDato = [transaction_id,side,price,quantity,commission,position_side,time]
        miArchivo = open('csv_files/transactions.csv', 'a+')
        writer = csv.writer(miArchivo)
        writer.writerow(miDato)
        miArchivo.close() 
```

Crear bd para logs
Ver que funciona sin problemas el añadir datos a cualquier bd