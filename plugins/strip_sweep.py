# Sweep animation
# Moves a dot from one side to the other, one pixel at a time.

import sys, traceback, random
from numpy import array,full

class strip_animation():
    def __init__(self,datastore):
        self.sweep_pos=0
        self.colpos=0
        self.max_led=datastore.LED_COUNT
        self.lamp_length=datastore.LAMP_LENGTH
        self.brightness_scaling=255/self.lamp_length

    def emit_row(self):
        try:
            if self.sweep_pos == 0:
                self.colpos=(self.colpos+1) %4 
            self.sweep_pos = (self.sweep_pos +1) % (self.max_led-1)

            row_arr=full((self.max_led,4),0)
            brt=int((self.sweep_pos % self.lamp_length)*self.brightness_scaling)
            row_arr[(((int(self.sweep_pos/self.lamp_length)-1)*self.lamp_length)) % self.max_led][self.colpos]=255-brt
            row_arr[int(self.sweep_pos/self.lamp_length)*self.lamp_length][self.colpos]=255
            row_arr[(((int(self.sweep_pos/self.lamp_length)+1)*self.lamp_length)) % self.max_led][self.colpos]=brt
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

