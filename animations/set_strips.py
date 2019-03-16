# Set Strips
# Set the strip leds to preset levels.

import sys, traceback, random
from numpy import array,full

class set_strips():
    def __init__(self,max_led,datastore):
        self.max_led=max_led
        self.datastore=datastore

    def emit_row(self):
        try:
            row_arr=full((self.max_led,4),[self.datastore.strip_vals[0], self.datastore.strip_vals[1], self.datastore.strip_vals[2], self.datastore.strip_vals[3]])
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

