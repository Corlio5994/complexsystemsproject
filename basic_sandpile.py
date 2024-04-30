import random as rand
import os
from multiprocessing import Process
import matplotlib.pyplot as plt
import time
import math
import pickle
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages

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

def sandpile_process(sandpile: list[list[int]], visual:bool = True, iterations:int = 1000):
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
    snapshots = math.ceil((len(sandpile)*len(sandpile[0])*iterations)/10**7)
    step = 0
    counter = 0 
    cmap = plt.cm.viridis
    norm = plt.Normalize(vmin = 0, vmax = 4)
    #TODO: Rename snaps
    snaps = []
    while step < iterations: 
        sandpile = sandpile_step(sandpile)
        counter+=1
        # take pictures of the sandpile every f steps,
        # where f is chosen so that the number of snapshots
        # taken has storage size <= ~20mb
        if counter == snapshots:
            print(f'Up to step {step}.')
        if counter == snapshots and visual== True:
            snaps.append(pickle.dumps(cmap(norm(sandpile))))
            counter = 0
        step += 1
    if visual == True: 
        print('Unpickling snapshots...')
        time = datetime.now().strftime("%H-%M-%S")
        fname = 'RecordedSimSnapshots_' + time
        f = PdfPages(fname)
        for i in range(len(snaps)): 
            pic = pickle.loads(snaps[i])
            plt.imsave(f, pic, format='pdf')
        f.close()
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

g = generate_sandpile((8,9))
sandpile_process(g, iterations = 10000)
