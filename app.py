from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import InputRequired, Email, Length
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import os
import re
from pprintpp import pprint as pp

app = Flask(__name__)
Bootstrap(app)


app.config['SECRET_KEY']= 'thisissecet!'


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=50)])
    email = StringField('Email Address', validators= [InputRequired(), Email(message='Invalid Email!'), Length(min=8, max=80)])
    password = PasswordField('New Password', [validators.InputRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', validators =[InputRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email!'), Length(min=8, max=80)])
    password = PasswordField('Password', validators= [InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class ReusableForm(Form):
    url = TextField('Enter Web URL:', validators=[validators.required()])



@app.route('/')
def index():

    return render_template('index.html')

@app.route('/valid', methods=['GET', 'POST'])
def valid():

    form= LoginForm()
    z = (form.email.data)
    v = (form.password.data)
    drop= "DROP TABLE users"


    if form.validate_on_submit():
        conn= sqlite3.connect('database.db')
        c= conn.cursor()

        cursor = c.execute("SELECT * FROM users")
        a =cursor.fetchall()
        for x in a:
            if z in x[0]:
                if v in x[1]:

                    return redirect(url_for('dashboard'))



                else:
                    return render_template('trial1.html')
            else:
                return render_template('trial.html')



        #rows = c.fetchall()
        #for row in rows:
            #if row[0]form.email.data not in row:
                #return render_template('trial.html')
            #elif form.password.data not in row:
                #return render_template('trial1.html')

            #else:
                #return render_template('dashboard.html', appuser=z)


    return render_template('valid.html', form=form)


@app.route('/signup', methods= ['GET', 'POST'])
def signup():
    form = RegistrationForm()
    q = 'Registration is valid.'
    y = (form.username.data)
    y2 = (form.email.data)
    y1 = (form.password.data)

    if form.validate_on_submit():
        conn= sqlite3.connect("database.db")
        cur = conn.cursor()
        ##cur.execute("CREATE TABLE IF NOT EXISTS users(email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)")
        cur.execute('SELECT * FROM users WHERE (email=? AND password=?)', (y2, y1))
        entry = cur.fetchone()
        if entry is None:
            cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (y2, y1))
            conn.commit()
            return render_template('success.html', username1= y)
        else:
            return render_template('taken.html')




    elif request.method == 'POST' and form.validate() == False:
        return render_template('try.html')

    return render_template('signup.html', form = form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form =ReusableForm()
    errors = []

    v = 'Webpage Title:'

    if request.method == "POST":
        # get url that the person has entered
        try:
            url = request.form['url']
            with urllib.request.urlopen(url) as response:
                soup = BeautifulSoup(response, 'lxml')
            match = soup.title.text
            article = soup.find('article')
            links = soup.find_all(href=True)[0:5]


            return render_template('dashboard.html', v = v, match = match, article = article, links = links)








        except:
            errors.append(
            "Unable to get URL. Please make sure it's valid and try again."
            )


    return render_template('dashboard.html')




@app.route('/logout')
def logout():

    return render_template('logout.html')
















if __name__ == '__main__':
    app.run(debug=True)
