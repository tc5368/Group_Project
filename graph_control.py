
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

style.use('ggplot')

def get_graph(stock_name):
	start = dt.datetime(2019,10,17)
	end = dt.datetime(2019,10,25)

	l_start = dt.datetime(2009,10,17)
	l_end = dt.datetime(2019,10,25)

	df = web.DataReader(stock_name, 'yahoo',start,end)
	large_df = web.DataReader(stock_name, 'yahoo',l_start,l_end)

	while True:
		try:
			print('Still early prototype all graph figures are in dollars')
			choice = input('Last week\'s figures or last 10 years ? [w/y]\n>> ')
			if choice == 'w':
				ax1 = df['Adj Close'].plot()
				plt.suptitle('Past Week')
				plt.show()
				break
			elif choice == 'y':
				ax2 = large_df['Adj Close'].plot()
				plt.suptitle('Past 9 years')
				plt.show()
				break
			else:
				print('Invalid Option')
		except:
			print('Invalid Option')

	
