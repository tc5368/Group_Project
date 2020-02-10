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


def get_history(stock_ticker):
	"""Will return the result of running a select * from the the history table of the given stock.
	
	Arguments:
		stock_ticker {[String]} -- 4 character unique identifier for a stock
	"""
	if (len(stock_ticker) == 4 and stock_ticker.isalpha()):

		#This if statment will be replaced, instead it will do a different cursor
		#select to find out if stock_id in Stock_Info then will pull the data.

		query = ("SELECT Date, High, Low, Open ,Close FROM "+stock_ticker.upper()+"_HIST")
		data = execute_query(query)

		df = pd.DataFrame.from_records(data)
		df.columns = ['Date','High','Low','Open','Close']
		return(df)
	
	else:
		print('Invalid Name')
		return None




def make_new_stock_history_table(df):
	None



if __name__ == '__main__':
	df = get_history('tsla')
	print(df)








