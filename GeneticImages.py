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

debug = 0

amount_imgs = 50
amount_gens = 20
img_name = "python.png"

if debug == 0:
    amount_imgs = int(raw_input("Population size: "))    #How many genetic images
    amount_gens = int(raw_input("Polygons: "))    #How many polygons per image
    img_name = raw_input("File name: ")

GenImg.init_Evolution(amount_imgs,amount_gens,img_name)

gens = []

for i in range(0,amount_imgs):
    gens.append(GenImg.GeneticImage())
    gens[i].recalc()

total = 0
steps = 100
iterations_pro_step = 50
if debug == 0:
    steps = int(raw_input("Steps :"))
    iterations_pro_step = int(raw_input("Iterations pro step : "))
while steps != 0:
    for k in range(0,steps):
        for i in range(0,iterations_pro_step):
            total = total + iterations_pro_step
            gens = GenImg.evolve(gens, iterations_pro_step)
            gens[0].img.save("%05d.png" % total) 
            print "%d: %f" %(total, gens[0].similarity)
    steps = int(raw_input("Steps :"))

