# Bar animation
# Moves a dot from one side to the other, one pixel at a time.

import sys, traceback, random
from numpy import array,full

class animation():
    def __init__(self,datastore):
        self.pos=0
        self.max_led=datastore.LED_COUNT

    def emit_row(self):
        try:
            direction=random.randint(-1,1)
            amt=random.randint(1,5)
            self.pos = self.pos+(direction*amt)
            if self.pos >= self.max_led:
                self.pos = self.max_led-1
            if self.pos <= -self.max_led:
                self.pos = -self.max_led
            row_arr=full((self.max_led,4),0)
            if self.pos >= 0:
                for i in range(self.pos):
                    row_arr[i]=[0,255,0,0]
            else:
                for i in range(self.max_led-1,self.max_led+self.pos,-1):
                    row_arr[i]=[0,255,0,0]
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

