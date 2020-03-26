from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, NumberRange
from Stocks.models import User
from flask_table import Table, Col, LinkCol

class RegistrationForm(FlaskForm):
	first_name       = StringField('First Name', validators=[DataRequired(), Length(min=3, max=20)])
	last_name        = StringField('Surname', validators=[DataRequired(), Length(min=3, max=20)])
	email            = StringField('Email', validators=[DataRequired(), Email()])
	password         = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,14}$', message='Your password should be between 6 and 14 characters long.')])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit           = SubmitField('Register')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already exists, please choose a different one.')

class LoginForm(FlaskForm):
	email    = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit   = SubmitField('Login')

class Retrieve_Stock_Ticker_Form(FlaskForm):
	stock_name = StringField('Stock Name')
	submit = SubmitField('Find')

class Get_Stock_Ticker_Form(FlaskForm):
	ticker = StringField('Stock Ticker', validators=[DataRequired()])
	submit = SubmitField('Find')

class SearchForm(FlaskForm):
	choices = [('Stock_ID', 'Stock ID'),('Stock_Name', 'Stock Name')]
	select = SelectField('Search Stocks:', choices=choices)
	search = StringField('Search')
	submit = SubmitField('Submit')

class NewsRequestForm(FlaskForm):
	topic = StringField('Enter News Topic', validators=[DataRequired()])
	submit = SubmitField('Search')

class BuyingForm(FlaskForm):
	ticker = StringField('Stock Ticker',      validators=[DataRequired()])
	amount = DecimalField('Amount of Shares', validators=[DataRequired()])
	submit = SubmitField('Next Stage')

class SellingForm(FlaskForm):
	ticker = StringField('Stock Ticker',      validators=[DataRequired()])
	amount = DecimalField('Amount of Shares', validators=[DataRequired(), NumberRange(min=0)])
	submit = SubmitField('Next Stage')

class Confirmation(FlaskForm):
	submit_yes = SubmitField('Yes')
	submit_no  = SubmitField('No')


class AutomationForm(FlaskForm):
	ticker        = StringField('Stock Ticker', validators=[DataRequired()])
	trigger_price = DecimalField('Price Trigger', validators=[DataRequired()])
	limit         = DecimalField('Limit of shares to trade', validators=[DataRequired()])
	increment     = DecimalField('The amount of shares to buy or sell at a time when the trigger is activated', validators=[DataRequired()])
	choices1 = [('Above', 'Above'),('Below', 'Below')]
	trigger       = SelectField('Trigger:', choices=choices1)#Either Above or Below in dropdown
	choices2 = [('Buy', 'Buy'),('Sell', 'Sell')]
	strategy      = SelectField('Strategy:', choices=choices2)#Either Buy or Sell in dropdown
	submit = SubmitField('Submit')
	
	# Someone please look into how to get the trigger and strategy field to be dropdown
	# Then make a html page for taking input for this form.
	
	# when this is done please let Tom know so he can finish the sql and route side




#///////////////////////////////////////////////////////////////////////////////////////////////////#
#								Tables																#
#///////////////////////////////////////////////////////////////////////////////////////////////////#


class Results(Table):
	Stock_ID         = LinkCol('Stock ID','stock_page',attr='Stock_ID',url_kwargs=dict(ticker='Stock_ID'))
	Stock_Name       = Col('Stock Name')
	Current_Price    = Col('Current Price')
	Stock_Table      = Col('Stock Table', show=False)


















