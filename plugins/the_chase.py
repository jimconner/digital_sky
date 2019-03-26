# The Chase
# Two dots which move forward either zero, one or two pixels at a time based on random chance.
# .. kind of like one is chasing the other.. but a bit crap

import sys, traceback, random
from numpy import array,full

class animation():
    def __init__(self,datastore):
        self.chaser1 = 0
        self.chaser2 = 0
        self.max_led = datastore.LED_COUNT

    def emit_row(self):
        try:
            self.chaser1 = (self.chaser1 + random.randint(0,2)) % self.max_led
            self.chaser2 = (self.chaser2 + random.randint(0,2)) % self.max_led
            row_arr=full((self.max_led,4),0)
            row_arr[self.chaser1]=[255,0,0,0]
            row_arr[self.chaser2]=[0,0,255,0]
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)
