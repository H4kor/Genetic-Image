'''
Created on 26.01.2012

@author: h4kor
'''
import Image, ImageChops, ImageDraw
import math, random


class PolyGen(object):
    
    def __init__(self, src):
        self.polygons = []
        self.colors = []
        self.img = Image.new(src.mode, src.size, (255,255,255))
        self.val = 0
        self.src = src
    def calc_val(self):
        diff = ImageChops.difference(self.img, self.src)
        h = diff.histogram()
        sq = (value*(idx**2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        self.val = math.sqrt(sum_of_squares/float(self.img.size[0] * self.img.size[1]))
        
    def add_polygon(self,polygon,color):
        self.polygons.append(polygon)
        self.colors.append(color)
        draw = ImageDraw.Draw(self.img)
        draw.polygon(polygon, color, color)
    
    def redraw(self):
        self.img = Image.new(self.src.mode, self.src.size, (255,255,255))
        draw = ImageDraw.Draw(self.img)
        for i in range(0,len(self.polygons)):
            draw.polygon(self.polygons[i], self.colors[i], self.colors[i])
        
    def mutate(self):
        if random.randint(0,100) < 20:
            if random.randint(0,100) < 50:
                self.polygons[random.randint(0,19)] = [random.randint(0,70),random.randint(0,70),
                                                       random.randint(0,70),random.randint(0,70),
                                                       random.randint(0,70),random.randint(0,70)]
            else:
                self.colors[random.randint(0,19)] = (random.randint(0,255),
                                                       random.randint(0,255),
                                                       random.randint(0,255))
            self.redraw()
                
    def pair(self, partner):
        child = PolyGen(self.src)
        for i in range(0,len(self.polygons)):
            if i % 2 == 0:
                child.add_polygon(self.polygons[i],self.colors[i])
            else:
                child.add_polygon(partner.polygons[i],partner.colors[i])
        return child

def evolve(population, steps):
    for i in range(0,steps):
        print i,": ",population[0].val
        for i in range(0,len(population)):
            population[i].mutate()
            population[i].calc_val()
        population = sorted(population, key=lambda gen: gen.val)
        for i in range(0,10):
            population[i+10] = population[i].pair(population[i+1])
    population = sorted(population, key=lambda gen: gen.val)
    population[0].img.save("finish.png")   
    return population
    
