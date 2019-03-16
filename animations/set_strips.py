# Set Strips
# Set the strip leds to preset levels.

import sys, traceback, random
from numpy import array,full

class set_strips():
    def __init__(self,max_led,ib,ww,nw,dw):
        self.max_led=max_led
	self.ww=ww
	self.ib=ib
	self.dw=dw
	self.nw=nw

    def emit_row(self):
        try:
            row_arr=full((self.max_led,4),[self.ww, self.ib, self.nw, self.dw])
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

