# Sweep animation
# Moves a dot from one side to the other, one pixel at a time.

import sys, traceback, random
from numpy import array,full

class strip_animation():
    def __init__(self,datastore):
        self.max_led=datastore.LED_COUNT
        self.lamp_length=datastore.LAMP_LENGTH

    def emit_row(self):
        try:
            row_arr=full((self.max_led,4),0)
            row_arr[0][0]=255 # Natural White
            row_arr[0][1]=255 # Daylight White
            row_arr[0][3]=255 # Warm White
            row_arr[self.lamp_length][0]=255 # Natural White
            row_arr[self.lamp_length][1]=255 # Daylight White
            row_arr[self.lamp_length][3]=255 # Warm White
            return row_arr
        except Exception as err:
            print(err)
        traceback.print_exc(file=sys.stdout)
