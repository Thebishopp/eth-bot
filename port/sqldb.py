import sqlite3 as sql
import yfinance as yf

# (
#     time timestamp,
#     p_accion varchar,
#     p_compra float,
#     p_venta float,
#     balance float
#     )

con = sql.connect('./stocks.db')
cur = con.cursor()
# cur.execute(""" CREATE TABLE transacciones
#             (time timestamp,
#             accion string,
#             p_compra float,
#             p_venta float,
#             balance float)
#             """)

# b = cur.execute("""INSERT INTO transacciones
#           VALUES(CURRENT_TIMESTAMP, 'test',5, 5,100000)""")
# print(b)
query = cur.execute('''select * from transacciones''')
con.commit()

a = query.fetchall()
print(a)
con.close()

data = yf.download(tickers='JPM', period='1d', interval='5m')
print(data)
data.to_csv("asd.csv")
ante_precio = data["Close"].iloc[-2]
ult_precio = data["Close"].iloc[-1]
print('Ante Precio: %s' % ante_precio)
print('ult_precio: %s' % ult_precio)