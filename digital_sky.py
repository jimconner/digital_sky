#!/usr/bin/env python
# Controller code for Digital Sky lighting project.
# This code is based upon the low level python wrapper for rpi_ws281x library
# which was produced by Tony DiCola (tony@tonydicory0x000080,a.com), Jeremy Garff (jer@jers.net)
# This code will animate a number of WS281x LEDs, and a number of LED Strips driven of WS2811 ICs on the same neopixel bus.
import sys,time, urllib, traceback, random
import subscriber

from PIL import Image
from numpy import array, bitwise_xor, dstack, full, uint8
from neopixel import *
from mqtt.client.factory import MQTTFactory
from subscriber import MQTTService
from twisted.application.internet import ClientService, backoffPolicy
from twisted.internet import stdio, reactor
from twisted.internet.task import LoopingCall
from twisted.internet.defer       import inlineCallbacks, DeferredList
from twisted.internet.endpoints   import clientFromString
from twisted.protocols import basic
from twisted.web import client
from twisted.web.resource import Resource
from cli import CLICommandProtocol
from led_control import LED_Control
from twisted.logger   import (
    Logger, LogLevel, globalLogBeginner, textFileLogObserver, 
    FilteringLogObserver, LogLevelFilterPredicate)
from animations import *

if len(sys.argv) != 2 : 
    print("Usage: "+sys.argv[0]+" <url_for_jpg_file>")
    sys.exit(1)


class Datastore_Data(Resource):
    def __init__(self):
        self.strip_vals = [0,0,0,0]
        self.strips = full((LED_COUNT,4),0, dtype=uint8)
        self.animations=[ \
                image_repeater.image_repeater(LED_COUNT, sys.argv[1]), \
                crumbling_in.crumbling_in(LED_COUNT), \
                sweep.sweep(LED_COUNT), \
                the_chase.the_chase(LED_COUNT), \
                #bar.bar(LED_COUNT) 
                ]
        self.strip_animations=[ \
                #inverse_strip_sweep.inverse_strip_sweep(LED_COUNT), \
                set_strips.set_strips(LED_COUNT, self), \
                ]
        self.filters=[]

# ----------------
# Global variables
# ----------------

# Global object to control globally namespace logging
logLevelFilterPredicate = LogLevelFilterPredicate(defaultLogLevel=LogLevel.info)
# LED strip configuration:
LED_COUNT      = 210      # Number of LED pixels.
# MQTT Service to subscribe to
BROKER = "tcp:localhost:1883"


# -----------------
# Utility Functions
# -----------------

def startLogging(console=True, filepath=None):
    '''
    Starts the global Twisted logger subsystem with maybe
    stdout and/or a file specified in the config file
    '''
    global logLevelFilterPredicate
   
    observers = []
    if console:
        observers.append( FilteringLogObserver(observer=textFileLogObserver(sys.stdout),  
            predicates=[logLevelFilterPredicate] ))
    if filepath is not None and filepath != "":
        observers.append( FilteringLogObserver(observer=textFileLogObserver(open(filepath,'a')), 
            predicates=[logLevelFilterPredicate] ))
    globalLogBeginner.beginLoggingTo(observers)


def setLogLevel(namespace=None, levelStr='info'):
    '''
    Set a new log level for a given namespace
    LevelStr is: 'critical', 'error', 'warn', 'info', 'debug'
    '''
    level = LogLevel.levelWithName(levelStr)
    logLevelFilterPredicate.setLogLevelForNamespace(namespace=namespace, level=level)


if __name__ == "__main__":
    datastore=Datastore_Data()
    lights=LED_Control(datastore, LED_COUNT)
    stdio.StandardIO(CLICommandProtocol(datastore))
    LEDTask = LoopingCall(lights.service_leds)
    LEDTask.start(0.01)
    log = Logger()
    startLogging()
    setLogLevel(namespace='mqtt',     levelStr='debug')
    setLogLevel(namespace='__main__', levelStr='debug')
    factory    = MQTTFactory(profile=MQTTFactory.SUBSCRIBER)
    myEndpoint = clientFromString(reactor, BROKER)
    serv       = MQTTService(myEndpoint, factory, log, datastore)
    serv.startService()
    reactor.run()

