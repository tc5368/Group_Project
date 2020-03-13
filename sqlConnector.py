import mysql.connector as mysql
from datetime import date
import pandas as pd
import pandas_datareader as web
import yfinance as yf 
from Stocks import db
from Stocks.models import *
from flask import flash

def get_Name(ticker):
	return(yf.Ticker(ticker).info['longName'])

def get_Info(ticker):
	return(yf.Ticker(ticker).info['longBusinessSummary'])

def get_raw_info(stock_ticker):
	'''Get a csv file for the past data of a given stock
	
	Takes the stocks ticker and then will create a data frame of the stock but without the Adj Close or Volume
	
	Arguments:
		stock_ticker {[String]} -- [4 Character unique identifier for the stock]
	'''

	#add validation later
	if stock_ticker != "Invalid":
		
		df = web.DataReader(stock_ticker,"yahoo")
		del (df['Volume'], df['Adj Close'])
		return df

	else:
		return None


def make_new_hist(ticker):
	ticker = ticker.upper()
	df = get_raw_info(ticker)
	if df is None:
		None
		#this should flash that stock dosen't exsist.
		
	else:
		make_new_stock_history_table(ticker,df)


def make_new_stock_history_table(ticker, df):
	'''Add a given stocks data to the Database

	Arguments:
		stock_name {String} -- 4 character string unique to the stock
		df {pandas dataframe} -- raw infomation of the stock's history.
	'''

	tables = db.engine.table_names()
	if ticker+"_HIST" in tables:
		flash("Stock already being tracked")
	else:
		query = ("""CREATE TABLE `c1769261_Second_Year`.`"""+ticker+"""_HIST` (
												`Date` DATE NOT NULL,
												`Open` DOUBLE NOT NULL,
												`High` DOUBLE NOT NULL,
												`Close` DOUBLE NOT NULL,
												`Low` DOUBLE NOT NULL,
												PRIMARY KEY (`Date`));""")
		execute_query(query)
		df['Date'] = df.index.map(lambda x: x.strftime('%Y-%m-%d'))
		df.to_sql(name=ticker+'_HIST', con=db.engine, index=False, if_exists='append')
		
		newEntry = Stock_Info(ticker,get_Name(ticker),float(df['Close'].iloc[-1]),ticker+'_HIST')
		db.session.add(newEntry)
		db.session.commit()



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


def check_buy(user_id, stock, amount):
	amount = float(amount)
	user = User.query.filter_by(id=user_id).first()

	# get * from stock info. if stock in stock_info then continues
	# else try and run make_new_hist() on the stock.

	# the track function will return it dosen't exsist for you here.

	stock_info = Stock_Info.query.filter_by(Stock_ID=stock).first()
	if stock_info != None and (amount > 0):
		price = float(amount) * stock_info.Current_Price
		#print('%s is trying to buy %s shares of %s stock at price %s, totaling %s' %(user.first_name,amount,stock,stock_info.Current_Price, float(amount)*float(stock_info.Current_Price)))
		#print('Their balance is %s' %(user.balance))

		if user.balance >= price:
			user.balance -= price

			portfolio = Portfolio.query.filter_by(Customer_ID = user_id).all()
			found = False
			for i in portfolio:
				if i.Stock_ID == stock_info.Stock_ID:
					i.Amount_of_Shares += float(amount)
					found = True
					break

			if found == False:
				newEntry = Portfolio(user.id,stock_info.Stock_ID,float(amount))
				db.session.add(newEntry)

			db.session.commit()
			return True
	else:
		print('Could not find',stock)

def check_sell(user_id, stock, amount):
	amount = float(amount)
	user = User.query.filter_by(id=user_id).first()
	stock_info = Stock_Info.query.filter_by(Stock_ID=stock).first()

	if stock_info != None and (amount > 0):
		price = float(amount) * stock_info.Current_Price
		#print('%s is trying to buy %s shares of %s stock at price %s, totaling %s' %(user.first_name,amount,stock,stock_info.Current_Price, float(amount)*float(stock_info.Current_Price)))
		#print('Their balance is %s' %(user.balance))

		portfolio = Portfolio.query.filter_by(Customer_ID = user_id).all()
		found = False
		for i in portfolio:
			if i.Stock_ID == stock_info.Stock_ID:
				if i.Amount_of_Shares >= amount:
					i.Amount_of_Shares -= amount
					user.balance += price
				found = True
				break

		if found == False:
			return False

		db.session.commit()
		return True
	else:
		print('Could not find',stock)


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

