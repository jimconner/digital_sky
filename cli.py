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

class CLICommandProtocol(basic.LineReceiver):
    delimiter = b'\n' # unix terminal style newlines. remove this line
                      # for use with Telnet
    def __init__(self, datastore):
        self.datastore = datastore

    def connectionMade(self):
        self.sendLine(b"Web checker console. Type 'help' for help.")

    def lineReceived(self, line):
        # Ignore blank lines
        if not line: return
        line = line.decode("ascii")

        # Parse the command
        commandParts = line.split()
        command = commandParts[0].lower()
        args = commandParts[1:]

        # Dispatch the command to the appropriate method.  Note that all you
        # need to do to implement a new command is add another do_* method.
        try:
            method = getattr(self, 'do_' + command)
        except AttributeError as e:
            self.sendLine(b'Error: no such command.')
        else:
            try:
                method(*args)
            except Exception as e:
                self.sendLine(b'Error: ' + str(e).encode("ascii"))

    def do_help(self, command=None):
        """help [command]: List commands, or show help on the given command"""
        if command:
            doc = getattr(self, 'do_' + command).__doc__
            self.sendLine(doc.encode("ascii"))
        else:
            commands = [cmd[3:].encode("ascii")
                        for cmd in dir(self)
                        if cmd.startswith('do_')]
            self.sendLine(b"Valid commands: " + b" ".join(commands))

    def do_quit(self):
        """quit: Quit this session"""
        self.sendLine(b'Goodbye.')
        self.transport.loseConnection()
        
    def do_check(self, url):
        """check <url>: Attempt to download the given web page"""
        url = url.encode("ascii")
        client.Agent(reactor).request(b'GET', url).addCallback(
            client.readBody).addCallback(
            self.__checkSuccess).addErrback(
            self.__checkFailure)

    def __checkSuccess(self, pageData):
        msg = "Success: got {} bytes.".format(len(pageData))
        self.sendLine(msg.encode("ascii"))

    def __checkFailure(self, failure):
        msg = "Failure: " + failure.getErrorMessage()
        self.sendLine(msg.encode("ascii"))

    def connectionLost(self, reason):
        # stop the reactor, only because this is meant to be run in Stdio.
        reactor.stop()

    def do_ib(self, pos, val):
        """Set level if Ice Blue strips (0-255)"""
        self.datastore.strips[int(pos)][0] = int(val)

    def do_dw(self, pos, val):
        """Set level if Daylight White strips (0-255)"""
        self.datastore.strips[int(pos)][1] = int(val)

    def do_nw(self, pos, val):
        """Set level if Natural White strips (0-255)"""
        self.datastore.strips[int(pos)][2] = int(val)

    def do_ww(self, pos, val):
        """Set level if Warm White strips (0-255)"""
        self.datastore.strips[int(pos)][3] = int(val)

