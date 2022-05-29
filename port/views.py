from datetime import datetime
from django.http import HttpResponse
import sqlite3 as sql
from port.stock_data import stock_bot
from multiprocessing import Pool
def indice(request):
    con = sql.connect('stocks.db')
    cur = con.execute('select * from transacciones ORDER BY time DESC limit 1')
    data = cur.fetchone()
    print(data[-2])
    a = data[-2]
    return HttpResponse('%s' %  data[-2])
