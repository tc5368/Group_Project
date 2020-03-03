from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
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
