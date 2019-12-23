# Controller code for Digital Sky lighting project.
# This code is based upon the low level python wrapper for rpi_ws281x library
# which was produced by Tony DiCola (tony@tonydicory0x000080,a.com), Jeremy Garff (jer@jers.net)
# This code will animate a number of WS281x LEDs, and a number of LED Strips driven of WS2811 ICs on the same neopixel bus.
import sys,time, urllib.request, urllib.parse, urllib.error, traceback, random
from PIL import Image
from numpy import array, bitwise_xor, clip, greater, dstack, full, uint8, maximum
from neopixel import *
from filters.make_it_red import make_it_red

# LED strip configuration:
POWER_PIN      = 15      # GPIO pin which controlls the 36V power supply.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.SK6812W_STRIP

class LED_Control():
    def __init__(self, datastore):
        self.datastore = datastore
        self.strip = Adafruit_NeoPixel(self.datastore.LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        self.strip.begin()


    def service_leds(self):
        try:
            if self.datastore.power != 0: 
                # Set up an empty blank row of Strip pixels
                self.datastore.strips=full((self.datastore.LED_COUNT,4),0)
                for animation in self.datastore.strip_animations:
                    self.datastore.strips=maximum(self.datastore.strips, animation.emit_row())
                # Set up an empty blank row of RGBW pixels
                rowdata=full((self.datastore.LED_COUNT,4),0)
                for animation in self.datastore.animations:
                    rowdata=maximum(rowdata, animation.emit_row())
                # Scale RGBW elements individually (colour tint)
                rowdata=rowdata*self.datastore.rgbw_brightness           
                # Then scale everything by master_brightness
                rowdata=rowdata*float(self.datastore.master_brightness)
                rowdata=uint8(rowdata)
                # Update each LED color in the buffer.
                for i in range(self.strip.numPixels()):
                    if i % self.datastore.LAMP_LENGTH < self.datastore.STRIP_LEDS:
                        #self.strip.setPixelColor(i, Color(ib,ww,nw,dw))
     
                         self.strip._led_data[i]=(int(self.datastore.strips[i][3]) << 24) | \
                                                 (int(self.datastore.strips[i][0]) << 16) | \
                                                 (int(self.datastore.strips[i][1]) << 8 ) | \
                                                  int(self.datastore.strips[i][2])   
                    else:
                    # Set the LED color buffer value.
                        #self.strip.setPixelColor(i, Color(r,g,b,w))
                        self.strip._led_data[i]=(int(rowdata[i][3]) << 24) | \
                                                (int(rowdata[i][0]) << 16) | \
                                                (int(rowdata[i][1]) << 8 ) | \
                                                 int(rowdata[i][2])
                # Send the LED color data to the hardware.
                self.strip.show()
        except Exception as err:
            print((self.datastore.strips))
            print(err)
            traceback.print_exc(file=sys.stdout)

def Color(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (red << 16)| (green << 8) | blue
