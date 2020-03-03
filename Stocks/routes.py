import os
from flask import render_template, url_for, request, redirect, flash, session
from Stocks import app, db
from Stocks.models import User, Stock_Info, Portfolio#, Checkout,Company,Bike
from Stocks.forms import RegistrationForm, LoginForm, Track_New_Stock_From, SearchForm#, CheckoutForm
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
			print(user)
			login_user(user)
			flash("Welcome " + user.first_name + " " + user.last_name)
			return redirect(url_for('home'))
		flash('Invalid email or password.')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/track", methods=['GET','POST'])
def track():
	form = Track_New_Stock_From()
	if form.validate_on_submit():
		make_new_hist(form.ticker.data)
	return render_template('track.html', title='Track', form=form)



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
	Output('plotly_fig', 'figure'),
	[Input('stock_dropdown', 'value')]
)

#Needs to update the dropdown menu with the new graphs


#Where is this update figure called ??
def update_figure(selected_stock):
	"""Will show different graphs on the figure, depending on what the user selects. Will be called every single time the user changes value on the dropdown list.
	Parameters
	----------
	selected_stock : string
		The value selected in the dropdown list.
	Returns
	-------
	figure
		Return the figure type information in an array with the new read figure data.
	"""
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
	#print(fig["layout"])
	return fig

@app.route('/news')
def news():
	"""
	Using newsAPI to collect a set of articles relevant to the topic. Will convert
	publishedAt field into datetime object and convert it back into a string in a certain
	format. Passes a whole article with a converted date into news template.
	"""
	news = newsapi.get_everything(q='Nvidia',language='en',sort_by='relevancy')
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
	if "user_id" in session.keys():
		user_portf = Portfolio.query.get(session["user_id"])
		print(user_portf.Amount_of_Shares)
	else:
		print("Not logged in")
	return render_template("portfolio.html")

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
