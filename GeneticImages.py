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

debug = 1

amount_imgs = 300
amount_gens = 20
img_name = "simple.png"

if debug == 0:
    amount_imgs = int(raw_input("Population size: "))    #How many genetic images
    amount_gens = int(raw_input("Polygons: "))    #How many polygons per image
    img_name = raw_input("File name: ")

#getting image
src = Image.open(img_name)

width, height = src.size 

gens = []

for i in range(0,amount_imgs):
    gens.append(GenImg.GeneticImage(src))
    gens[i].recalc()
'''for i in range(0,amount_imgs): 
    for k in range(0,amount_gens):
        g = GenImg.PolyGen([(random.randint(0,width),random.randint(0,height)),
                            (random.randint(0,width),random.randint(0,height)),
                            #(random.randint(0,width),random.randint(0,height)),
                            #(random.randint(0,width),random.randint(0,height)),
                            #(random.randint(0,width),random.randint(0,height))
                            ],
                            (random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255),random.randint(0,255)),src.size)
        gens[i].addGen(g)
    
'''
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
    steps = int(raw_input("Steps :"))

