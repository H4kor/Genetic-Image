'''
Created on 26.01.2012

@author: h4kor
'''
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
            self._coordinates = [random.randint(0,self._size[0]),random.randint(0,self._size[1]),
                                 random.randint(0,self._size[0]),random.randint(0,self._size[1]),
                                 random.randint(0,self._size[0]),random.randint(0,self._size[1])]
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
        for gen in self._gens:
            if(random.randint(0,100) < chance):
                gen.mutate(impact)
        self.redraw()
    def pair(self, partner):
        r = random.sample(range(0,len(self._gens)),len(self._gens)/2)
        child = GeneticImage(self.reference_img)
        for i in range(0,len(self._gens)):
            if i in r:
                child.addGen(self._gens[i].copy())
            else:
                child.addGen(partner._gens[i].copy())
        return child
'''
class PolyGen(Gen):
    
    def __init__(self, src):

        self.polygons = []
        self.colors = []
        self.img = Image.new(src.mode, src.size, (255,255,255))
        self.val = 0
        self.src = src
        self.recalc = 1
    def calc_val(self):
        diff = ImageChops.difference(self.img, self.src)
        h = diff.histogram()
        sq = (value*(idx**2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        self.val = math.sqrt(sum_of_squares/float(self.img.size[0] * self.img.size[1]))
        self.recalc = 0
    def add_polygon(self,polygon,color):
        self.polygons.append(polygon)
        self.colors.append(color)
        draw = ImageDraw.Draw(self.img)
        draw.polygon(polygon, color, color)
        self.recalc = 1
    def redraw(self):
        self.img = Image.new(self.src.mode, self.src.size, (255,255,255))
        draw = ImageDraw.Draw(self.img)
        for i in range(0,len(self.polygons)):
            draw.polygon(self.polygons[i], self.colors[i], self.colors[i])
        self.recalc = 1
    def mutate(self):
        if random.randint(0,100) < 20:
            if random.randint(0,100) < 50:
                self.polygons[random.randint(0,len(self.polygons)-1)] = [random.randint(0,self.src.size[0]),random.randint(0,self.src.size[1]),
                                                       random.randint(0,self.src.size[0]),random.randint(0,self.src.size[1]),
                                                       random.randint(0,self.src.size[0]),random.randint(0,self.src.size[1])]
            else:
                self.colors[random.randint(0,len(self.colors)-1)] = (random.randint(0,255),
                                                       random.randint(0,255),
                                                       random.randint(0,255))
            self.redraw()
            self.recalc = 1

    def pair(self, partner):
        self.r = random.sample(range(0,len(self.polygons)),len(self.polygons)/2)
        child = PolyGen(self.src)
        for i in range(0,len(self.polygons)):
            if i in self.r:
                child.add_polygon(self.polygons[i],self.colors[i])
            else:
                child.add_polygon(partner.polygons[i],partner.colors[i])
        return child
    
    def copy(self):
        ret = PolyGen(self.src);
        ret.polygons = self.polygons[:]
        ret.colors = self.colors[:]
        ret.redraw()
        return ret
'''

        
def evolve(population, steps):
    for i in range(0,steps):
        #print best Image value
        if i % 10 == 0:
            print i,": ",population[0].similarity
        
        #mutate and recalculate value
        for i in range(0,len(population)):
            population[i].mutate()
            population[i].recalc()
                    
        #sort the population with best on top
        population = sorted(population, key=lambda gen: gen.similarity)

        #create next generation
        for i in range(0,len(population)/4):
            population[i+len(population)/4] = population[i].pair(population[i+1])
            population[i+2*len(population)/4] = population[i].pair(population[i+1])
            population[i+3*len(population)/4] = population[i].pair(population[i+1])
            
    population = sorted(population, key=lambda gen: gen.similarity)
       
    return population
    
