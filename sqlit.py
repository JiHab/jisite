from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper
from sqlalchemy import Table, create_engine, Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
import re
from datetime import datetime, date
from datetime import *
Base = declarative_base()

engine = create_engine('sqlite:///db_jisite_tmp.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    is_active = Column(Boolean)
    password = Column(String,unique=False)

    def __init__(self, name, password, email, is_active=True):
        s = self
        self.name = name
        self.password = password
        self.email = email
        self.is_active = is_active
        #self.id = id


    def __repr__(self):
       return "<User('%i', '%s','%s', '%s')>" % (self.id, self.name, self.email, self.password)
       # print(self.name_user)
       # return str(self.name_user)

    def save (self):
        session.add(self)
        session.commit()
        #session.flush()

    def check(self):
        ret_str = ""
        correct = True
        em = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.email)
        if em is None and self.email != '':
            print('email' + str(self.email) + ' is invalid')
            ret_str = ret_str + 'email' + str(self.email) + ' is invalid' + '<br>'
            correct = False
        rest = engine.execute('select * from users where email = :1', [self.email]).fetchall().__len__()
        #rest_fetch = rest
        if rest > 0:
            print('mail '+ self.email + ' is allready exist')
            ret_str = ret_str + 'mail '+ self.email + ' is allready exist' + '<br>'
            correct = False
        restn = engine.execute('select * from users where name = :1', [self.name]).fetchall().__len__()
        if restn > 0:
            print('login '+ self.name + ' is allready exist')
            ret_str = ret_str + 'login '+ self.name + ' is allready exist' + '<br>'
            correct = False
        if correct:
            self.save()
            return self
        else:
            return ret_str

    def login(self):
        result = engine.execute('select * from users where name = :1', [self.name]).fetchall()

    def get_id(self):
        return (self.id)
        #findUser(id=id)

    def get_user(id):
        q = query_user()
        q = filter(lambda q: q.id == id, q)
        try:
            u = q.__next__()
            return u
        except:
           return None


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def query(self):
        return session.query(User).all()


class Advt(Base):
    __tablename__ = 'advertisment'
    id = Column(Integer, primary_key=True)
    header = Column(String(50), unique=False)
    body = Column(String(300), unique=False)
    location = Column(String(50), unique=False)
    is_active = Column(Boolean,unique=False)
    author = Column(Integer, unique=False)
    date = Column(DateTime, unique=False)
    date_pub = Column(DateTime, unique=False)
    activity = Column(String)

    def __init__(self, date, date_pub, header, body, location, is_active, user, activity):
        self.header = header
        self.body = body
        self.location = location
        self.is_active = True
        self.author = user
        self.date = date
        self.date_pub = date_pub
        self.activity = activity

    def save(self):
        session.add(self)
        session.commit()

    def query(self):
        return session.query(Advt).all()

    def get_adv(id):
        q = query_adv()
        q = filter(lambda q: q.id == id, q)
        try:
            a = q.__next__()
            return a
        except:
           return None

    def get_adv_auth(id):
        q = query_adv()
        q = filter(lambda q: q.author == id, q)
        l = []
        while True:
            try:
                l.append(q.__next__())
            except:
                return l

    def get_adv_search(location, event, text):
        q = query_adv()
        q = filter(lambda q: q.location == location and q.activity == event and text.lower() in q.body.lower(), q)
        l=[]
        while True:
            try:
                l.append(q.__next__())
            except:
                return l

    def get_adv_all(id):
        q = query_adv()
        q = filter(lambda q: int(q.is_active) == 1, q)
        l = []
        while True:
            try:
                l.append(q.__next__())
            except:
                return l





def findUser(login=None, password=None, id=None):
    if id is None:
        result = engine.execute('select password, id, email, name from users where name = :1 COLLATE NOCASE', [login]).fetchall()
    else:
        result = engine.execute('select password, id, email, name from users where id = :1 COLLATE NOCASE', [id]).fetchall()
    if result.__len__() > 0:
        password_ = result[0]._row[0]
        id_ =  result[0]._row[1]
        email_ = result[0]._row[2]
        name_ = result[0]._row[3]
        if password == password_:
            user = User(name_, password_, email_, id)
            #user.id = id_
            return user
        else:
            return None
    else:
        return None



def query_user():
    users = session.query(User)
    #print("user", users)
    return users

def query_adv():
    adv = session.query(Advt)
    return adv



Base.metadata.create_all(engine)

