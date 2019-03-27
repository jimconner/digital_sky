# Rainbow animation
# Rotating rainbow across the whole strip.

import sys, traceback, random
from numpy import array,full

class animation():
    def __init__(self,datastore):
        self.colour_pos=0
        self.max_led=datastore.LED_COUNT

    def Wheel(self, WheelPos):
        WheelPos = 255 - WheelPos
        if WheelPos < 85:
            return [255-WheelPos*3,0,WheelPos*3,0]
        if WheelPos < 170:
            WheelPos -= 85
            return [0, WheelPos*3,255-WheelPos*3,0]
        WheelPos -= 170
        return [WheelPos*3,255-WheelPos*3, 0, 0]

    def emit_row(self):
        try:
            if self.colour_pos == 255:
                self.colour_pos = 0
            else:
                self.colour_pos += 1
            row_arr=full((self.max_led,4),0)
            for i in range(self.max_led):
                wheelVal = self.Wheel((int(i * 256 / self.max_led) + self.colour_pos) & 255)
                row_arr[i]=wheelVal
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)
