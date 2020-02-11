import random as r


class Stock():
	"""Stock Object	"""
	def __init__(self, name, start_value):
		'''Initilises the object
		
		Arguments:
			name {String} -- display name for the stock
			start_value {int or float} -- price of the stock at initilisation
		'''
		self.name = name
		self.value  = start_value
		self.avaliable_volume = 100

	def getValue(self):
		'''Returns the Current stock price

		Returns:
			[Float] -- [Current Stock Price]
		'''
		return self.value

	def getName(self):
		'''Returns the printing name of the stock
		
		Returns:
			[String] -- [Display name]
		'''
		return self.name

	def buy(self,amount):
		'''Controls the buying function of the stock
		
		Will cause the stock's value to rise when more stock is bought
		
		Arguments:
			amount {integer} -- Amount of shares being purchesed
		'''
		self.avaliable_volume -= amount
		for i in range(amount):
			growth = 1 + (r.random()/100)
			self.value = self.value * growth

	def sell(self,amount):
		'''Controls the selling of the stock
		
		Will cause the stock's value to drop the more stocks are sold
		
		Arguments:
			amount {integer} -- Amount of shares being sold off
		'''
		self.avaliable_volume += amount
		for i in range(amount):
			growth = 1 - (r.random()/100)
			self.value = self.value * growth

#Creates 4 example stocks for this simulation

aapl = Stock('Apple',100)
tsla = Stock('Tesla',100)
msft = Stock('Microsoft',100)
nvda = Stock('Nvidia',100)

#Gloabl list of all the posisble stocks
global stocks
stocks = [aapl,tsla,msft,nvda]


def buy(to_buy,amount):
	'''Buying printing
	
	Will print out infomation about the trade being made
	
	Arguments:
		to_buy {stock} -- Stock Object to run the buy method on
		amount {integer} -- Amount of shares being bought
	'''
	print('Buying %s shares of %s at price £%s' %(amount,to_buy.getName(),to_buy.getValue()))
	to_buy.buy(amount)
	after = to_buy.getValue()
	print('Price of %s stock after the trade %s' %(to_buy.getName(),to_buy.getValue()))

def sell(to_sell,amount):
	'''Selling printing
	
	Will print out the infomation about the trade being made
	
	Arguments:
		to_sell {stock} -- Stock object for the stock that is to be sold
		amount {integer} -- Amonut of shares being sold
	'''
	print('Selling %s shares of %s at price £%s' %(amount,to_sell.getName(),to_sell.getValue()))
	to_sell.sell(amount)
	after = to_sell.getValue()
	print('Price of %s stock after the trade %s' %(to_sell.getName(),to_sell.getValue()))


def main(sim_length):
	'''Main loop
	
	Has a 50:50 chance to buy or sell a random amount of a random stock
	
	Arguments:
		sim_length {integer} -- Amount of iterations to loop through
	'''
	for trade in range(sim_length):
		if r.random() > 0.5:
			to_buy = r.choice(stocks)
			amount = (r.randint(1,10))
			buy(to_buy,amount)
		else:
			to_sell = r.choice(stocks)
			amount = (r.randint(1,10))
			sell(to_sell,amount)

if __name__ == '__main__':
	main(10)