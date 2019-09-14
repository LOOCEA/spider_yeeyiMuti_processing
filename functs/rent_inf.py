import sqlite3
import os

class RentInf:
    def __init__(self):
        self.house_type='unknown'
        self.bedroom=0
        self.bathroom = 0
        self.rent_price = 0
        self.gender_requirement = 'No requirement'
        self.title = 'unknown'
        self.address = 'unknown'
        self.city = 'unknown'
        self.url = 'unknown'
        self.time = '1900-1-1'
        self.time_limit = 0
        self.distance = -1
        self.rent_type='unknown'
    def insert_into_table(self):
        sql="insert into mytable\
        (house_type,bedroom,bathroom,rent_price,gender_requirement,title,address,city,url,time,time_limit,distance,rent_type) " \
            "values(?,?,?,?,?,?,?,?,?,?,?,?,?)"
        db=getDB()
        cur=db.cursor()
        cur.execute(sql,[self.house_type,self.bedroom,self.bathroom,self.rent_price,
                         self.gender_requirement,self.title,self.address,self.city,self.url
                             ,self.time,self.time_limit,self.distance,self.rent_type])
        db.commit()
        cur.close()
        db.close()

def getDB():
    # db = pymysql.connect("localhost", "root", "123456", "RentInf")
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    sqlite_filename = os.path.join(BASE_PATH, 'yeeyitable.db')
    db=sqlite3.connect(sqlite_filename)
    return db

db = getDB()
cur = db.cursor()
cur.execute('select time,id from mytable')
datas=cur.fetchall()
for data in datas:
    time=data[0]
    id = data[1]
    times=time.split('-')
    if len(times[2])<2:
        times[2]='0'+times[2]
    time=times[0]+'-'+times[1]+'-'+times[2]
    print(time)
    cur.execute('update mytable set time = ?  where id= ?', (time, id))
db.commit()
