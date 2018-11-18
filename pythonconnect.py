#!/usr/bin/python
import mysql.connector

servername = "den1.mysql5.gear.host"
username = "plantdata1"
pw = "BestProject!" # need to change to real password
dbname = "plantdata1"

cnx = mysql.connector.connect(user=username, password=pw,
                              host=servername,
                              database=dbname)
cur = cnx.cursor()

# Query to fetch most recent result
# cur.execute('SELECT * FROM plantdata1.plaeddit_data ORDER  BY dateofcare DESC LIMIT  1;')

# print results
#for row in cur.fetchall():
#    print "Temperature: " + str(row[0])
#    print "Humidity: " + str(row[1])
#    print "Moisture: " + str(row[2])
#    print "Date of care: " + str(row[3])

# Query to insert into database
tempval = 19
humidityval = 19
moistureval = 19
query = 'insert into plantdata1.plaeddit_data (temperature, humidity, moisture, dateofcare) values (' + str(tempval) + ', ' + str(humidityval) + ', ' + str(moistureval) + ', CURRENT_TIMESTAMP);'
cur.execute(query)
cnx.commit()

cnx.close()
