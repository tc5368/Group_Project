import random as r


class Stock():
	"""Stock Object """
	def __init__(self, name, start_value):
		self.name = name
		self.value  = start_value
		self.avaliable_volume = 100

	def getValue(self):
		return self.value

	def getName(self):
		return self.name

	def buy(self,amount):
		self.avaliable_volume -= amount
		for i in range(amount):
			growth = 1 + (r.random()/100)
			self.value = self.value * growth

aapl = Stock('Apple',100)
tsla = Stock('Tesla',100)
msft = Stock('Microsoft',100)
nvda = Stock('Nvidia',100)

global stocks
stocks = [aapl,tsla,msft,nvda]


def main(sim_length):
	for trade in range(sim_length):
		to_buy = r.choice(stocks)
		amount = (r.randint(1,10))
		print('Buying %s shares of %s at price £%s' %(amount,to_buy.getName(),to_buy.getValue()))
		to_buy.buy(amount)
		after = to_buy.getValue()
		print('Price of %s stock after the trade %s' %(to_buy.getName(),to_buy.getValue()))


if __name__ == '__main__':
	main(10)