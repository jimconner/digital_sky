# Set Strips
# Set the strip leds to preset levels.

import sys, traceback, random
from numpy import array, full

class strip_animation():
    def __init__(self,datastore):
        self.datastore=datastore

    def emit_row(self):
        try:
            row_arr=full((self.datastore.LED_COUNT,4),0)
            for lamp in range(0, int(self.datastore.LED_COUNT / self.datastore.LAMP_LENGTH)):
                row_arr[ (self.datastore.LAMP_LENGTH * lamp) ]=[int(self.datastore.strip_vals[0]), int(self.datastore.strip_vals[1]), int(self.datastore.strip_vals[2]), int(self.datastore.strip_vals[3])]
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)
