import pandas as pd
from sqlConnector import get_history
import plotly.graph_objs as go

stock_name = 'AAPL'

def main(stock_name):
	'''Generates Stock Graph
	
	Will utilise the sqlConnector code to pull a given stocks history from the database and then use
	and ohlc library to plot that data in a ohcl graph.
	
	Arguments:
		stock_name {[String} -- 4 character String unique to the Stock
	'''

	df = get_history(stock_name)

	fig = go.Figure(data=go.Ohlc(x=df['Date'],
					open=df['Open'],
					high=df['High'],
					low=df['Low'],
					close=df['Close']))
	fig.show()



if __name__ == '__main__':
	main(stock_name)