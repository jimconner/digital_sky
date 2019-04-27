# Sweep animation
# Moves a dot from one side to the other, one pixel at a time.

import sys, traceback, random
from numpy import array,full

class animation():
    def __init__(self,datastore):
        self.pos=0
        self.max_led=datastore.LED_COUNT

    def emit_row(self):
        try:
            if self.pos == self.max_led-1:
                self.pos = 0
            else:
                self.pos += 1
            row_arr=full((self.max_led,4),0)
            row_arr[self.pos]=[255,255,255,255]
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

