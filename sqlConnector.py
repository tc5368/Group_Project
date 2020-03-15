import mysql.connector as mysql
from datetime import date
import pandas as pd
import pandas_datareader as web
import yfinance as yf
from Stocks import db
from Stocks.models import *
from flask import flash
import random as r

def get_Name(ticker):
	return(yf.Ticker(ticker).info['longName'])

def get_Info(ticker):
	return(yf.Ticker(ticker).info['longBusinessSummary'])

def find_avaliable():
	stock_list     = db.engine.table_names()
	history_tables = []
	for i in stock_list:
		if i.endswith('_HIST'):
			history_tables.append(i)
	if history_tables == []:
		history_tables.append(None)
	return history_tables

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
	try:
		df = get_raw_info(ticker)
		make_new_stock_history_table(ticker,df)
		return True
	except:
		return False


def make_new_stock_history_table(ticker, df):
	'''Add a given stocks data to the Database

	Arguments:
		stock_name {String} -- 4 character string unique to the stock
		df {pandas dataframe} -- raw infomation of the stock's history.
	'''

	tables = db.engine.table_names()
	if ticker+"_HIST" in tables:
		flash("Stock already being tracked")
		raise Exception('Stock has been already tracked')
	else:
		query = ("""CREATE TABLE `c1769261_Second_Year`.`"""+ticker+"""_HIST` (
												`Date`  DATE NOT NULL,
												`Open`  DOUBLE,
												`High`  DOUBLE,
												`Close` DOUBLE,
												`Low`   DOUBLE,
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
		cnx.commit()
		data = None
	cnx.close()
	return data


def check_buy(user_id, stock, amount):
	user = User.query.filter_by(id=user_id).first()
	stock_info = Stock_Info.query.filter_by(Stock_ID=stock).first()
	if stock_info != None and (amount > 0):
		price = float(amount) * stock_info.Current_Price

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
	user = User.query.filter_by(id=user_id).first()
	stock_info = Stock_Info.query.filter_by(Stock_ID=stock).first()
	if stock_info != None and (amount > 0):
		price = float(amount) * stock_info.Current_Price

		portfolio = Portfolio.query.filter_by(Customer_ID = user_id).all()
		found = False
		for i in portfolio:
			if i.Stock_ID == stock_info.Stock_ID:
				if i.Amount_of_Shares >= amount:
					i.Amount_of_Shares -= amount
					user.balance += price
				else:
					return False
				break

		Portfolio.query.filter_by(Amount_of_Shares=0).delete()

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

def simulate_trading():
	stocks = Stock_Info.query.all()
	for stock in stocks:
		growth = r.random()/100
		trade_type = ["buy", "sell"]
		query = "SELECT * FROM " + stock.Stock_Table + " ORDER BY Date DESC LIMIT 1"
		data = execute_query(query)
		if r.choice(trade_type) == "buy":
			growth = 1 + growth
		else:
			growth = 1 - growth
		stock.Current_Price = stock.Current_Price * growth
		db.session.commit()
		# high = data[0][2]
		# low = data[0][4]
		# if curr_price >= high:
		# 	print("Higher")
		# elif curr_price <+ low:
		# 	print("Lower")

def new_day():
	print('All tables have been updated for the new day')
	t = date.today()
	y,m,d = str(t.year),str(t.month),str(t.day)
	if len(d) == 1:
		d = '0'+d
	if len(m) == 1:
		m = '0'+m

	history_tables = find_avaliable()
	for i in history_tables:
		query = "INSERT INTO `c1769261_Second_Year`.`"+i+"` (`Date`) VALUES ('"+y+"-"+m+"-"+d+"');"
		execute_query(query)

		#previous day set close to the current price
		#open high and low set to previous close & close is left blank


















