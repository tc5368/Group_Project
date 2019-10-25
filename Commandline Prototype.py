#Commandline application for Group 13's Project

#Evnetully thee sql will have something like this format
#user = [name,username,password,portfolio,balance]
#Username being primary key and then through agile develpoment will can move the password
#to a differnt database to make it more secure.

#Also this may not be needed as I may do it now but just in case this definitly won't be 
#how our users infomation will be stored.


#Requires pip installation of yahoo_fin, requests_html, pandas, forex-python


from csv_control import *
import subprocess as sp
import graph_control
from yahoo_fin import stock_info as si
from forex_python.converter import CurrencyRates

def find_user_type():
	while True:
		Login_or_create = str(input('Would you like to login or make new account [l/n]\n>>'))
		print(Login_or_create)
		if Login_or_create.lower() not in ['l','n']:		#Simple Command line interface, loops
			print('Invalid choice, please try again')		#until it gets a valid input from the user
		else:												#then it will either go to the login screen
			break											#or the create user screen
	if Login_or_create.lower() == 'l':
		print('Proceding to Login screen')
		return login()
	elif Login_or_create.lower() == 'n':
		print('Proceding to create user sceen')
		return create()

def get_info(name=0):
	#Simply takes the two inputs for now, no error checking (will obvisously change).
	while True:
		try:
			username = str(input('What is your username ?\n>> '))
			password = str(input('What is your password (not secure)?\n>> '))
			if name:
				name = str(input('What is your name ?\n>> '))
			break
		except:
			print('Sorry invalid please retry')
	if name:
		return username, password, name
	return username, password

def login():
	username, password = get_info()
	while True:
		try:
			info = get_info_from_csv(username)
			if info[2] == password:		#Check database to see is username[given_user_name] = password
				return username			#however for now just check the dictionary.
		except:
			print('Invalid login infomation please try again')
			username,password = get_info()

def create():
	username, password, name = get_info(True)
	add_user_to_csv([username,name,password,{},0])
	return username

def get_stock_price(stock_name, amount_of_shares):
	c = CurrencyRates()
	conversion = c.get_rate('USD','GBP')
	value = si.get_live_price(stock_name)
	return amount_of_shares * value * conversion

def buy_stock(stock_name,price, user_balance):
	try:
		while True:
			shares_to_buy = float(input('How many shares would you like to purchase ?\n>> '))
			if float(shares_to_buy) == shares_to_buy:
				break
			else:
				print('Invalid Selection\n')
	except:
		print('Error please try again')

	if True:
		confirm = input('You wish to purchase %s shares at a price of £%s a share coming to a total of £%s ? [y/n]\n>>' %(shares_to_buy, price, round(shares_to_buy*price,2)))
		if confirm.lower() == 'y':
			print('Confirmed')
			if user_balance < (shares_to_buy * price):
				print('Transaction failed due to insufficent funds')
			else:
				print('Your new balance is %s and your portfolio has been updated' %round(user_balance - shares_to_buy*price,2))
				return True, shares_to_buy, price
		else:
			print('Transaction cancelled retruning to menu')
	input('\nPress any key to continue')

	return False, 0, 0

def startup():
	username = find_user_type()
	print('Logged in as %s' %username)
	#This is where the main body of the code starts
	profile = get_info_from_csv(username)
	return profile

def main_menu():
	while True:
		print('Welcome to your trading panel')
		print('What would you like to do ?')
		print('1. Stock Lookup')
		print('2. View portfolio')
		print('3. Check Balance')
		print('4. Buy Stock')
		print('5. Sell Stock')
		print('6. Show stock graph')
		print('7. Exit')
		choice = input('>>')
		if choice in ['1','2','3','4','5','6']:
			return choice
		elif choice == '7':
			exit()
		else:
			print('Invalid Option')

def clear_terminal():
	try:
		a = sp.call('clear')
		a = sp.call('cls')
	except:
		None

def main(profile):
	username  = profile[0]
	name      = profile[1]
	portfolio = eval(profile[3])
	balance   = float(profile[4])

	print('Welcome %s' %name)
	while True:
		clear_terminal()
		choice = int(main_menu())
		print('You have chosen', choice)


		if choice == 1:
			stock_name = str(input('What is the ticker of the stock you would like to lookup ?\n>>'))
			try:
				print('The currect stock price of %s is £%s a share' %(stock_name,get_stock_price(stock_name,1)))
			except:
				print('Invalid Ticker')
			input('\nPress any key to continue')


		if choice == 2:
			print('Your current portfolio is:')
			for stock in portfolio:
				worth = get_stock_price(stock,portfolio[stock]) 
				print('%s shares of %s worth a total of £%s' %(portfolio[stock],stock,worth))
			input('\nPress any key to continue')


		if choice == 3:
			print('Your current balance is £%s' %balance)
			input('\nPress any key to continue')


		if choice == 4:
			stock_name = input('What is the ticker of the stock you would like to buy ?\n>> ')
			try:
				price = get_stock_price(stock_name,1)
				print('The currect stock price of %s stock is £%s a share' %(stock_name,price))
			except:
				print('Invalid Ticker')
			confirmed, amount_of_shares, price = buy_stock(stock_name, price, balance)
			balance = round(balance - amount_of_shares * price,2)
			if stock_name not in portfolio:
				portfolio.update({stock_name:amount_of_shares})
			else:
				previous_amount = portfolio[stock_name]
				portfolio.update({stock_name:amount_of_shares+previous_amount})
			update_current_user([username,name,profile[2],portfolio,balance])
			input('\nPress any key to continue')


		if choice == 5:
			print('Your Portfolio: \n') 
			for stock in portfolio:
				worth = get_stock_price(stock,portfolio[stock])
				print('%s shares of %s worth a total of £%s' %(portfolio[stock],stock,worth))
			try:
				while True:
					stock_name = str(input('What is the ticker of the stock you would lik to sell? \n>> ')).lower()
					if stock_name in portfolio:
						amount_to_sell = float(input('You have %s shares of that stock, how much would you like to sell ?\n>> ' %portfolio[stock_name]))
						if amount_to_sell > portfolio[stock_name]:
							print('You don\'t have that many shares to sell.')
						else:
							value = get_stock_price(stock_name,amount_to_sell)
							print('Selling %s shares of %s for a total of %s' %(amount_to_sell,stock_name,value))
							choice = input('Are you sure you wish to sell [y/n] ?\n>> ')
							if choice.lower() == 'y':
								
								current_amount_of_shares = portfolio[stock_name]
								portfolio[stock_name] = current_amount_of_shares - amount_to_sell

								if portfolio[stock_name] == 0:
									del portfolio[stock_name]
								balance += round(value,2)

								update_current_user([username,name,profile[2],portfolio,balance])
							else:
								print('Cancelling')
						break
						
					else:
						print('You don\'t own that stock for %s' %choice)
			except:
				print('Error please try again')

		if choice == 6:
			stock_name = str(input('What is the ticker of the stock you would like to lookup ?\n>>'))
			try:
				print('The currect stock price of %s is £%s a share' %(stock_name,get_stock_price(stock_name,1)))
				print('Here is the stock graph for the last week:')

				graph_control.get_graph(stock_name)

			except:
				print('Invalid Ticker')
			input('\nPress any key to continue')

if __name__ == '__main__':
	profile = startup()
	main(profile)