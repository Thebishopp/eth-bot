import sqlite3 as sql
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
# # (
# #     time timestamp,
# #     p_accion varchar,
# #     p_compra float,
# #     p_venta float,
# #     balance float
# #     )

con = sql.connect('./stocks.db')
cur = con.cursor()