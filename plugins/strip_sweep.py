# Sweep animation
# Moves a dot from one side to the other, one pixel at a time.

import sys, traceback, random
from numpy import array,full

class strip_animation():
    def __init__(self,datastore):
        self.sweep_pos=0
        self.colpos=0
        self.max_led=datastore.LED_COUNT

    def emit_row(self):
        try:
            if self.sweep_pos == 0:
                self.colpos=(self.colpos+1) %4 
            #if random.randint(0,10) >= 9:
            #    if random.randint(0,4) == 1:
            #        self.sweep_pos = (self.sweep_pos -1) % (self.max_led-1)
            #    else:
            #        self.sweep_pos = (self.sweep_pos +1) % (self.max_led-1)
            self.sweep_pos = (self.sweep_pos +1) % (self.max_led-1)

            row_arr=full((self.max_led,4),0)
            brt=(self.sweep_pos % 30)*8
            brtlo=240-(self.sweep_pos % 30)*8 
            brthi=(self.sweep_pos % 30) *8
            row_arr[(((int(self.sweep_pos/30)-1)*30)) % self.max_led][self.colpos]=brtlo
            row_arr[int(self.sweep_pos/30)*30][self.colpos]=240
            row_arr[(((int(self.sweep_pos/30)+1)*30)) % self.max_led][self.colpos]=brthi
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

