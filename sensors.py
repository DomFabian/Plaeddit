#!/usr/bin/python

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def get_sensor_values():
    values = [0]*8
    for i in range(0, 8):
        values[i] = mcp.read_adc(i)
    return values
