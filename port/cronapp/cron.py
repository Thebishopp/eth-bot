
#### IMPORTACION DE LIBRERIAS
import sqlite3 as sql
from time import sleep
import numpy as np
import pandas as pd
import yfinance as yf


#PARAMETROS INICALES
inventario = [1988, 1988, 1988, 1988, 1988, 1988]
#INICIO DE LOOP
while True:
        #conexión al a base de datos
        con = sql.connect('./stocks.db')
        cur = con.cursor()
        #Selecionamos el último registro de balance, si esta vacío se inicia con un defecto de $100.000
        ult_balance = cur.execute(
            "SELECT balance FROM transacciones ORDER BY time DESC LIMIT 1").fetchone()
        if not ult_balance:
            balance = 100000
        else:            
            log = open('log.txt', 'a')
            log.write('done \n')
            log.close()
            balance = ult_balance[0]
        
        #Selecionamos la última compra realiazada para obtener precio de referencia
        q_primer_item = cur.execute(
        "SELECT p_compra FROM transacciones ORDER BY time DESC LIMIT 1").fetchone()
        #Consultamos a la API por el precio en vivo
        try:
            data = yf.download(tickers='ETH-USD', period='1d', interval='5m', prepost=True)
            print('############INICIO###########')
            #Tomamos el precio a la baja para la compra y el precio al alza para la compra
            compra = data["Low"].iloc[-1]
            venta = data["High"].iloc[-1]
            ult_compra = data["Low"].iloc[-2]
            print("PRECIO HIGH: %s" % venta)
            print("Precio LOW: %s" % compra)
            print(compra/venta)
            print("INVENTARIO: %s" % inventario)
            inventario.sort()
        except:
            print('Fallo en consultar a la API')
            sleep(30)

        #Iteramos por nuestra cartera
        for i in inventario:
                    print(i/venta)
                    print(inventario)
    #Si la diferencia entre el precio de venta y el precio de nuestra cartera es mayor o igual a 10 hacemos una venta
                    if (venta - i) >= 10:
                        print('######PASO VENTA:##############')
                        inventario.remove(i)
                        print(inventario)
                        balance = balance + venta
                        print("Venta realiazada!: +%s Balance: %s" % (i, balance))
                        #Insertamos la transacción en la base de datos
                        cur.execute("""INSERT INTO transacciones VALUES(CURRENT_TIMESTAMP, '{0}', {1}, {2}, {3})""".format('venta', venta, i, balance))
                        con.commit()
                #Si el inventario esta vacío, realiza una compra
                    if not inventario:
                            print('######PASO COMPRA:##############')
                            inventario.append(compra)
                            print("Compra realiazada!222: %s" % compra)
                            print(inventario)
                            balance = balance - compra
                            cur.execute("""INSERT INTO transacciones
                            VALUES(CURRENT_TIMESTAMP, '%s', %s, %s, %s)""" % ("compra", compra, compra, balance))
                            #Insertamos la transacción en la base de datos
                            con.commit()
                        
                #Si el precio de compra esta por debajo de $5 o más realizamos una compra
                    inventario.sort()
                    if (inventario[0] - compra) <= 5 and len(inventario) <= 5:
                                print('######PASO COMPRA:##############')
                                inventario.append(compra)
                                print("Compra realiazada!: %s" % compra)
                                print(inventario)
                                balance = balance - compra
                                cur.execute("""INSERT INTO transacciones
                                VALUES(CURRENT_TIMESTAMP, '%s', %s, %s, %s)""" % ("compra", compra, compra, balance))
                                #Insertamos la transacción en la base de datos
                                con.commit()
                    else:
                        print('Cartera: %s' % inventario)
                    inventario.sort()
                    print('Balance: %s' % balance)
                    
                    sleep(5)
                            

                        