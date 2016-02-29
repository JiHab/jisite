import sqlite3
import sqlalchemy



db_name = 'db_jisite.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()
c.execute('SELECT *  FROM users where id_user = 1')
#print(c.fetchall())


class User(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
    #def write()
