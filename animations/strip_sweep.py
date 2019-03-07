# Sweep animation
# Moves a dot from one side to the other, one pixel at a time.

import sys, traceback, random
from numpy import array,full

class strip_sweep():
    def __init__(self,max_led):
        self.sweep_pos=0
        self.max_led=max_led

    def emit_row(self):
        try:
            self.sweep_pos = (self.sweep_pos +1) % (self.max_led-1)
            row_arr=full((self.max_led,4),0)
            brt=(self.sweep_pos % 30)*8
            brtlo=240-(self.sweep_pos % 30)*8 
            brthi=(self.sweep_pos % 30) *8
            row_arr[int(((self.sweep_pos/30)-1)*30 % self.max_led)]=[0,brtlo,0,0]
            row_arr[int(self.sweep_pos/30)*30]=[0,240,0,0]
            row_arr[int(((self.sweep_pos/30)+1)*30 % self.max_led)]=[0,brthi,0,0]
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

