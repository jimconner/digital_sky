#!/usr/bin/env python
# Controller code for Digital Sky lighting project.
# This code is utilises the low level python wrapper for rpi_ws281x library
# which was produced by Tony DiCola (tony@tonydicory0x000080,a.com), Jeremy Garff (jer@jers.net)
# This code will animate a number of WS281x LEDs, and a number of LED Strips driven of WS2811 ICs on the same neopixel bus.

import sys,time, os, urllib.request, urllib.parse, urllib.error, traceback, random, core.subscriber, importlib
import RPi.GPIO as GPIO
from PIL import Image
from numpy import array, bitwise_xor, full, uint8
from neopixel import *
from mqtt.client.factory import MQTTFactory
from core.subscriber import MQTTService
from twisted.application.internet import ClientService, backoffPolicy
from twisted.internet import stdio, reactor
from twisted.internet.task import LoopingCall
from twisted.internet.defer       import inlineCallbacks, DeferredList
from twisted.internet.endpoints   import clientFromString
from twisted.protocols import basic
from twisted.python import components
from twisted.web import client
from twisted.web.resource import Resource
from core.led_control import LED_Control
from core.ssh import *
from twisted.logger   import (
    Logger, LogLevel, globalLogBeginner, textFileLogObserver, 
    FilteringLogObserver, LogLevelFilterPredicate)
from settings import * 

class Datastore_Data(Resource):
    def __init__(self):
        self.LED_COUNT=LED_COUNT  # Total number of addressable pixels (including those which have strips attached)
        self.LAMP_LENGTH=LAMP_LENGTH # The length of each lamp module
        self.STRIP_LEDS=STRIP_LEDS   # The number of pixels at the start of each lamp which are special
        self.IMAGES=IMAGES # Image name to URL mapping definitions 
        #FUTURE# self.strip_vals = full(int((self.LED_COUNT/self.LAMP_LENGTH)*self.STRIP_LEDS),4),0, dtype=uint8)
        self.strip_vals = array([0,0,0,0], dtype=uint8)
        self.master_brightness = 1.0
        self.rgbw_brightness = [1.0,1.0,1.0,1.0]
        self.strips = full((self.LED_COUNT,4),0)
        self.plugins = []
        self.animations=[]
        self.strip_animations=[]
        self.filters=[]
        self.power=0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(15, GPIO.OUT)
        GPIO.output(15, GPIO.LOW)
        
    def add_animation(self, pluginname, extra=None, extra2=None):
          """ Add an instance of a plugin to the running animations list"""
          for plugin in self.plugins:
              if plugin.__name__[8:] == pluginname:
                  if 'animation' in dir(plugin):
                      if extra == None:
                          self.animations.append(plugin.animation(self))
                      else:
                          self.animations.append(plugin.animation(self, extra, extra2))
                  elif 'strip_animation' in dir(plugin):
                      if extra == None:
                          self.strip_animations.append(plugin.strip_animation(self))
                      else:
                          self.strip_animations.append(plugin.strip_animation(self, extra, extra2))
                  	
    def del_animation(self, pluginname):
          """ Add an instance of a plugin to the running animations list"""
          for animation in self.animations:
              if animation.__module__[8:] == pluginname:
                  self.animations.remove(animation)
          for strip_animation in self.strip_animations:
              if strip_animation.__module__[8:] == pluginname:
                  self.strip_animations.remove(strip_animation)
                  
    def del_by_class(self, plugin):
        print("Removing: ", plugin)
        self.strip_animations.remove(plugin)

    def set_power(self, state):
        print("Setting Power: ", state)
        self.power=int(state)
        if self.power == 0:
            GPIO.output(15, GPIO.LOW)
        else:
            GPIO.output(15, GPIO.HIGH)
        
                  
class SSHCLIFactory(factory.SSHFactory):
    protocol = SSHServerTransport
    publicKeys = {
        b'ssh-rsa': keys.Key.fromFile(SERVER_RSA_PUBLIC)
    }
    privateKeys = {
        b'ssh-rsa': keys.Key.fromFile(SERVER_RSA_PRIVATE)
    }
    # Service handlers.
    services = {
        b'ssh-userauth': userauth.SSHUserAuthServer,
        b'ssh-connection': connection.SSHConnection
    }
           

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
    portal = portal.Portal(ExampleRealm(datastore))
    passwdDB = InMemoryUsernamePasswordDatabaseDontUse()
    #passwdDB.addUser(b'dumbuser', b'badpassword')
    sshDB = SSHPublicKeyChecker(InMemorySSHKeyDB(
        {b'jim': [keys.Key.fromFile(CLIENT_RSA_PUBLIC)]}))
    portal.registerChecker(passwdDB)
    portal.registerChecker(sshDB)
    SSHCLIFactory.portal = portal
    SSHCLIFactory.datastore = datastore
    components.registerAdapter(ExampleSession, ExampleAvatar, session.ISession)
    for filename in os.listdir('plugins'):
        if filename == '__init__.py' or filename[-3:] != '.py':
            continue
        datastore.plugins.append(importlib.import_module('plugins.'+filename[:-3]))
    del filename
    datastore.add_animation('set_strips') # Lazy hack to ensure set_strips is available - FIXME later.
    lights=LED_Control(datastore)
    LEDTask = LoopingCall(lights.service_leds)
    LEDTask.start(0.02)
    log = Logger()
    startLogging()
    setLogLevel(namespace='mqtt',     levelStr='debug')
    setLogLevel(namespace='__main__', levelStr='debug')
    factory    = MQTTFactory(profile=MQTTFactory.SUBSCRIBER)
    myEndpoint = clientFromString(reactor, BROKER)
    serv       = MQTTService(myEndpoint, factory, log, datastore)
    serv.startService()
    reactor.listenTCP(5022, SSHCLIFactory())
    reactor.run()
