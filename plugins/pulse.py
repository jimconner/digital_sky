# Pulse strip_animation
# A single ramp up/down in brightness on the ice blue strips.

import sys, traceback, random
from numpy import array,full

class strip_animation():
    def __init__(self,datastore):
        self.brightness=0
        self.direction=0
        self.datastore=datastore

    def emit_row(self):
        try:
            if self.direction == 0:
                self.brightness += 30
                if self.brightness >= 240:
                    self.direction=1
            else:
                self.brightness -= 40
                if self.brightness <= 0:
                    self.datastore.del_by_class(self)
            row_arr=full((self.datastore.LED_COUNT,4),[0, 0, self.brightness, 0])
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

