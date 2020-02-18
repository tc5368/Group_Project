from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
#https://mpld3.github.io/quickstart.html for mpld3 matplotlib to html
import matplotlib.pyplot as plt, mpld3
from matplotlib.pyplot import figure

from sqlConnector import get_history
stock_name = 'nvda'

style.use('ggplot')
f = figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')

# Converting index into datetime format
df = get_history(stock_name)
df = df.set_index('Date')
df.index = pd.to_datetime(df.index)

df_ohlc = df['Close'].resample('10D').ohlc()
df_ohlc.reset_index(inplace=True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1)
ax1.xaxis_date()
candlestick_ohlc(ax1, df_ohlc.values, width=4, colorup='g')


mpld3.show()
