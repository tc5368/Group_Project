import os
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Author, Book, User
from shop.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    books = Book.query.all()
    return render_template('home.html', books=books, title='My Wonderful Book Shop')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created.  You can now log in.')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You are now logged in.')
            return redirect(url_for('home'))
        flash('Invalid username or password.')

        return render_template('login.html', form=form)

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#Flask lab 3: implementation of Cart.  Needs 'session' import!
# https://github.com/kkschick/ubermelon-shopping-app/blob/master/melons.py MELONS

