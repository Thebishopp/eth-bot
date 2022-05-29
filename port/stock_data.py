
# Raw Package
# base de datos
import sqlite3 as sql
from time import sleep

import numpy as np
import pandas as pd
import plotly.graph_objs as go
# Data Source
import yfinance as yf

# DB


def stock_bot():
    con = sql.connect('./stocks.db')
    cur = con.cursor()

    balance = 100000
    ult_balance = cur.execute(
        "SELECT balance FROM transacciones ORDER BY time DESC LIMIT 1").fetchone()
    if ult_balance[0] < 100000 or ult_balance[0] is None:
        balance = 100000
    else:
        balance = ult_balance[0]
    inventario = []
    q_primer_item = cur.execute(
        "SELECT p_compra FROM transacciones ORDER BY time DESC LIMIT 1").fetchone()
    primer_item = inventario.append(q_primer_item[0])
    print(len(inventario))
    data = yf.download(tickers='JPM', period='1d', interval='5m')
    ante_precio = data["High"].iloc[-2]
    ult_precio = data["Low"].iloc[-1]
    print("PRECIO ACTUAL: %s" % ult_precio)
    if len(inventario) == 0 or (ante_precio/ult_precio) <= 0.95:
            inventario.append(ult_precio)
            print("Compra realiazada!: %s" % ult_precio)
            print(inventario)
            balance = balance - ult_precio
            cur.execute("""INSERT INTO transacciones(p_compra, p_accion, balance)
            VALUES(%s, %s, %s)""" % (ult_precio, ult_precio, balance))
    else:
        with open('log.txt', 'w') as a:
            a.write('done /n')
            
            for i in inventario:
                pass
                if (i/ante_precio) >= 1.1:
                    ult_compra = primer_item.fetchone()
                    ult_compra = ult_compra.fetchone()
                    inventario.remove(i)
                    print(inventario)
                    balance = balance + i
                    print("Venta realiazada!: +%s Balance: %s" % (i, balance))
                    cur.execute("""INSERT INTO transacciones (p_compra, p_accion, p_venta, balance)
                    VALUES(%s, %s, %s, %s)
                        """) % (ult_compra, ult_precio, i, balance)
                else:
                    print(balance)
    return 

# stock_bot()


# #declare figure
# fig = go.Figure()

# #Candlestick
# fig.add_trace(go.Candlestick(x=data.index,
#                 open=data['Open'],
#                 high=data['High'],
#                 low=data['Low'],
#                 close=data['Close'], name = 'market data'))

# # Add titles
# fig.update_layout(
#     title='JPM live share price evolution',
#     yaxis_title='Stock Price (USD per Shares)')

# # X-Axes
# fig.update_xaxes(
#     rangeslider_visible=True,
#     rangeselector=dict(
#         buttons=list([
#             dict(count=15, label="15m", step="minute", stepmode="backward"),
#             dict(count=45, label="45m", step="minute", stepmode="backward"),
#             dict(count=1, label="HTD", step="hour", stepmode="todate"),
#             dict(count=3, label="3h", step="hour", stepmode="backward"),
#             dict(step="all")
#         ])
#     )
# )

# #Show
# fig.show()
