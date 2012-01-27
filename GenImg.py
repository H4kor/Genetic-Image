'''
Created on 26.01.2012

@author: h4kor
'''
import Image, ImageChops, ImageDraw
import math, random, threading


class PolyGen(object):
    
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

class GenThread (threading.Thread):
    def __init__(self,g):
        self.gs = g
        threading.Thread.__init__(self)
    def run(self):
        for g in self.gs:
            g.mutate()
            g.calc_val()
    def setGen(self,g):
        self.g = g
        
def evolve(population, steps):
    t = [0,0,0,0]
    for i in range(0,steps):
        print i,": ",population[0].val
        
        '''
        stepsize = len(population)/4
        for i in range(0,4):
            t[i] = GenThread(population[stepsize*i:stepsize*(i+1)])
            t[i].start()
            
        for tt in t:
            tt.join()
        '''
        for i in range(0,len(population)):
            population[i].mutate()
            if population[i].recalc == 1:
                population[i].calc_val()
        
        population = sorted(population, key=lambda gen: gen.val)

        for i in range(0,len(population)/4):
            population[i+len(population)/4] = population[i].pair(population[i+1])
            population[i+2*len(population)/4] = population[i].pair(population[i+1])
            population[i+3*len(population)/4] = population[i].pair(population[i+1])
            
    population = sorted(population, key=lambda gen: gen.val)
    population[0].img.save("finish.png")   
    return population
    
