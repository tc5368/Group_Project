import mysql.connector
from datetime import date
import pandas as pd

def get_history(stock_ticker):
	"""Will return the result of running a select * from the the history table of the given stock.
	
	Arguments:
		stock_ticker {[String]} -- 4 character unique identifier for a stock
	"""
	if (len(stock_ticker) == 4 and stock_ticker.isalpha()):

		#This if statment will be replaced, instead it will do a different cursor
		#select to find out if stock_id in Stock_Info then will pull the data.

		cnx = mysql.connector.connect(user='c1769261', password='apmWzUswLy6LvfX', host='csmysql.cs.cf.ac.uk', database='c1769261_Second_Year')
		
		cursor = cnx.cursor()
		query = ("SELECT Date, High, Low, Open ,Close FROM "+stock_ticker.upper()+"_HIST")
		cursor.execute(query)

		data = cursor.fetchall()
		cnx.close()

		df = pd.DataFrame.from_records(data)
		df.columns = ['Date','High','Low','Open','Close']
		return(df)
	
	else:
		print('Invalid Name')
		return None


if __name__ == '__main__':
	get_history('tsla')