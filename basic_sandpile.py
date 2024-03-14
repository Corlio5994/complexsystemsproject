import random as rand
import os
from multiprocessing import Process
import keyboard
import time

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
    initial = rand.choices([0,1], k=t[0]*t[1])
    return initial 

def sandpile_step(sandpile: list[list[int]]):
    '''
    Updates sandpile according to rules.
    '''
    k0 = rand.randint(0, len(sandpile))
    k1 = rand.randint(0, len(sandpile[0])
    sandpile[k0][k1] += 1
    for i in range(len(sandpile)):
        for j in range(len(sandpile)):
            if sandpile[i][j] >= 4:
                sandpile[i][j] -= 4
                if i + 1 < len(lst): 
                    sandpile[i+1][j] = sandpile[i+1][j] + 1
                if i-1 > -1: 
                    sandpile[i-1][j] = sandpile[i-1][j] + 1
                if j + 1 < len(lst[0]):
                    sandpile[i][j+1] = sandpile[i][j+1] + 1
                if j - 1 > -1:
                    sandpile[i][j-1] = sandpile[i][j-1] + 1
    return sandpile

def sandpile_process(iterations:int = 1000):
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
    pass



if __name__ == '__main__':
    process = Process(target=visualise_sandpile)
    process.start()
    while process.is_alive():
        if keyboard.is_pressed('q'):
            process.terminate()
            break

class Sandpile: 
    '''
    My instincts say we should wrap this all in an object. 
    '''
    def __init__(self, dimensions, palette):

print(generate_sandpile((8,9)))
