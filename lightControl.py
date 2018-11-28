#!/usr/bin/python3
# ----------- MAIN -----------

# --- Light Control ----
# Have to install some libraries first, look on:
# https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
import time
import board
import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
# D18 is same as GPIO18 on board.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 256

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

# Turn on light to all white, will stay on until turned off
# Comment this line out if you have RGBW/GRBW NeoPixels
pixels.fill((255, 255, 255))
pixels.show()

# -- End of Light Control ---
