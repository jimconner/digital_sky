# Sweep animation
# Moves a dot from one side to the other, one pixel at a time.

import sys, traceback, random
from numpy import array,full

class sweep():
    def __init__(self,max_led):
        self.sweep_pos=0
        self.max_led=max_led

    def emit_row(self):
        try:
            if self.sweep_pos == self.max_led-1:
                self.sweep_pos = 0
            else:
                self.sweep_pos += 1
            row_arr=full((self.max_led,4),0)
            row_arr[self.sweep_pos]=[255,255,255,255]
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

