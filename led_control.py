# Controller code for Digital Sky lighting project.
# This code is based upon the low level python wrapper for rpi_ws281x library
# which was produced by Tony DiCola (tony@tonydicory0x000080,a.com), Jeremy Garff (jer@jers.net)
# This code will animate a number of WS281x LEDs, and a number of LED Strips driven of WS2811 ICs on the same neopixel bus.
import sys,time, urllib, traceback, random
from PIL import Image
from numpy import array, bitwise_xor, dstack, full
from neopixel import *
from effects.sweep import sweep
from effects.bar import bar
from effects.the_chase import the_chase
from effects.image_repeater import image_repeater
from effects.crumbling_in import crumbling_in
from filters.make_it_red import make_it_red

# LED strip configuration:
# LED_COUNT    = <whevs> # This value is now passed in as a parameter when LED_Control is instanciated.
LAMP_LENGTH    = 30      # Number of LEDs per lamp fixture.
STRIP_LEDS     = 3       # The number of LEDs per lamp fixture which are actually driving entire strips instead of RGB
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.SK6812W_STRIP

class LED_Control():
    def __init__(self, datastore, LED_COUNT):
        self.datastore = datastore
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        self.strip.begin()
        self.LED_COUNT=LED_COUNT
        self.effects=[ \
                #image_repeater(LED_COUNT, sys.argv[1]), \
                #sweep(LED_COUNT), \
                the_chase(LED_COUNT), \
                crumbling_in(LED_COUNT), \
                #bar(LED_COUNT) 
                ]
        self.filters=[]

    def service_leds(self):
        try:
            # Set up an empty blank row of RGBW pixels
            rowdata=full((self.LED_COUNT,4),0)
            # XOR on each pixel source effect in turn.
            for effect in self.effects:
                rowdata=bitwise_xor(rowdata, effect.emit_row())
            # Pass the resulting rowdata through each filter in turn
            for filt in self.filters:
                rowdata=filt(rowdata)
            # Update each LED color in the buffer.
            for i in range(self.strip.numPixels()):
                if i % LAMP_LENGTH < STRIP_LEDS:
                        self.strip.setPixelColor(i, Color(self.datastore.ib,self.datastore.ww,self.datastore.nw,self.datastore.dw))
                else:
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

