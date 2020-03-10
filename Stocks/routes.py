import os
from flask import render_template, url_for, request, redirect, flash, session
from Stocks import app, db
from Stocks.models import *
from Stocks.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

# Plotly and Dash import
import chart_studio.plotly as py
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import chart_studio
# Login: group13Yes
# Password: group13HelloWorld
chart_studio.tools.set_credentials_file(username ='group13Yes', api_key='OspkIgNNW6CTIM7110px')
import pandas as pd
from datetime import datetime

# Sql
from sqlConnector import *

# News API
# Login = levondr@cardiff.ac.uk
# Password = group13HelloWorld
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='0f58067ab2ad447ba8e4af81ecea25c5')

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(first_name=form.first_name.data,
					last_name=form.last_name.data,
					email=form.email.data,
					password=form.password.data,
					balance=100.00) #Default start balance for all accounts

		db.session.add(user)
		db.session.commit()
		login_user(user)
		flash("Welcome " + user.first_name + " " + user.last_name)
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			flash("Welcome " + user.first_name + " " + user.last_name)
			return redirect(url_for('home'))
		flash('Invalid email or password.')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/buy", methods=['GET','POST'])
@login_required
def buy():
	form = BuyingForm()
	if form.validate_on_submit():
		return redirect(url_for('buyConfirm', ticker=form.ticker.data.upper(), amount=form.amount.data))
	return render_template('buy.html', title='Buying', form=form)

@app.route("/sell",methods=['GET','POST'])
@login_required
def sell():
	form = SellingForm()
	user_portfolio = Portfolio.query.filter_by(Customer_ID=current_user.id).all()
	if form.validate_on_submit():
		return redirect(url_for('sellConfirm', ticker=form.ticker.data.upper(), amount=form.amount.data))
	return render_template('sell.html', title='sell', form=form, portfolio=user_portfolio)

@app.route("/sellConfirm/<ticker>/<amount>", methods=['GET','POST'])
@login_required
def sellConfirm(ticker,amount):
	if (ticker or amount) == None:
		return redirect(url_for('home'))
		#This needs more validation implemented
	form = SellConfirmation()
	if form.validate_on_submit():
		if form.submit_yes.data :
			if check_sell(current_user.id,ticker,amount):
				flash('Stock Bought')
			else:
				flash('Not high enough share amount or trying to sell stock you dont own')
		else:
			return redirect(url_for('home'))
	return render_template('sellConfirmation.html', title='Sell Confirmation', form=form)
	


@app.route("/buyConfirm/<ticker>/<amount>", methods=['GET','POST'])
@login_required
def buyConfirm(ticker,amount):
	if (ticker or amount) == None:
		return redirect(url_for('home'))
		#This needs more validation implemented
	form = BuyConfirmation()
	if form.validate_on_submit():
		if form.submit_yes.data :
			if check_buy(current_user.id,ticker,amount):
				flash('Stock Bought')
			else:
				flash('Not high enough balance or trying to buy untracked stock')
		else:
			return redirect(url_for('home'))
	return render_template('buyConfirmation.html', title='Buy Confirmation', form=form)

@app.route("/track", methods=['GET','POST'])
@login_required
def track():
	form = Track_New_Stock_From()
	if form.validate_on_submit():
		make_new_hist(form.ticker.data)
	return render_template('track.html', title='Track', form=form)



#to be implemented

#Searching for a stock should take you to this particular page
#It will show the graph, the news and the current price. 
#Also if the users owns shares how many shares they own should be shown.

#@app.route("/stock/<ticker>",methods=['GET','POST'])
#def stock_page(ticker):
#	stock_data = Stock_Info.query.filter_by(Stock_ID=ticker).first()
#	return render_template('stockpage.html', title=stock-page)



# Uses Flask as the server and dash as the app that connects to the server and works together.
app_dash = dash.Dash(
	__name__,
	server                 = app,
	routes_pathname_prefix = '/stocks/',
	external_stylesheets   = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

def find_avaliable():
	stock_list     = db.engine.table_names()
	history_tables = []
	for i in stock_list:
		if i.endswith('_HIST'):
			history_tables.append(i)
	if history_tables == []:
		history_tables.append(None)
	return history_tables

stock_list = find_avaliable()

# You can duplicate code and render this fig to get rid off empty figure when you reach the page.
fig = go.Figure()

# Generates HTML on the dash page and embeds a template of the graph and a dropdown list.
app_dash.layout = html.Div(children=[
	html.H1(children='Detailed stock graph page'),
	dcc.Graph(id='plotly_fig', figure=fig),
	dcc.Dropdown(
		id      ='stock_dropdown',
		options =[{'label': i, 'value': i} for i in stock_list],
		value   =stock_list[0],
		style   ={"max-width": "200px", "margin": "auto"}
	)
],
style={"max-width": "1000px", "margin": "auto"})

# Will wait for the user to select anything on the dropdown menu and output the result on the graph.
@app_dash.callback(
	[Output('plotly_fig', 'figure'),
	Output('stock_dropdown', 'options')],
	[Input('stock_dropdown', 'value')]
)
def update_figure(selected_stock):
	"""Will show different graphs on the figure, depending on what the user selects.
	Will be called every single time the user changes value on the dropdown list.
	Will also be called once everytime the page is loaded.
	Parameters
	----------
	selected_stock : string
		The value selected in the dropdown list.
	Returns
	-------
	figure
		Return the figure type information in an array with the new read figure data.
	"""
	stock_list = find_avaliable()
	options =[{'label': i, 'value': i} for i in stock_list]

	df = get_history(selected_stock)
	fig = go.Figure(data=go.Ohlc(x=df['Date'],
						open   = df['Open'],
						high   = df['High'],
						low    = df['Low'],
						close  = df['Close']),
						layout = go.Layout(
						title  = go.layout.Title(text="Graph Showing " + selected_stock.upper() + " Stock Price History")
						)
	)
	print()
	return fig, options

@app.route('/newsSearch',methods=['GET','POST'])
def newsSearch():
	form = NewsRequestForm()
	if form.validate_on_submit():
		return redirect(url_for('news', topic=form.topic.data))
	return render_template('newsSearch.html', title='News', form=form)


@app.route('/news/<topic>')
def news(topic):
	"""
	Using newsAPI to collect a set of articles relevant to the topic. Will convert
	publishedAt field into datetime object and convert it back into a string in a certain
	format. Passes a whole article with a converted date into news template.
	"""
	news = newsapi.get_everything(q=topic,language='en',sort_by='relevancy')
	if news['totalResults'] > 0 and news['status'] == 'ok':
		count = 0
		articleList = []
		while count != 3:
			article = news['articles'][count]
			date = article['publishedAt']
			date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
			dateAndTime = date.strftime("%d %B %Y, %H:%M")
			article['publishedAt'] = dateAndTime
			articleList.append(article)
			count = count + 1
		return render_template("news.html", articles=articleList)
	else:
		return "<p>Couldn't find any article</p>"

@app.route('/portfolio')
def portfolio():

	#This dosen't seem to be working for me
	#the first if statment is always returning false can't find my accounts
	#in the session.keys() ?

	# if "user_id" in session.keys():
	# 	user = User.query.get(session["id"])
	# 	user_portfolio = Portfolio.query.filter_by(Customer_ID=session["user_id"]).all()
	# else:
	# 	user = None
	# 	user_portfolio = []

	#I have left your code where it is and if you want to change it back then no worries
	#Completly get the thought behind the above but hopefully when we move over to the
	#new html templates we will make it so thats immpossible to get to the portfolio
	#page without being logged in.
	user = current_user.id
	user_portfolio = Portfolio.query.filter_by(Customer_ID=current_user.id).all()


	return render_template("portfolio.html", portfolio = user_portfolio, user = user)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect((url_for('search_results', query=form.search.data)))  # or what you want
    return render_template('search.html', form=form)

@app.route('/search_results/<query>')
@login_required
def search_results(query):
	results = User.query.whoosh_search(query).all()
	return render_template('search_results.html', query=query, results=results)
