import os
#From initilisation
from Stocks import app, db

#Import models and forms
from Stocks.models import *
from Stocks.forms import *

#Import Flask methods
from flask import render_template, url_for, request, redirect, flash, session
from flask_login import login_user, current_user, logout_user, login_required

# Plotly and Dash import
import chart_studio.plotly as py
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from   dash.dependencies import Input, Output

import chart_studio
# Login: group13Yes
# Password: group13HelloWorld
chart_studio.tools.set_credentials_file(username ='group13Yes', api_key='OspkIgNNW6CTIM7110px')

#Other libraries
import pandas as pd
from datetime import datetime

#
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

		return "<p>Couldn't find any articles</p>"

@app.route("/buy", methods=['GET','POST'])
@login_required
def buy():
	form = BuyingForm()
	if form.validate_on_submit():
		return redirect(url_for('buyConfirm', ticker=form.ticker.data.upper(), amount=form.amount.data))
	return render_template('buy.html', title='Buying', form=form) #add price in here to display on website how mush trade will cost.

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
				flash('Stock Sold')
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
	ticker_info = Stock_Info.query.filter_by(Stock_ID=ticker).first()
	return render_template('buyConfirmation.html', title='Buy Confirmation', form=form, ticker=ticker_info, amount=amount)

@app.route("/track", methods=['GET','POST'])
@login_required
def track():
	form = Track_New_Stock_From()
	if form.validate_on_submit():
		make_new_hist(form.ticker.data)
	return render_template('track.html', title='Track', form=form)


@app.route("/stock",methods=['GET','POST'])
def stock():
	form = Get_Stock_Ticker_From()
	if form.validate_on_submit():
		return redirect(url_for('stock_page',ticker=form.ticker.data.upper()))
	return render_template('stock.html', title='Stock',form=form)


@app.route("/stock_page/<ticker>",methods=['GET','POST'])
def stock_page(ticker):
	stock_data = Stock_Info.query.filter_by(Stock_ID=ticker).first()
	price = stock_data.Current_Price
	info = get_Info(ticker)
	return render_template('stock_page.html'
							, title  = 'stock_page'
							, ticker = ticker
							, price  = price	
							, info   = info)

@app.route('/portfolio')
@login_required
def portfolio():
	user = current_user.id
	user_portfolio = Portfolio.query.filter_by(Customer_ID=current_user.id).all()
	return render_template("portfolio.html", portfolio = user_portfolio)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('search.html', form=search)

@app.route('/search_results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search_string != None:
        if search.data['select'] == 'Stock_ID':
            qry = Stock_Info.query().filter_by(Stock_Info.Stock_ID.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'Stock_Name':
            qry = Stock_Info.query().filter_by(Stock_Info.Stock_Name.contains(search_string))
            results = qry.all()
        else:
            qry = Stock_Info.query().all()
            results = qry
    else:
        qry = db.query(Album)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/search')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('search_results.html', table=table)
# For unauthorized users, will redirect them to login page.
@login_manager.unauthorized_handler
def unauthorized():
	return redirect(url_for('login'))
