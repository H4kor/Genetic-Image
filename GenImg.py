'''
Created on 26.01.2012

@author: h4kor
'''
from time import time
import Image, ImageChops, ImageDraw
import math, random, threading

amount_imgs = 50
amount_gens = 20
complexity_gens = 10
img_name = "python.png"


def init_Evolution(a_imgs,a_gens,img):
    global amount_imgs
    global amount_gens
    global src
    amount_imgs = a_imgs
    amount_gens = a_gens
    src = Image.open(img_name)

class Gen:
    def __init__(self,coordinates,color):
        self._color = color
        self._coordinates = coordinates
    def draw(self,img):
        pass
    def mutate(self,impact):
        pass

class PolyGen(Gen):
    def draw(self,img):
        draw = ImageDraw.Draw(img)
        draw.polygon(self._coordinates, self._color, self._color)
    def mutate(self,impact):
       global src
       if(random.randint(1,2) == 1):
           self._color = (random.randint(0,255),
                                  random.randint(0,255),
                                  random.randint(0,255))
       else:
           r = random.randint(0,100)
           if r < 1 and len(self._coordinates) <= complexity_gens:
               inc = 1
           elif r > 99 and len(self._coordinates) > 2:
               inc = -1
           else:
               inc = 0
           coord = []
           for i in range(0,len(self._coordinates)+inc):
              coord.append((random.randint(0,src.size[0]),random.randint(0,src.size[1])))
              
           self._coordinates = coord
    def copy(self):
        n = PolyGen(self._coordinates[:],self._color[:])
        return n     
            

class GeneticImage:
    def __init__(self):
        global src
        self.gens = []
        self.similarity = 0
        self._recalc = 1
        self.reference_img = src
        self.img = Image.new(src.mode, src.size, (255,255,255))
        g = PolyGen([(random.randint(0,self.img.size[0]),random.randint(0,self.img.size[1])),
                         (random.randint(0,self.img.size[0]),random.randint(0,self.img.size[1]))],
                         (random.randint(0,255), random.randint(0,255),random.randint(0,255)))
        self.addGen(g)
    def addGen(self,gen):
        self.gens.append(gen)
        gen.draw(self.img)
        self._recalc = 1
    def recalc(self):
        if self._recalc == 1:
            diff = ImageChops.difference(self.img, self.reference_img)
            h = diff.histogram()
            sq = (value*(idx**2) for idx, value in enumerate(h))
            sum_of_squares = sum(sq)
            self.similarity = math.sqrt(sum_of_squares/float(self.img.size[0] * self.img.size[1]))
            self._recalc = 0
    def redraw(self):
        self.img = Image.new(self.reference_img.mode, self.reference_img.size, (255,255,255))
        for gen in self.gens:
            gen.draw(self.img)
        self._recalc = 1
    def mutate(self):
        impact = 0.2
        chance = 5
        r = random.randint(0,100)
        if r < 1 and len(self.gens) <= amount_gens:
            g = PolyGen([(random.randint(0,self.img.size[0]),random.randint(0,self.img.size[1])),
                         (random.randint(0,self.img.size[0]),random.randint(0,self.img.size[1]))],
                         (random.randint(0,255), random.randint(0,255),random.randint(0,255)))
            self.addGen(g)
        elif r >99:
            self.gens.pop()
            
        for gen in self.gens:
            if(random.randint(0,100) < chance):
                gen.mutate(impact)
        self.redraw()
    def pair(self, partner):
        x = random.sample(self.gens,len(self.gens)/2)
        y = (random.sample(partner.gens,len(partner.gens)/2))
        child = GeneticImage()
        for part in x:
            child.addGen(part.copy())
        for part in y:
            child.addGen(part.copy())
        return child



        
def evolve(population, steps):
    for i in range(0,steps):
        #print best Image value
        #if i % 10 == 0:
        #    print i,": ",population[0].similarity
        
        #mutate and recalculate value
        for i in population:
            i.mutate()
            i.recalc()

        #sort the population with best on top
        population = sorted(population, key=lambda gen: gen.similarity)

        population[0].pair(population[1])

        #create next generation
        for i in range(0,len(population)/4):
            population[i+len(population)/4] = population[i].pair(population[i+1])
            population[i+2*len(population)/4] = population[i].pair(population[i+1])
            population[i+3*len(population)/4] = population[i].pair(population[i+1])
        for i in range(1,len(population)/4):
            population[i] = population[i+len(population)/4].pair(population[i+1+len(population)/4])


    for i in population:
        i.recalc()
    population = sorted(population, key=lambda gen: gen.similarity)
       
    return population
    
