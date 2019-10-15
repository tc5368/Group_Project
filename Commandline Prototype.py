#Commandline application for Group 13's Project

#Evnetully thee sql will have something like this format
#user = [name,username,password,portfolio,balance]
#Username being primary key and then through agile develpoment will can move the password
#to a differnt database to make it more secure.

#Also this may not be needed as I may do it now but just in case this definitly won't be 
#how our users infomation will be stored.


#Requires pip installation of yahoo_fin, requests_html, pandas, forex-python



from get_info import get_info_from_csv
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

def get_info():
	#Simply takes the two inputs for now, no error checking (will obvisously change).
	while True:
		try:
			username = str(input('What is your username ?\n>>'))
			password = str(input('What is your password (not secure)?\n>>'))
			break
		except:
			print('Sorry invalid please retry')
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
	username, password = get_info()
	users.update({username:password})
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

def main(profile):
	username  = profile[0]
	name      = profile[1]
	portfolio = eval(profile[3])
	Balance   = profile[4]
	try:
		a = sp.call('clear')
		a = sp.call('cls')
	except:
		None
	print('Welcome %s' %name)
	print('Your current portfolio is:')
	for stock in portfolio:
		print('%s shares of %s worth a total of %s' %(portfolio[stock],stock,get_stock_price(stock,portfolio[stock])))





if __name__ == '__main__':
	profile = startup()
	main(profile)













