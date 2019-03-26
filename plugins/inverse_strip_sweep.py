# Sweep animation
# Moves a dot from one side to the other, one pixel at a time.

import sys, traceback, random
from numpy import array,full

class strip_animation():
    def __init__(self,datastore):
        self.max_led=datastore.LED_COUNT
        self.sweep_pos=0
        self.colpos=0
        self.nextpos=0
        self.changestrip=0

    def emit_row(self):
        try:
            if self.changestrip == 0 and random.randint(0,1000) == 800:
                self.nextpos=random.randint(0,3)
                if self.nextpos != self.colpos:
                    self.changestrip=1
                    #print("Cur Col: ", self.colpos, "Next: ",self.nextpos)
            if random.randint(0,10)==5:
                self.sweep_pos = (self.sweep_pos +1) % (self.max_led-1)
            row_arr=full((self.max_led,4),0)
            brt=((self.sweep_pos % 30)*8)
            curbg=240-((240*self.changestrip)>>8)
            if self.changestrip > 0:
                newbg=(240*self.changestrip)>>8
                row_arr[int(((self.sweep_pos/30)-3)*30 % self.max_led)][self.nextpos]=newbg
                row_arr[int(((self.sweep_pos/30)-2)*30 % self.max_led)][self.nextpos]=newbg
                row_arr[int(((self.sweep_pos/30)-1)*30 % self.max_led)][self.nextpos]=(brt*self.changestrip)>>8
                row_arr[int(self.sweep_pos/30)*30][self.colpos]=0
                row_arr[int(((self.sweep_pos/30)+1)*30 % self.max_led)][self.nextpos]=newbg-((brt*self.changestrip)>>8)
                row_arr[int(((self.sweep_pos/30)+2)*30 % self.max_led)][self.nextpos]=newbg
                row_arr[int(((self.sweep_pos/30)+3)*30 % self.max_led)][self.nextpos]=newbg
                #print("str",self.changestrip,"btr",brt,"nbg",newbg,"nlo",(brt*self.changestrip)>>8,"nhi",newbg-((brt*self.changestrip)>>8),"cbg",curbg,"clo",brt-((brt*self.changestrip)>>8),"chi",curbg-(brt-((brt*self.changestrip)>>8)))

                if self.changestrip < 256:
                    self.changestrip += 1
                else:
                    self.changestrip = 0
                    curbg=240-((240*self.changestrip)>>8)
                    self.colpos = self.nextpos
            row_arr[int(((self.sweep_pos/30)-3)*30 % self.max_led)][self.colpos]=curbg
            row_arr[int(((self.sweep_pos/30)-2)*30 % self.max_led)][self.colpos]=curbg
            row_arr[int(((self.sweep_pos/30)-1)*30 % self.max_led)][self.colpos]=brt-((brt*self.changestrip)>>8)
            row_arr[int(self.sweep_pos/30)*30][self.colpos]=0
            row_arr[int(((self.sweep_pos/30)+1)*30 % self.max_led)][self.colpos]=curbg-(brt-((brt*self.changestrip)>>8))
            row_arr[int(((self.sweep_pos/30)+2)*30 % self.max_led)][self.colpos]=curbg
            row_arr[int(((self.sweep_pos/30)+3)*30 % self.max_led)][self.colpos]=curbg
            return row_arr
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)

