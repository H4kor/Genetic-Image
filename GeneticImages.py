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

amount_img = 80    #How many genetic images
amount_poly = 25    #How many polygons per image


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
inp = int(raw_input("Steps :"))
while input != 0:
    gens = GenImg.evolve(gens, inp)
    inp = int(raw_input("Steps :"))
 

