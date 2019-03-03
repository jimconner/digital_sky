# Example of low-level Python wrapper for rpi_ws281x library.
# Author: Tony DiCola (tony@tonydicory0x000080,a.com), Jeremy Garff (jer@jers.net)
#
# This is an example of how to use the SWIG-generated _rpi_ws281x module.
# You probably don't want to use this unless you are building your own library,
# because the SWIG generated module is clunky and verbose.  Instead look at the
# high level Python port of Adafruit's NeoPixel Arduino library in strandtest.py.
#
# This code will animate a number of WS281x LEDs displaying rainbow colors.
import sys,time, urllib, traceback, random

from PIL import Image
from numpy import array,bitwise_xor,dstack,full
from neopixel import *
from twisted.internet import stdio, reactor
from twisted.internet.task import LoopingCall
from twisted.protocols import basic
from twisted.web import client
from twisted.web.resource import Resource

if len(sys.argv) != 2 : 
    print("Usage: "+sys.argv[0]+" <url_for_jpg_file>")
    sys.exit(1)

# LED strip configuration:
LED_COUNT      = 210      # Number of LED pixels.
LAMP_LENGTH    = 30      # Number of LEDs per lamp fixture.
STRIP_LEDS     = 3       # The number of LEDs per lamp fixture which are actually driving entire strips instead of RGB
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.SK6812W_STRIP

class Datastore_Data(Resource):
    def __init__(self):
        self.ww = 0
        self.nw = 0
        self.ib = 0
        self.dw = 0
        self.np = 0

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

    def do_ib(self, val):
        """Set level if Ice Blue strips (0-255)"""
        self.datastore.ib = int(val)

    def do_dw(self, val):
        """Set level if Daylight White strips (0-255)"""
        self.datastore.dw = int(val)

    def do_nw(self, val):
        """Set level if Natural White strips (0-255)"""
        self.datastore.nw = int(val)

    def do_ww(self, val):
        """Set level if Warm White strips (0-255)"""
        self.datastore.ww = int(val)

    def do_np(self, val):
        """Set level if Neopixel Warm White strips (0-255)"""
        self.datastore.np = int(val)

class LED_Control():
    def __init__(self, datastore):
        self.datastore = datastore
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        urllib.urlretrieve(sys.argv[1], "file.jpg")
        img = Image.open("file.jpg")
        self.img = img.resize((self.strip.numPixels(),img.size[0]), Image.ANTIALIAS) # Resize width to match number of pixels.
        img_tmp = array(self.img)
        b_tmp=full((img_tmp.shape[0],img_tmp.shape[1],1),0) # An extra 2D array of single bytes to store 6812B WW pixel data
        self.arr=dstack((img_tmp,b_tmp)) # Stack the extra bytes onto the 24bpp array to get 32bpp
        self.row = 0
        self.strip.begin()
        self.sweep_pos = 0
        self.chaser1 = 0
        self.chaser2 = 0

    def the_chase(self):
        # print("Image Row: ", self.row)
        try:
            self.chaser1 = (self.chaser1 + random.randint(-2,2)) % LED_COUNT
            self.chaser2 = (self.chaser2 + random.randint(-2,2)) % LED_COUNT
            row_arr=full((self.img.size[0],4),0)
            row_arr[self.chaser1]=[255,0,0,0]
            row_arr[self.chaser2]=[0,0,255,0]
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

    def sweep(self):
        # print("Image Row: ", self.row)
        try:
            if self.sweep_pos == LED_COUNT-1:
                self.sweep_pos = 0
            else:
                self.sweep_pos += 1
            row_arr=full((self.img.size[0],4),0)
            row_arr[self.sweep_pos]=[255,255,255,255]
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)


    def image_repeater(self):
        # print("Image Row: ", self.row)
        try:
            if self.row ==len(self.arr)-1:
                self.row = 0
            else:
                self.row += 1
            return self.arr[self.row]
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

    def service_leds(self):
        # print("Image Row: ", self.row)
        # Update each LED color in the buffer.
        try:
            data1=self.image_repeater()
            data2=self.the_chase()
            data3=self.sweep()
            rowdata=bitwise_xor(data1, data2, data3)
            for i in range(self.strip.numPixels()):
                if i % LAMP_LENGTH < STRIP_LEDS:
                        self.strip.setPixelColor(i, Color(self.datastore.ib,self.datastore.ww,self.datastore.nw,self.datastore.dw))
                else:
                    # Pick a color based on LED position and an offset for animation.
                    # color = DOT_COLORS[(i + offset) % len(DOT_COLORS)]
                    r=int(rowdata[i][0])
                    g=int(rowdata[i][1])
                    b=int(rowdata[i][2])
                    w=int(rowdata[i][3])
                # Set the LED color buffer value.
                    self.strip.setPixelColor(i, Color(r,g,b,w))
            # Send the LED color data to the hardware.
            self.strip.show()
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)



datastore=Datastore_Data()
lights=LED_Control(datastore)

if __name__ == "__main__":
    stdio.StandardIO(CLICommandProtocol(datastore))
    LEDTask = LoopingCall(lights.service_leds)
    LEDTask.start(0.03)
    reactor.run()

