# Twinkle
# Same as image_repeater, but using only the W pixels and ignoring RGB
# Hopefully this will be good for twhinkling stars.

import sys,time, urllib.request, urllib.parse, urllib.error, traceback, random

from PIL import Image
from numpy import array,dstack,full
from pathlib import Path

# Requires an image_url and a 0-3 value to select R,G,B or W respectively.
class animation():
    def __init__(self, datastore, img_name, strip):
        img_file=sys.path[0]+'/image_cache/'+img_name+'.jpg'
        if not Path(img_file).is_file():
            img_url=datastore.IMAGES[img_name]
            urllib.request.urlretrieve(img_url, img_file)
        self.strip=int(strip)
        img = Image.open(img_file)
        self.img = img.resize((datastore.LED_COUNT,img.size[0]), Image.ANTIALIAS) # Resize width to match number of pixels.
        img_tmp = array(self.img)
        self.arr=full((img_tmp.shape[0],img_tmp.shape[1],4),0) # An extra 2D array of single bytes to store 6812B WW pixel data
        for row in range(len(img_tmp)):
            for pixel in range(len(img_tmp[row])):
                self.arr[row][pixel][self.strip]=min(img_tmp[row][pixel][0],img_tmp[row][pixel][1],img_tmp[row][pixel][2])
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
