# Plug a speaker into the audio jack of Pi
#
# Follow these commands:
# https://www.dexterindustries.com/howto/make-your-raspberry-pi-speak/

#!/usr/bin/python
from num2words import num2words
from subprocess import call
import mysql.connector
import datetime

servername = "den1.mysql5.gear.host"
username = "plantdata1"
pw = "BestProject!" # need to change to real password
dbname = "plantdata1"

cnx = mysql.connector.connect(user=username, password=pw,
                              host=servername,
                              database=dbname)
cur = cnx.cursor()

# Query to fetch most recent result
cur.execute('SELECT * FROM plantdata1.plaeddit_data ORDER  BY dateofcare DESC LIMIT  1;')

temp_value = 0
humid_val = 0
mois_val = 0
date = ""

# Fetch results
for row in cur.fetchall():
    temp_value = row[0]
    humid_value = row[1]
    mois_value = row[2]
    date = str(row[3])

cmd_beg= 'espeak -ven+f2'
cmd_end= ' | aplay /home/pi/Desktop/Text.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
cmd_out= '--stdout > /home/pi/Desktop/Text.wav ' # To store the voice file

# FIXME: need to get temp_value, mois_value, humid_value
now = datetime.datetime.now()

text = '''Welcome_to_the_Daily_Plant_Update._Thanks_for_tuning_in._
Today_is_''' + str(now.month()) + '''_''' + str(now.day())
+ '''_''' + str(now.year()) + '''._The_current_temperature_of_the_plant_
is_''' + str(temp_value) + '''_degrees_Farenheit._''' + '''.The_current_humidity_of_the_plant_
is_''' + str(humid_value) + '''_percent._''' + '''.The_current_moisture_of_the_plant_
is_''' + str(mois_value) + '''_percent._Do_not_forget_to_comment_on_todays_post_to
_help_care_for_the_plant!'''

#Calls the Espeak TTS Engine to read aloud a Text
call([cmd_beg+cmd_out+text+cmd_end], shell=True)
