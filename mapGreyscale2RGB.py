#!/usr/local/bin/python3

import sys
from PIL import Image
import numpy as np

if len(sys.argv) != 2:
	print("Usage : mapGreyscale2RGB.py inputimage")
	sys.exit(1)

filename = sys.argv[1]
outfilename = f"out-{filename}.png"

im = Image.open(filename)

if im.mode[0]!="L" and im.mode[0]!="I" and im.mode[0]!="F":
    print(f"Input error, supporting only Greyscale input files. Current mode:{im.mode}")
    sys.exit(1)


data = np.array(im)
w, h = im.size

imout = Image.new('RGB', (w, h))

srcmax = 0
srcmin = (2<<32)-1

for x in range(w):
    for y in range(h):
        cleansrc = im.getpixel((x,y))

        if cleansrc > srcmax:
            srcmax = cleansrc

        if cleansrc < srcmin:
            srcmin = cleansrc

print(f"Input min:{srcmin} max:{srcmax}")
srcsize = 1<<16
if srcmax > srcsize:
    srcsize = 1<<32
destsize = 1<<24

print(f"Converter using max data size src:{srcsize} and dst:{destsize}")

for x in range(w):
    for y in range(h):
        cleansrc = im.getpixel((x,y))
        
        #Convert to full usage of 24bit ( RGB ) 
        src = int(cleansrc * destsize / srcsize)

        dst = ((src>>16)&255, (src>>8)&255, src&255)

        # #Convert back for validation
        # resrc = (dst[0]<<16)|(dst[1]<<8)|dst[2]
        # resrc = int(resrc * srcsize / destsize)
        # print(cleansrc, src, dst, resrc)
        imout.putpixel((x,y),dst) 

imout.save(outfilename)
