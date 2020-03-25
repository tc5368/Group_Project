
from datetime import datetime
from Stocks import login_manager,db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class User(UserMixin, db.Model):
	__tablename__ = "User"
	id            = db.Column(db.Integer,     primary_key=True)
	first_name    = db.Column(db.String(20),  nullable=False)
	last_name     = db.Column(db.String(20),  nullable=False)
	email         = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(128))
	password      = db.Column(db.String(60),  nullable=False)
	balance       = db.Column(db.Float,       nullable=False)

	def __repr__(self):
		return f"User('{self.email}')"

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

class Stock_Info(db.Model):
	__tablename__ 	 = "Stock_Info"
	Stock_ID         = db.Column(db.String(4),  primary_key = True)
	Stock_Name       = db.Column(db.String(45), nullable    = False)
	Current_Price    = db.Column(db.Float,      nullable    = False)
	Stock_Table      = db.Column(db.String(10), nullable    = False)

	def __init__(self, Stock_ID, Stock_Name, Current_Price, Stock_Table):
		self.Stock_ID      = Stock_ID
		self.Stock_Name    = Stock_Name
		self.Current_Price = Current_Price
		self.Stock_Table   = Stock_Table

class Portfolio(db.Model):
	__tablename__ 	 = "Portfolio"
	Customer_ID      = db.Column(db.Integer, db.ForeignKey(User.id), primary_key = True)
	Stock_ID         = db.Column(db.String(4), db.ForeignKey('Stock_Info.Stock_ID'), primary_key = True)
	Amount_of_Shares = db.Column(db.Float, nullable=False)

	def __init__(self, Customer_ID, Stock_ID, Amount_of_Shares):
		self.Customer_ID      = Customer_ID
		self.Stock_ID         = Stock_ID
		self.Amount_of_Shares = Amount_of_Shares

class Automation(db.Model):
	__tablename__ = "Automation"
	Customer_ID   = db.Column(db.Integer,   db.ForeignKey(User.id), primary_key = True)
	Stock_ID      = db.Column(db.String(4), db.ForeignKey('Stock_Info.Stock_ID'), primary_key = True)
	Trigger       = db.Column(db.String(1), nullable = False)
	Trigger_Price = db.Column(db.Float,     nullable = False)
	Strategy      = db.Column(db.String(1), nullable = False)
	Increment     = db.Column(db.Float,     nullable = False)
	Limit         = db.Column(db.Float,   nullable = True)

	def __init__(self, Customer_ID, Stock_ID, Trigger, Trigger_Price, Strategy, Limit):
		self.Customer_ID   = Customer_ID
		self.Stock_ID      = Stock_ID
		self.Trigger 	   = Trigger
		self.Trigger_Price = Trigger_Price
		self.Strategy      = Strategy
		self.Limit 		   = Limit


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

db.create_all()
db.session.commit()


























