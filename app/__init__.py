from django.core.management.sql import sql_all
from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_login import LoginManager, login_user, login_required, logout_user
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime, date
import hashlib
from sqlit import User, findUser, query_user, Advt, query_adv
app = Flask(__name__)
if __name__ == "app":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

engine = create_engine('sqlite:///:db_jisite:', echo=True)
Session = sessionmaker(bind=engine)
session_ = Session()

login_manager = LoginManager()
login_manager.init_app(app)
curUser = None
#session['user'] = None
#login_manager.login_view = 'login'

@login_manager.user_loader
@app.route('/', methods=['GET'])
def index():
    l_adv = Advt.get_adv_all(Advt)
    i = request.form.__len__()
    if i > 0:
        l = request.form['location']
        e = request.form['event']
        t = request.form['text']
        l_adv = Advt.get_adv_search(l, e, t)
        session['l_adv'] = l_adv
    try:
        curUser = User.get_user(session['user_id'])
        return render_template('index.html', loggedUser=True, name=curUser.name, my_adv=True, adv_list=l_adv)
    except:
        return render_template('index.html', loggedUser=False, my_adv=True, adv_list=l_adv)



@app.route('/find',methods=['POST'])
def find_adv():
    try:
        s = session
        f = request.form
        l = str(request.form['location'])
        e = str(request.form['event'])
        t = str(request.form['text'])
        l_adv = Advt.get_adv_search(l, e, t)
        #a = l_adv
        try:
            curUser = User.get_user(session['user_id'])
            return render_template('index.html', loggedUser=True, name=curUser.name, my_adv=True, adv_list=l_adv) #redirect(url_for('index', loggedUser=True, name=curUser.name, my_adv=True, adv_list=l_adv))
        except:
            return redirect(url_for('index', loggedUser=False, my_adv=True, adv_list=l_adv))
            #return str(t)
    except:
        a=1
        return str(t)


@app.route('/new_notice')#, methods=['POST']
def new_notice(new_not = True):
     #return 'ololololol'
     return render_template('new_notice.html')

@app.route('/my_adv')
def my_adv():
    #try:
        u_id = session['user_id']
        curUser = User.get_user(session['user_id'])
        if u_id is None:
            ret =  'log in please'
        else:
            l = Advt.get_adv_auth(u_id)
            if l.__len__() < 1:
                ret = 'no adv'
            else:
                ret = render_template('/index.html', my_adv=True, adv_list=l, loggedUser=True, name=curUser.name)
    #except:
        #ret = 'log in please'
    #lq = query_adv()
        return ret


@app.route('/add_new_not', methods=['POST'])
def nn_submit():
    global curUser
    u_id = session['user_id']
    header = str(request.form['header'])
    body = str(request.form['body'])
    date_str = str(request.form['date'])
    date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')#.strftime('%d.%m.%Y %H:%M:%S')
    location = str(request.form['location'])
    activity = str(request.form['event'])
    date_pub = datetime.now(tz=None)#.strftime('%d.%m.%Y %H:%M:%S')

    adv = Advt(date, date_pub, header, body, location, True, u_id, activity)
    adv.save()
    l = Advt.get_adv_auth(u_id)
    a=l
    return my_adv()
    # str(request.form['header']) + str(request.form['body']) + str(request.form['date']) + str(request.form['location']) + str(request.form['event'])


@app.route('/login')
def log_in(error=False):
    #error = False
    return render_template('login.html', error=error, error_name='', array=range(100))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    global curUser
    curUser = None
    #session['user'] = None
    return redirect(url_for('index', loggedUser=False))


@app.route('/log', methods=['GET','POST'])
def log_in2():
    global curUser
    r = request
    if request.method == 'POST':
        login = request.form['login']
        hash_pass = str(hashlib.md5(request.form['password'].encode('utf-8')).hexdigest())
        remember = request.form['remember']
        q = query_user().all()
        q = filter(lambda q: q.name.lower() == login.lower() and q.password == hash_pass, q)
        try:
            curUser = q.__next__()
            login_user(curUser, remember=remember)
            return redirect(url_for('index', loggedUser=True, name=curUser.name))

        except:
            s= session
            #messages = json.dumps({"main":"Condition failed on page baz"})
            #session['error'] = True
            r = redirect(url_for('log_in'), session['error'])

            return r#return redirect(url_for('login'))
    else:
        return 'ololo'


@login_manager.user_loader
def load_user(id):
    global curUser
    curUser = User.get_user(int(id))
    session['user_id'] = id
    #return User.get_user(int(id))
    return curUser

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/reg', methods = ['POST'])
def reg_():
    if str(request.form['password_repeat']) != str(request.form['password']) or str(request.form['password_repeat']) == '':
        return "password is incorrect"
    hash_pass = str(hashlib.md5(request.form['password'].encode('utf-8')).hexdigest())
    regUser = User(name=str(request.form['login']), password=hash_pass, email=str(request.form['email']))

    #user2 = User()
    #user2.name_user = str(request.form['login'])
    #user2.email = "u2@"
    #session.add(vasiaUser)
    #regUser.save()
    user = regUser.check()
    if not type(user) == str:
        a = user.is_active
        login_user(user, remember=False)
        l_adv = Advt.get_adv_all(Advt)
        #curUser = User.get_user(session['user_id'])
        #ret =  render_template('index.html', loggedUser=True, name=user.name, my_adv = True, adv_list=l_adv)
        ret = redirect(url_for('index', loggedUser=True, name=user.name, my_adv=False))
    #regUser.save()
    #user2.save()
    return ret