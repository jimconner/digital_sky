# Twinkle
# Same as image_repeater, but using only the W pixels and ignoring RGB
# Hopefully this will be good for twhinkling stars.

import sys,time, urllib.request, urllib.parse, urllib.error, traceback, random

from PIL import Image
from numpy import array,dstack,full

class animation():
    def __init__(self, datastore, img_url):
        urllib.request.urlretrieve(img_url, "file.jpg")
        img = Image.open("file.jpg")
        self.img = img.resize((datastore.LED_COUNT,img.size[0]), Image.ANTIALIAS) # Resize width to match number of pixels.
        img_tmp = array(self.img)
        b_tmp=full((img_tmp.shape[0],img_tmp.shape[1],1),0) # An extra 2D array of single bytes to store 6812B WW pixel data
        self.arr=dstack((img_tmp,b_tmp)) # Stack the extra bytes onto the 24bpp array to get 32bpp
        for row in range(len(self.arr)):
            for pixel in range(len(self.arr[row])):
                self.arr[row][pixel][3]=min([self.arr[row][pixel][0],self.arr[row][pixel][1],self.arr[row][pixel][2]])
        self.row = 0
        self.cycle = 2 # self.cycle used as divisor to make image play more slowly.
        self.count = 0

    def emit_row(self):
        # print("Image Row: ", self.row)
        try:
            self.count = (self.count+1) %self.cycle
            if self.row ==len(self.arr)-1:
                self.row = 0
            else:
                if self.count == 0:
                	self.row += 1
            return self.arr[self.row]
        except Exception as err:
            print(err)
            traceback.print_exc(file=sys.stdout)
