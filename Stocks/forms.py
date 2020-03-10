from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, NumberRange
from Stocks.models import User

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

class Track_New_Stock_From(FlaskForm):
	ticker = StringField('Stock Ticker', validators=[DataRequired(), Length(min=4,max=4)])
	submit = SubmitField('Track Stock')

class SearchForm(FlaskForm):
	search = StringField('search', validators=[DataRequired()])
	submit = SubmitField('Search', render_kw={'class': 'btn btn-success btn-block'})

class NewsRequestForm(FlaskForm):
	topic = StringField('Enter News Topic', validators=[DataRequired()])
	submit = SubmitField('Search')

class BuyingForm(FlaskForm):
	ticker = StringField('Stock Ticker',      validators=[DataRequired(), Length(min=4,max=4)])
	amount = DecimalField('Amount of Shares', validators=[DataRequired(), NumberRange(min=0)])
	submit = SubmitField('Next Stage')

class SellingForm(FlaskForm):
	ticker = StringField('Stock Ticker',      validators=[DataRequired(), Length(min=4,max=4)])
	amount = DecimalField('Amount of Shares', validators=[DataRequired(), NumberRange(min=0)])
	submit = SubmitField('Next Stage')

class BuyConfirmation(FlaskForm):
	submit_yes = SubmitField('Yes')
	submit_no  = SubmitField('No')

class SellConfirmation(FlaskForm):
	submit_yes = SubmitField('Yes')
	submit_no  = SubmitField('No')