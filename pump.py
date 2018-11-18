#!/usr/bin/python

import time
import RPi.GPIO as io

io.setmode(io.BOARD)
io.setwarnings(False)

# define pins
pump_pin = 38
io.setup(pump_pin, io.OUT)

def pump_water(time_sec):
    if time_sec > 10:
        print('No')
        return
    io.output(pump_pin, io.HIGH)
    time.sleep(time_sec)
    io.output(pump_pin, io.LOW)

pump_time = 1.0
pump_water(pump_time)

