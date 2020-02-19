import os
from flask import render_template, url_for, request, redirect, flash, session
from Stocks import app, db
from Stocks.models import User#, Checkout,Company,Bike
from Stocks.forms import RegistrationForm, LoginForm#, CheckoutForm
from flask_login import login_user, current_user, logout_user, login_required
# Plotly and Dash import
import chart_studio.plotly as py
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import chart_studio
chart_studio.tools.set_credentials_file(username ='group13Yes', api_key='OspkIgNNW6CTIM7110px')
import pandas as pd
from datetime import datetime
# Sql
from sqlConnector import get_history, get_all_stocks

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(url_for('home'))
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


# Uses Flask as the server and dash as the app that connects to the server and works together.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app_dash = dash.Dash(
    __name__,
    server=app,
    routes_pathname_prefix='/dash/',
    external_stylesheets=external_stylesheets
)

stock_list = get_all_stocks()

# You can duplicate code and render this fig to get rid off empty figure when you reach the page.
fig = go.Figure()

# Generates HTML on the dash page and embeds a template of the graph and a dropdown list.
app_dash.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''Dash: A web application framework for Python.'''),
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
    print(fig["layout"])
    return fig
