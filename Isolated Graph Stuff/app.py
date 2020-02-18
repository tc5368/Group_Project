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
# Sql
from sqlConnector import get_history

server = Flask(__name__)


@server.route('/')
def index():
    return "<a class='nav-item nav-link' href='/matplot'>Show Matplotlib Graph</a> <a class='nav-item nav-link' href='/dash/'>Show Plotly Graph</a>"

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

@server.route('/matplot')
def matplot():
    """ Creates a matplotlib graph using ohlc every 10 days of the stock price. Plots date on the x axis and stock value on the y axis. After, the figure is converted into html.

    Returns
    -------
    string
        A block of html & javascript code that will display an interactive graph.

    """
    style.use('ggplot')
    f = figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
    # Converting index into datetime format
    stock_name = 'nvda'
    df = get_history(stock_name)
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index)

    df_ohlc = df['Close'].resample('10D').ohlc()
    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1)
    ax1.xaxis_date()
    candlestick_ohlc(ax1, df_ohlc.values, width=4, colorup='g')
    html_graph = mpld3.fig_to_html(f, figid="matplot_graph")
    return html_graph

# Uses Flask as the server and dash as the app that connects to the server and works together.
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

# Generates HTML on the dash page and embeds a template of the graph and a dropdown list.
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''Dash: A web application framework for Python.'''),
    dcc.Graph(id='plotly_fig', figure=fig),
    dcc.Dropdown(
        id      ='stock_dropdown',
        options =[{'label': i, 'value': i} for i in stock_list],
        value   =stock_list[0],
        style   ={"max-width": "200px", "margin": "auto"}
    )
],
style={"max-width": "1000px", "margin": "auto"})

# Will wait for the user to select anything on the dropdown menu and output the result on the graph.
@app.callback(
    Output('plotly_fig', 'figure'),
    [Input('stock_dropdown', 'value')]
)
def update_figure(selected_stock):
    """Will show different graphs on the figure, depending on what the user selects. Will be called every single time the user changes value on the dropdown list.

    Parameters
    ----------
    selected_stock : string
        The value selected in the dropdown list.

    Returns
    -------
    figure
        Return the figure type information in an array with the new read figure data.

    """
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
