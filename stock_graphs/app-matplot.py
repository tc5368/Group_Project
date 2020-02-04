from flask import Flask
# Matplotlib Graph
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt, mpld3
from matplotlib.pyplot import figure

app = Flask(__name__)


@app.route('/')
def index():
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
