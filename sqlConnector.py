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

	# Here is very basic error checking for sql injecttion.
	# This needs work to make it more sophisticated also should be chaged so
	# that these checks are made when the input is taken and not here.


	# I cant test this but it should work if there is an error it will be here just comment it out
	# Inbetween these 2 comments is untested
	dangerWords = ['DROP','DELETE']
	for i in dangerWords:
		if i in query.upper():
		print('SQL injection detected with query: %s' %query)
		return None
	# Inbetween these 2 comments is untested


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
			newHistoryEntry = History(user.id,datetime.now(),stock_info.Stock_ID,float(stock_info.Current_Price * amount),float(amount), "Buy")
			db.session.add(newHistoryEntry)

			for i in portfolio:
				if i.Stock_ID == stock_info.Stock_ID:
					# Growing the price of the stock.
					growth = r.random()/100
					growth = 1 + growth
					stock_info.Current_Price = stock_info.Current_Price * growth

					i.Amount_of_Shares += float(amount)
					i.Spend += (stock_info.Current_Price * amount)
					found = True
					break
			if found == False:
				newEntry = Portfolio(user.id,stock_info.Stock_ID,float(amount),float(stock_info.Current_Price * amount))
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
		newHistoryEntry = History(user.id,datetime.now(),stock_info.Stock_ID,float(stock_info.Current_Price * amount),float(amount), "Sell")
		db.session.add(newHistoryEntry)
		for i in portfolio:
			if i.Stock_ID == stock_info.Stock_ID:
				if i.Amount_of_Shares >= amount:
					# Decreasing the price of the stock.
					growth = r.random()/100
					growth = 1 - growth
					stock_info.Current_Price = stock_info.Current_Price * growth

					i.Amount_of_Shares -= amount
					i.Spend -= (stock_info.Current_Price * amount)
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
		# Updating the Stock_Info table's current prices
		growth = r.random()/100
		trade_type = ["buy", "sell"]
		if r.choice(trade_type) == "buy":
			growth = 1 + growth
		else:
			growth = 1 - growth
		stock.Current_Price = stock.Current_Price * growth
		db.session.commit()
		# Updating the HIST table each stock's OHLC values

		#always reaching this point
		query = "SELECT * FROM " + stock.Stock_Table + " ORDER BY Date DESC LIMIT 1"
		curr_day = execute_query(query)
		curr_price = str(stock.Current_Price)

		# If new day, fill in the OHL
		#If high = None
		if curr_day[0][2] == None:
			update_curr_day = "UPDATE " + stock.Stock_Table + " SET Open = " + curr_price + ", High = " + curr_price + ", Low = " + curr_price + " WHERE Date = '" + str(curr_day[0][0]) + "'"
			execute_query(update_curr_day)

			query = "SELECT * FROM " + stock.Stock_Table + " ORDER BY Date DESC LIMIT 1"
			curr_day = execute_query(query)

		# Else, when the data is already in the table
		else:
			high = curr_day[0][2]
			low = curr_day[0][4]

			if stock.Current_Price >= high:
				update_higher = "UPDATE " + stock.Stock_Table + " SET High = " + curr_price + " WHERE Date = '" + str(curr_day[0][0]) + "'"
				execute_query(update_higher)

			elif stock.Current_Price <= low:
				update_lower = "UPDATE " + stock.Stock_Table + " SET Low = " + curr_price + " WHERE Date = '" + str(curr_day[0][0]) + "'"
				execute_query(update_lower)
	check_automated_strategies()


def check_automated_strategies():
	users_with_strategies = Automation.query.order_by(Automation.Customer_ID).all()
	for user in users_with_strategies:
		s = Automation.query.filter_by(Customer_ID = user.Customer_ID).first()
		stock_info = Stock_Info.query.filter_by(Stock_ID=s.Stock_ID).first()
		if (s.Trigger == 'A' and stock_info.Current_Price > s.Trigger_Price) or (s.Trigger == 'B' and stock_info.Current_Price < s.Trigger_Price):
			#print('Automation is %s ing %s shares of %s for user %s' %(s.Strategy, s.Increment, stock_info.Stock_Name ,s.Customer_ID))
			if s.Limit == None:
				if s.Strategy == 'B':
					check_buy (s.Customer_ID, s.Stock_ID, s.Increment)
				else:
					check_sell(s.Customer_ID, s.Stock_ID, s.Increment)

			elif s.Limit - s.Increment >= 0:
				if s.Strategy == 'B':
					check_buy (s.Customer_ID, s.Stock_ID, s.Increment)
				else:
					check_sell(s.Customer_ID, s.Stock_ID, s.Increment)
				newValue = s.Limit - s.Increment
				s.Limit = newValue
			else:
				db.session.delete(s)
			db.session.commit()

def add_new_automated_strategy(user, form):
	# need to add test to make the user track a stock before it can be automated.
	test = Automation.query.filter_by(Customer_ID = user).all()
	for i in test:
		if form.ticker.data == i.Stock_ID:
			return False
	if form.limit.data == None:
		limit = 'null'
	else:
		limit = '"'+str(form.limit.data)+'"'
	query = """INSERT INTO `c1769261_Second_Year`.`Automation` (`Customer_ID`, `Stock_ID`, `Trigger`, `Trigger_Price`, `Strategy`, `Increment`, `Limit`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s);""" %(user, form.ticker.data, form.trigger.data, form.trigger_price.data, form.strategy.data, form.increment.data, limit)
	execute_query(query)
	return True

	#add validation here
	#also add delete functionaility.

def getStratergies(id):
	stategies = Automation.query.filter_by(Customer_ID = id).all()
	return stategies

def removeStrategy(ticker, id):
	toRemove = Automation.query.filter_by(Customer_ID = id, Stock_ID = ticker).delete()
	db.session.commit()



def time_decode(dateObj):
	y,m,d = str(dateObj.year),str(dateObj.month),str(dateObj.day)
	if len(d) == 1:
		d = '0'+d
	if len(m) == 1:
		m = '0'+m
	return y,m,d


def new_day():
	t = date.today()
	y,m,d = time_decode(t)

	history_tables = find_avaliable()
	if history_tables[0] != None:
		for i in history_tables:
			i = str(i)

			stock_info = Stock_Info.query.filter_by(Stock_ID=i.split('_')[0]).first()
			price      = str(stock_info.Current_Price)

			#Add validation to this to see if there is already an entry for this date

			query = "SELECT * FROM "+ i + " WHERE (Date = '"+y+"-"+m+"-"+d+"' )"
			data = execute_query(query)
			if data == []:

				query = "INSERT INTO `c1769261_Second_Year`.`"+i+"` (`Date`) VALUES ('"+y+"-"+m+"-"+d+"');"
				execute_query(query)

			query = "SELECT * FROM "+ i + " ORDER BY Date DESC LIMIT 2"
			data = execute_query(query)
			last_full_row = data[1]

			y2,m2,d2 = time_decode(last_full_row[0])
			query = "UPDATE `c1769261_Second_Year`.`"+i+"` SET `Close` = '"+price+"' WHERE (`Date` = '"+y2+"-"+m2+"-"+d2+"');"
			execute_query(query)


def find_tickers(inp):
	inp = inp.capitalize()
	tickers = web.get_nasdaq_symbols()
	return tickers.index[tickers['Security Name'].str.contains(inp)].tolist()
