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
			username = str(input('What is your username ?\n>>'))
			password = str(input('What is your password (not secure)?\n>>'))
			if name:
				name = str(input('What is your name ?\n>>'))
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
		print('4. Sell Stock')
		print('5. Buy Stock')
		print('6. Exit')
		choice = input('>>')
		if choice in ['1','2','3','4','5']:
			return choice
		elif choice == '6':
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
	balance   = profile[4]

	print('Welcome %s' %name)
	while True:
		clear_terminal()
		choice = int(main_menu())
		print('You have chosen', choice)
		if choice == 1:
			stock_name = str(input('What is the ticker of the stock you would like to lookup ?\n>>'))
			try:
				print('The currect stock price is £%s' %get_stock_price(stock_name,1))
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




def buy_stock():
	None

def sell_stock():
	None


if __name__ == '__main__':
	profile = startup()
	main(profile)













