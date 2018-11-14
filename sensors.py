#!/usr/bin/python

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_DHT

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# define sensor pins
humid_temp = 5

# returns an array of the 8 MCP3008 channels
def get_mcp3008_values():
    values = [0]*8
    for i in range(0, 8):
        values[i] = mcp.read_adc(i)
    return values

# convert Celsius to Fahrenheit because America
def C_to_F(celsius):
    return celsius * 9.0/5.0 + 32.0

# tries like 15 times to get the values, fails sometimes and returns None, None
def get_humidity_and_temp():
    return Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, humid_temp)

humidity, temperature = get_humidity_and_temp()
temperature = C_to_F(temperature)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get humidity and temperature.')

