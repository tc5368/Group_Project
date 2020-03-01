import mysql.connector as mysql
from datetime import date
import pandas as pd





def execute_query(query):
	'''Executes SQL statments

	Takes a query and then makes a connection to the SQL server, it will then execute that statment
	Arguments:
		query {String} -- A valid SQL statment that can be run on current permissions.

	Returns:
		[Pandas Dataframe] -- This is used only for select statments will return the results from the sql select into a data frame.
	'''
	cnx = mysql.connect(user='c1769261',
						password='apmWzUswLy6LvfX',
    						host='csmysql.cs.cf.ac.uk',
						database='c1769261_Second_Year')
	cursor = cnx.cursor()
	cursor.execute(query)
	data = cursor.fetchall()
	cnx.close()

	return data

def get_all_stocks():
	"""Will return a list of stock history tables.
	Returns
    -------
    array
        A list of available stock history tables that can be used to query.
	"""
	query = ("SHOW TABLES")
	cnx = mysql.connect(user='c1769261',
						password='apmWzUswLy6LvfX',
						host='csmysql.cs.cf.ac.uk',
						database='c1769261_Second_Year')
	cursor = cnx.cursor()
	cursor.execute(query)
	tables = cursor.fetchall()
	cnx.close()

	stock_list = []
	for table in tables:
		curr_table = table[0]
		if curr_table.endswith("_HIST"):
			stock_list.append(curr_table[:-5])
	return stock_list

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




def make_new_stock_history_table(stock_name, df):
	'''Add a given stocks data to the Database

	Arguments:
		stock_name {String} -- 4 character string unique to the stock
		df {pandas dataframe} -- raw infomation of the stock's history.
	'''
	query = ("""CREATE TABLE `c1769261_Second_Year`.`"""+stock_name+"""_HIST` (
  											`Date` DATE NOT NULL,
											`Open` DOUBLE NOT NULL,
											`High` DOUBLE NOT NULL,
											`Close` DOUBLE NOT NULL,
											`Low` DOUBLE NOT NULL,
											PRIMARY KEY (`Date`));""")
	execute_query(query)

	#This currently works but dosen't do anything with the data.
	#Need to convert the whole system to using SQL Alchemy and not using mysql
