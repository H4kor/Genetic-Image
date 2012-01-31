'''
Created on 26.01.2012

@author: h4kor
'''
from time import time
import Image, ImageChops, ImageDraw
import math, random, threading

class Gen:
    
    def __init__(self,coordinates,color,size):
        self._size = size
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
       if(random.randint(1,2) == 1):
           self._color = (random.randint(0,255),
                                  random.randint(0,255),
                                  random.randint(0,255))
       else:
           r = random.randint(0,100)
           if r < 10:
               inc = 1
           elif r > 95 and len(self._coordinates) > 2:
               inc = -1
           else:
               inc = 0
           coord = []
           for i in range(0,len(self._coordinates)+inc):
              coord.append((random.randint(0,self._size[0]),random.randint(0,self._size[1])))
              
           self._coordinates = coord
    def copy(self):
        n = PolyGen(self._coordinates[:],self._color[:],self._size)
        return n     
            

class GeneticImage:

    def __init__(self,src):
        self._gens = []
        self.similarity = 0
        self._recalc = 1
        self.reference_img = src
        self.img = Image.new(src.mode, src.size, (255,255,255))
        g = PolyGen([(random.randint(0,self.img.size[0]),random.randint(0,self.img.size[1])),
                         (random.randint(0,self.img.size[0]),random.randint(0,self.img.size[1]))],
                         (random.randint(0,255), random.randint(0,255),random.randint(0,255)),src.size)
        self.addGen(g)
        g = PolyGen([(random.randint(0,self.img.size[0]),random.randint(0,self.img.size[1])),
                         (random.randint(0,self.img.size[0]),random.randint(0,self.img.size[1]))],
                         (random.randint(0,255), random.randint(0,255),random.randint(0,255)),src.size)
        self.addGen(g)
    def addGen(self,gen):
        self._gens.append(gen)
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
        for gen in self._gens:
            gen.draw(self.img)
        self._recalc = 1
    def mutate(self):
        impact = 0.2
        chance = 5
        if random.randint < 50:
            g = PolyGen([(random.randint(0,self.img.size[0]),random.randint(0,self.img.size[1])),
                         (random.randint(0,self.img.size[0]),random.randint(0,self.img.size[1]))],
                         (random.randint(0,255), random.randint(0,255),random.randint(0,255)),src.size)
            self.addGen(g)
        for gen in self._gens:
            if(random.randint(0,100) < chance):
                gen.mutate(impact)
        self.redraw()
    def pair(self, partner):
        x = random.sample(self._gens,len(self._gens)/2)
        y = random.sample(partner._gens,len(partner._gens)/2)
        child = GeneticImage(self.reference_img)
        for part in x:
            child.addGen(part.copy())
        for part in y:
            child.addGen(part.copy())



        
def evolve(population, steps):
    for i in range(0,steps):
        #print best Image value
        if i % 10 == 0:
            print i,": ",population[0].similarity
        
        #mutate and recalculate value
        for i in population:
            i.mutate()
            i.recalc()

        #sort the population with best on top
        population = sorted(population, key=lambda gen: gen.similarity)

        #create next generation
        for i in range(0,len(population)/4):
            population[i+len(population)/4] = population[i].pair(population[i+1])
            population[i+2*len(population)/4] = population[i].pair(population[i+1])
            population[i+3*len(population)/4] = population[i].pair(population[i+1])

    population = sorted(population, key=lambda gen: gen.similarity)
       
    return population
    
