
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
        log = open('log.txt', 'a')
        log.write('done \n')
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        log.close()
        for i in inventario:
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