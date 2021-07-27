
import operator
import random

import numpy
import math

from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

import cost

Nitem = 50

Min= [280.9]*Nitem+[-16.3]*Nitem
Max= [319.1]*Nitem+[ 20.1]*Nitem



creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Particle", list, fitness=creator.FitnessMax, speed=list, 
    smin=None, smax=None, best=None, elements=list)

def generate(size, pmin, pmax, smin, smax):
    part = creator.Particle(random.uniform(pmin[i], pmax[i]) for i in range(2*size)) 
    part.speed = [random.uniform(smin, smax) for _ in range(2*size)]
    part.smin = smin
    part.smax = smax
    return part



def updateParticle(part, best, phi1, phi2):
    #Genera dos vectores aleatorios con la misma longitud que la particula
    
    u1 = list(random.uniform(0, phi1) for _ in range(len(part)))
    u2 = list(random.uniform(0, phi2) for _ in range(len(part)))
    
    
    #v_u1=u1*(part.best-part)  part.best mejor valor de la particula
    v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
    #v_u2=u2*(part.best-part)  part.best mejor valor a nivel global
    v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
    #v(t)= v_u1+v_u2+ v(t-1)
    part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
    
    
    for i, speed in enumerate(part.speed):
        
        if abs(speed) < part.smin:
            part.speed[i] = math.copysign(part.smin, speed)
            #copia psrt.smin cambiando su signo original por el de speed
        elif abs(speed) > part.smax:
            part.speed[i] = math.copysign(part.smax, speed)
        
    #Actualizar particula
    part[:] = list(map(operator.add, part, part.speed))

toolbox = base.Toolbox()
toolbox.register("particle", generate, size=Nitem, pmin=Max, pmax=Min, smin=-1, smax=1)
toolbox.register("population", tools.initRepeat, list, toolbox.particle)
toolbox.register("update", updateParticle, phi1=2, phi2=2)
toolbox.register("evaluate", cost.Fitness)




import matplotlib.pyplot as plt

#Problema de maximizacion enfoque global.
def main(Pops, sizes):
    pop = toolbox.population(n=Pops)
    GEN = 500
    best = None
    Pop=[]
    S=0
    for g in range(GEN):
        print(g)
        for part in pop:
            apt, lis= cost.Fitness(part, sizes, Nitem)
            part.fitness.values =(apt,)
            part.elements= lis
            
            if not part.best or part.best.fitness < part.fitness:
                part.best = creator.Particle(part)
                part.best.fitness.values = part.fitness.values
                part.best.elements = part.elements
                #Si la particula no tiene un mejor valor encontrado o si el mejor valor encontrado  es menor al  actual, entonces este es actualizado.
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values
                best.elements = part.elements
            #Si no hay ningun vector mejor o hay un vector que tiene mejores valores que el que se considera ser mejor, entonces se actualiza.
        #print(best.fitness.values, best.elements)
        for part in pop:
            toolbox.update(part, best)
            
        xx,yy=cost.Fitness(best, sizes, Nitem)
        print(g, xx, len(yy))
        if S!= xx:
            S=xx
            Pop.append((best.elements, best, g))
            fig, ax = plt.subplots()
            cost.Paint(ax)
            print("="*20)
            cost.Paint_Q( best.elements, best, sizes, Nitem,ax)
            xx,yy=cost.Fitness(best, sizes, Nitem)
            print(g, xx, len(yy))
            plt.title("Generation: "+ str(g+1) +   "    Area: "+ str(xx), size= 20)
            plt.xticks([])
            plt.yticks([])
            plt.show()
   
    return pop, best

if __name__ == "__main__":
    random.seed(0)
    PopS = 100
    sizes = [[random.randrange(1, 6),random.randrange(1,6)] for _ in range(Nitem)]

    main(PopS, sizes)

