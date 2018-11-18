#!/usr/bin/python
import MySQLdb

servername = "den1.mysql5.gear.host"
username = "plantdata1"
pw = "BestProject!" # need to change to real password
dbname = "plantdata1"

conn = MySQLdb.connect(host=servername, user=username, password=pw, db=dbname)
cur = conn.cursor()

# Query to fetch most recent result
cur.execute('SELECT * FROM   plantdata1.plaeddit_data ORDER  BY dateofcare DESC LIMIT  1;')

# print results
for row in cur.fetchall():
    print row['temperature']
    print row['humidity']
    print row['moisture']
    print row['dateofcare']

conn.close()
