from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper
from sqlalchemy import Table, create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
import re
from sqlit import query_user
from datetime import datetime
my_str = 'vladimir.mail@ukr.net'

res = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", my_str)
if res != None:
    print('none')

engine = create_engine('sqlite:///db_jisite_tmp.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

em = 'bill@mail.com'
name = 'jihab1'
#em = em.decode('utf-8')
ololo = engine.execute('select password, id from users where name = :1', [name])
all = ololo.fetchall()
#('select * from users where email = :1 or name = :2', [self.email, self.name])
#password = all[0]._row[0]
#id_ =  all[0]._row[1]
#print(all[0])
# login = 'jihab1'
# q = query_user()
# q = q.all()
# q = filter(lambda q: q.name.lower() == login.lower(), q)
# print(q.__next__().name)
# from datetime import datetime
# str = '14/01/2014'
# strdt = '14/01/2014 14:14:21'
# dt = datetime.strptime(str, '%d/%m/%Y')
# dtt = datetime.strptime(strdt, '%d/%m/%Y %H:%M:%S')
# a=0

str1 = 'zazazazazazazazazaz'
str2 = 'Za'

print(str(str2.lower() in str1.lower()))