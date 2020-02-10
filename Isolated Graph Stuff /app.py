from flask import Flask, redirect, url_for
# Matplotlib Graph
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt, mpld3
from matplotlib.pyplot import figure
# Plotly and Dash import
import chart_studio.plotly as py
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import chart_studio
chart_studio.tools.set_credentials_file(username ='group13Yes', api_key='OspkIgNNW6CTIM7110px')
import pandas as pd
from datetime import datetime


server = Flask(__name__)


@server.route('/')
def index():
    return "<a class='nav-item nav-link' href='/matplot'>Show Matplotlib Graph</a> <a class='nav-item nav-link' href='/dash/'>Show Plotly Graph</a>"

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

@server.route('/matplot')
def matplot():
    style.use('ggplot')
    f = figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
    df = pd.read_csv('tsla.csv', parse_dates= True, index_col=0)
    df_ohlc = df['Close'].resample('10D').ohlc()
    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1)
    ax1.xaxis_date()
    candlestick_ohlc(ax1, df_ohlc.values, width=4, colorup='g')
    html_graph = mpld3.fig_to_html(f, figid="matplot_graph")
    return html_graph

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/',
    external_stylesheets=external_stylesheets
)

# Need to automate the filling of stock_list
stock_list = ['tsla', 'nvda']
df = pd.read_csv(stock_list[0]+'.csv', parse_dates= True)

# You can duplicate code and render this fig to get rid off empty figure when you reach the page.
fig = go.Figure()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''Dash: A web application framework for Python.'''),
    dcc.Graph(id='plotly_fig', figure=fig),
    dcc.Dropdown(
        id      ='stock_dropdown',
        options =[{'label': i, 'value': i} for i in stock_list],
        value   ='tsla',
        style   ={"max-width": "200px", "margin": "auto"}
    )
],
style={"max-width": "1000px", "margin": "auto"})

@app.callback(
    Output('plotly_fig', 'figure'),
    [Input('stock_dropdown', 'value')]
)
def update_figure(selected_stock):
    df = pd.read_csv(selected_stock+'.csv', parse_dates= True)
    fig = go.Figure(data=go.Ohlc(x=df['Date'],
                        open   = df['Open'],
                        high   = df['High'],
                        low    = df['Low'],
                        close  = df['Close']),
                        layout = go.Layout(
                        title  = go.layout.Title(text="Graph Showing " + selected_stock.upper() + " Stock Price History")
                        )
    )
    print(fig["layout"])
    return fig
