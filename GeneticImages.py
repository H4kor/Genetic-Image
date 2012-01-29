#!/usr/bin/python
'''
Created on 26.01.2012

@author: h4kor
'''

if __name__ == '__main__':
    pass

import Image
import random
import GenImg

amount_img = 100    #How many genetic images
amount_poly = 50    #How many polygons per image


img_name = raw_input("File name: ")

src = Image.open(img_name)
width, height = src.size 

gens = []

for i in range(0,amount_img):
    gens.append(GenImg.PolyGen(src))

for i in range(0,amount_img): 
    for k in range(0,amount_poly):
        gens[i].add_polygon([random.randint(0,width),random.randint(0,height),
                             random.randint(0,width),random.randint(0,height),
                             random.randint(0,width),random.randint(0,height)],
                             (random.randint(0,255),
                              random.randint(0,255),
                              random.randint(0,255)))
    gens[i].calc_val()
total = 0
inp = int(raw_input("Steps :"))
while input != 0:
    total = total + inp
    gens = GenImg.evolve(gens, inp)
    gens[0].img.save("finish%d.png" % total) 
    inp = int(raw_input("Steps :"))

