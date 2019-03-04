# Controller code for Digital Sky lighting project.
# This code is based upon the low level python wrapper for rpi_ws281x library
# which was produced by Tony DiCola (tony@tonydicory0x000080,a.com), Jeremy Garff (jer@jers.net)
# This code will animate a number of WS281x LEDs, and a number of LED Strips driven of WS2811 ICs on the same neopixel bus.
import sys,time, urllib, traceback, random

from PIL import Image
from numpy import array, bitwise_xor, dstack, full
from neopixel import *
from twisted.internet import stdio, reactor
from twisted.internet.task import LoopingCall
from twisted.protocols import basic
from twisted.web import client
from twisted.web.resource import Resource
from effects import sweep, the_chase, image_repeater
from cli import CLICommandProtocol
from led_control import LED_Control

if len(sys.argv) != 2 : 
    print("Usage: "+sys.argv[0]+" <url_for_jpg_file>")
    sys.exit(1)

# LED strip configuration:
LED_COUNT      = 210      # Number of LED pixels.

class Datastore_Data(Resource):
    def __init__(self):
        self.ww = 0
        self.nw = 0
        self.ib = 0
        self.dw = 0
        self.np = 0

datastore=Datastore_Data()
lights=LED_Control(datastore, LED_COUNT)

if __name__ == "__main__":
    stdio.StandardIO(CLICommandProtocol(datastore))
    LEDTask = LoopingCall(lights.service_leds)
    LEDTask.start(0.03)
    reactor.run()

