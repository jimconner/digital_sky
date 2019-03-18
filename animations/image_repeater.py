# Image Repeater
# Fetches an image from the given URL, resizes it to num_pixels width
# and then emits it one row at a time from top to bottom over and over again.

import sys,time, urllib, traceback, random

from PIL import Image
from numpy import array,dstack,full

class image_repeater():
    def __init__(self, width, img_url):
        urllib.urlretrieve(img_url, "file.jpg")
        img = Image.open("file.jpg")
        self.img = img.resize((width,img.size[0]), Image.ANTIALIAS) # Resize width to match number of pixels.
        img_tmp = array(self.img)
        b_tmp=full((img_tmp.shape[0],img_tmp.shape[1],1),0) # An extra 2D array of single bytes to store 6812B WW pixel data
        self.arr=dstack((img_tmp,b_tmp)) # Stack the extra bytes onto the 24bpp array to get 32bpp
        self.row = 0
	self.cycle = 4
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
