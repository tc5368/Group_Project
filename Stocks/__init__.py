from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'd63e56c75fc4923a027728f430dfb2c899e67a632497317a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1769261:apmWzUswLy6LvfX@csmysql.cs.cf.ac.uk:3306/c1769261_Second_Year'

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from Stocks import routes
