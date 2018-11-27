#!/usr/bin/python

import RPi.GPIO as io
import time

io.setmode(io.BOARD)
io.setwarnings(False)

pump_pin = 38
io.setup(pump_pin, io.OUT)

def pump_water(time_sec):
    if time_sec > 10:
        print('No')
        return
    io.output(pump_pin, io.HIGH)
    time.sleep(time_sec)
    io.output(pump_pin, io.LOW)


# ---- MAIN() ----

pump_water(3)

