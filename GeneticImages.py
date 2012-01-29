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

amount_imgs = int(raw_input("Population size: "))    #How many genetic images
amount_gens = int(raw_input("Polygons: "))    #How many polygons per image


#getting image
img_name = raw_input("File name: ")
src = Image.open(img_name)

width, height = src.size 

gens = []

for i in range(0,amount_imgs):
    gens.append(GenImg.GeneticImage(src))

for i in range(0,amount_imgs): 
    for k in range(0,amount_gens):
        g = GenImg.PolyGen([random.randint(0,width),random.randint(0,height),
                            random.randint(0,width),random.randint(0,height),
                            random.randint(0,width),random.randint(0,height)],
                            (random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255)),src.size)
        gens[i].addGen(g)
    gens[i].recalc()
total = 0
inp = int(raw_input("Steps :"))
while input != 0:
    total = total + inp
    gens = GenImg.evolve(gens, inp)
    gens[0].img.save("finish%d.png" % total) 
    inp = int(raw_input("Steps :"))

