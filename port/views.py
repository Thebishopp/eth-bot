from datetime import datetime
from pipes import Template
from django.shortcuts import render
from django.http import HttpResponse
import sqlite3 as sql
import pandas as pd
# Import mimetypes module
import mimetypes
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = 'plotly_dark'
pio.templates["plotly_dark_custom"] = pio.templates["plotly_dark"]
# import os module
import os

import plotly
def indice(request):
    con = sql.connect('stocks.db')
    df = pd.read_sql_query('select * from transacciones ORDER BY time', con)
    print(df)
    # doc = open('/template_bot.html')
    # plt = Template(doc.read())
    # doc.close()
    # ctx = Context({df})
    df = df.iloc[-5:]
    df.columns = ['time', 'accion', 'precio compra', 'precio venta', 'balance']
    df.reset_index(drop=True, inplace=True)
    dataframe = df.to_html(index=False, justify='center')
    plot = df = pd.read_sql("""SELECT * from transacciones""", con)
    df = df.iloc[70:]
    fig = px.line(df, x='time', y='balance', width=800, height=600)
    fig2 = px.scatter(df, x='time', y='p_venta', width=800, height=600)
    plut = plotly.offline.plot(fig, filename = 'filename.html', auto_open=False)
    read_grafico = open('filename.html', 'r')
    html = """"
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
  padding: 25px;
  background-color: black;
  color: white;
  font-size: 25px;
}
</style>
</head>
<body>
 <div style="width:800px; margin:0 auto;">
 <h1>ETH  Bot</h1>
 <p>Bot que compra y vende Ethereum, analizando su precio</p>
 %s
 %s
 </div>
 </body>
<div class="tradingview-widget-container">
  <div id="tradingview_c04cc"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/chart/3HAVMXiE/?symbol=ETH" rel="noopener" target="_blank"><span class="blue-text">ETH/USD Chart</span></a> by TradingView</div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {
  "width": 980,
  "height": 610,
  "symbol": "ETHUSD",
  "interval": "60",
  "timezone": "Etc/UTC",
  "theme": "dark",
  "style": "1",
  "locale": "en",
  "toolbar_bg": "#f1f3f6",
  "enable_publishing": false,
  "hide_side_toolbar": false,
  "allow_symbol_change": true,
  "container_id": "tradingview_e6bca"
}
  );
  </script>
</div>
</html> 
    """ % (dataframe, read_grafico.read())
    return HttpResponse(html)

def download(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = '/source_code.rar'
    # Define the full file path
    filepath = BASE_DIR + filename
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    response = HttpResponse(path, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response
