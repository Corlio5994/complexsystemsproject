import random as rand
import os
from multiprocessing import Process
import matplotlib.pyplot as plt
import time
import pickle

rand.seed()

def generate_sandpile(t: tuple):
    '''
    Function for generating a sandpile. Initialises 2D-array with
    t[0] rows and t[1] columns, with 1's representing grains of sand.
    :input: A tuple t = (number of rows, number of columns) specifying
            size of sandpile simulation. 
    :output: A 2D-array of binary digits, with 1 representing a grain
            of sand and 0 representing an empty space.
    :complexity: O(random.choices)
    '''
    initial = []
    for _ in range(t[0]):
        initial.append(rand.choices([0,1], k=t[1]))
    return initial 

def sandpile_step(sandpile: list[list[int]]):
    '''
    Updates sandpile according to rules.
    '''
    k0 = rand.randint(0, len(sandpile)-1)
    k1 = rand.randint(0, len(sandpile[0])-1)
    sandpile[k0][k1] += 1
    for i in range(len(sandpile)):
        for j in range(len(sandpile)):
            if sandpile[i][j] >= 4:
                sandpile[i][j] -= 4
                if i + 1 < len(sandpile): 
                    sandpile[i+1][j] = sandpile[i+1][j] + 1
                if i-1 > -1: 
                    sandpile[i-1][j] = sandpile[i-1][j] + 1
                if j + 1 < len(sandpile[0]):
                    sandpile[i][j+1] = sandpile[i][j+1] + 1
                if j - 1 > -1:
                    sandpile[i][j-1] = sandpile[i][j-1] + 1
    return sandpile

def sandpile_process(sandpile: list[list[int]], iterations:int = 1000):
    '''
    I don't think this will fit in a single function, but I want
    to display sandpile evolution on a grid that continuously updates. 
    I think for base functionality we need to be able to specify a 
    number of iterations, to record evolution (maybe save snapshots
    every x steps), and a way to manually interrupt early to avoid 
    infinite loops. Obviously more robust error handling would be nice,
    but we'll see how complicated it all gets. We should use 
    different colours for different sandpile heights so that it's 
    ~pretty~, maybe some colour presets would be nice also. Don't 
    get too bogged down in cosmetics though. 
    '''
    snapshots = ceil((sandpile*sandpile[0]*iterations)/10**7)
    step = 0
    counter = 0 
    while step < iterations: 
        sandpile = sandpile_step(sandpile)
        counter+=1
        # take pictures of the sandpile every f steps,
        # where f is chosen so that the number of snapshots
        # taken has storage size <= ~20mb
        if counter == snapshots:
            plt.imshow(sandpile)
            plt.legend()
            plt.show()
            counter = 0
        step += 1
    return sandpile



#if __name__ == '__main__':
#    process = Process(target=visualise_sandpile)
#    process.start()
#    while process.is_alive():
#        if keyboard.is_pressed('q'):
#            process.terminate()
#            break

#class Sandpile: 
#    '''
#    My instincts say we should wrap this all in an object. 
#    '''
#    def __init__(self, dimensions, palette):

g = generate_sandpile((3,3))
sandpile_process(g, iterations=20)
