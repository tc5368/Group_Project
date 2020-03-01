
import pandas_datareader as web


def get_raw(stock_ticker):
	'''Get a csv file for the past data of a given stock
	
	Takes the stocks ticker and then will create a data frame of the stock but without the Adj Close or Volume
	
	Arguments:
		stock_ticker {[String]} -- [4 Character unique identifier for the stock]
	'''
	df = web.DataReader("tsla","yahoo")
	del (df['Volume'], df['Adj Close'])

	return df


def main(ticker):
	df = get_raw(ticker)
	



if __name__ == '__main__':
	main('UBER')