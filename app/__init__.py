from django.core.management.sql import sql_all
from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_login import LoginManager
import sqlalchemy
from sqlit import User
import hashlib

app = Flask(__name__)

#from sqlalchemy.ext import SQ

@app.route('/')
def index():
    return render_template('ind2.html', new_not = False)


@app.route('/new_notice')#, methods=['POST']
def new_notice(new_not = True):
     #return 'ololololol'
     return render_template('ind2.html',  new_not = new_not)


@app.route('/nn', methods = ['POST'])
def nn_submit():
    return str(request.form['not_header']) + str(request.form['not_body'])


@app.route('/login')
def log_in():
    return render_template('login.html')


@app.route('/log', methods = ['POST'])
def log_in2():
    User.name = request.form['login']
    foh = request.form['password'].encode('utf-8')
    User.password = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()
    #p = h.hexdigest()
    return str(hashlib.md5(request.form['password'].encode('utf-8')).hexdigest() == hashlib.md5('qwerty'.encode('utf-8')).hexdigest())
    #return User.password.hexdigest()
    #return str(request.form['login']) + str(request.form['password'])