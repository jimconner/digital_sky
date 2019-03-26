# Crumbling In
# Like randomised coloured dots and then they
# increase on both sides getting closer and closer into the middle.

import sys, traceback, random
from numpy import array,full

class animation():
    def __init__(self,datastore):
        self.max_led = datastore.LED_COUNT
        self.pos = 0
        self.direction=0
        self.cols = [ \
                [255,0,0,0], \
                [0,255,0,0], \
                [0,0,255,0], \
                [0,0,0,255], \
                [255,255,0,0], \
                [255,0,255,0], \
                [0,255,255,0], \
                [0,0,255,64], \
                ]
        self.row=full((self.max_led,4),0)

    def emit_row(self):
        try:
            if self.pos >= self.max_led/2:
                self.direction=1
            if self.pos <= 0:
                self.direction=0
            col=self.cols[random.randint(0,7)]
            if self.direction==1:
                col=[0,0,0,0]
            self.row[self.pos]=col
            self.row[(self.max_led-1)-self.pos]=col
            if self.direction==0:
                self.pos+=1
            else:
                self.pos-=1

            return self.row
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)
