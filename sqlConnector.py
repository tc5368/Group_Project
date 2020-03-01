import mysql.connector as mysql
from datetime import date
import pandas as pd
import pandas_datareader as web
from Stocks import db

def get_raw_info(stock_ticker):
	'''Get a csv file for the past data of a given stock
	
	Takes the stocks ticker and then will create a data frame of the stock but without the Adj Close or Volume
	
	Arguments:
		stock_ticker {[String]} -- [4 Character unique identifier for the stock]
	'''

	#add validation later
	if stock_ticker != None:
		
		df = web.DataReader(stock_ticker,"yahoo")
		del (df['Volume'], df['Adj Close'])
		return df

	else:
		return None


def make_new_hist(ticker):
	ticker = ticker.upper()
	df = get_raw_info(ticker)
	make_new_stock_history_table(ticker,df)


def make_new_stock_history_table(ticker, df):
	'''Add a given stocks data to the Database

	Arguments:
		stock_name {String} -- 4 character string unique to the stock
		df {pandas dataframe} -- raw infomation of the stock's history.
	'''
	query = ("""CREATE TABLE `c1769261_Second_Year`.`"""+ticker+"""_HIST` (
  											`Date` DATE NOT NULL,
											`Open` DOUBLE NOT NULL,
											`High` DOUBLE NOT NULL,
											`Close` DOUBLE NOT NULL,
											`Low` DOUBLE NOT NULL,
											PRIMARY KEY (`Date`));""")
	execute_query(query)

	print(df)
	df['Date'] = df.index.map(lambda x: x.strftime('%Y-%m-%d'))
	print(df)

	df.to_sql(name=ticker+'_HIST', con=db.engine, index=False, if_exists='append')



def execute_query(query):
	'''Executes SQL statments

	Takes a query and then makes a connection to the SQL server, it will then execute that statment
	Arguments:
		query {String} -- A valid SQL statment that can be run on current permissions.

	Returns:
		[Pandas Dataframe] -- This is used only for select statments will return the results from the sql select into a data frame.
	'''
	cnx = mysql.connect(user     = 'c1769261',
						password = 'apmWzUswLy6LvfX',
    						host = 'csmysql.cs.cf.ac.uk',
						database = 'c1769261_Second_Year')
	cursor = cnx.cursor()
	cursor.execute(query)
	try:
		data = cursor.fetchall()
	except:
		data = None
	cnx.close()

	return data
















def get_history(stock_ticker):
	"""Will return the result of running a select * from the the history table of the given stock.

	Arguments:
		stock_ticker {[String]} -- 4 character unique identifier for a stock followed by _HIST
	"""

	#This if statment will be replaced, instead it will do a different cursor
	#select to find out if stock_id in Stock_Info then will pull the data.

	query = ("SELECT Date, High, Low, Open ,Close FROM "+stock_ticker)
	try:
		data = execute_query(query)
	except:
		data = None

	df = pd.DataFrame.from_records(data)
	df.columns = ['Date','High','Low','Open','Close']
	return(df)

