import random as rand
import os
from multiprocessing import Process
import matplotlib.pyplot as plt
import time
import math
import pickle
import numpy as np
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

rand.seed()


#IDEA : Larger grid for sandpile size. Changes to gen are : take in grid dimensions, as well as site dimensions. To further generalise, we can allow multiple sites. This is simple - supply a matrix of site
# sizes. Either generate random locations or manually input

#Note: It is allowed for users to input overlap. This will just mean that the intersection of sites gets rewritten, which might be inefficient but should be ok since the work done should be that of the average case. 



def generate_sandpile(grid: tuple, sites, locations=False):
    '''
    Function for generating a sandpile. Initialises 2D-array with
    t[0] rows and t[1] columns, with 1's representing grains of sand.
    The user specifies the sizes and optionally the locations of 
    regions with grains of sand.
    Examples: 
        generate_sandpile((x,y), [(x,y)]) will cover the whole array with sand grains. 
        generate_sandpile((x,x), [(x-2a,x-2a), (a-1, a-1)]) will create a square with side length x-2a at the centre of the grid.
    :input: A tuple t = (number of rows, number of columns) specifying
            size of sandpile simulation. 
    :output: A 2D-array of binary digits, with 1 representing a grain
            of sand and 0 representing an empty space.
    '''   
    table = np.zeros(grid)
    size_sum = 0 
    if locations == False:
        for s in sites: 
            size_sum += s[0]*s[1]
    else: 
        for s in sites: 
            size_sum += s[0][0]*s[0][1]

    if size_sum > grid[0]*grid[1]:
        raise ValueError(f"Total site dimensions are {size_sum}, input smaller sites.")
    #Format of each s: [(length, width), (location_x, location_y)] if locations = True, (length,width) otherwise 
    if locations == True:
        for s in sites: 
            for i in range(s[1][0], min(s[1][0]+s[0][0]-1, len(table))):
                for j in range(s[1][1], min(s[1][1]+s[0][1]-1, len(table[0]))):
                        table[i][j] = rand.choice([0,1])
    else:
        head = [0,0] 
        for s in sites: 
            for i in range(head[0], min(head[0]+s[0]-1, len(table))):
                for j in range(head[1], min(head[1]+s[1]-1, len(table[0]))):
                        table[i][j] = rand.choice([0,1])
            head = [head[0]+s[0]-1, head[1]+s[1]-1]
            if head[0] > len(table):
                head[0] = 0
            if head[1] > len(table[1]):
                head[1] = 0       
    return table

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
    def avg_height(sandpile: list[list[int]]) -> float:
        h = 0 
        for i in range(len(sandpile)): 
            for j in range(len(sandpile[i])):
                h += sandpile[i][j]
        return h/(len(sandpile)*len(sandpile[0]))
    def loss():
        pass
    def area():
        pass 
    def topples():
        pass
    def length(): 
        pass 
    snapshots = math.ceil((len(sandpile)*len(sandpile[0])*iterations)/10**7)
    step = 0
    counter = 0 
    cmap = plt.cm.viridis
    norm = plt.Normalize(vmin = 0, vmax = 4)
    #TODO: Rename snaps
    snaps = []
    with open(f'logstats-{datetime.now().strftime("%m-%d-%H")}.txt', 'a') as f:
        f.write(f'Simulation starting at {datetime.now().strftime("%m-%d-%H-%M")}. \n')
    while step < iterations: 
        #if counter == snapshots-1:
            #past = sandpile
        sandpile = sandpile_step(sandpile)
        counter+=1
        # take pictures and record statistics of the sandpile every f steps,
        # where f is chosen so that the number of snapshots
        # taken has storage size <= ~20mb
        if counter == snapshots:
            print(f'Up to step {step}.')
            with open(f'logstats-{datetime.now().strftime("%m-%d-%H")}.txt', 'a') as f:
                f.write(f'Average height at step {step} is: {avg_height(sandpile)} \n')
            if visual== True:
                snaps.append(pickle.dumps(cmap(norm(sandpile))))
                counter = 0
        step += 1
    with open(f'logstats-{datetime.now().strftime("%m-%d-%H")}.txt', 'a') as f:
        f.write('--------------------------------------\n')
    if visual == True: 
        print('Unpickling snapshots...')
        time = datetime.now().strftime("%m-%d-%H-%M")
        fname = 'RecordedSimSnapshots_' + time + '.pdf'
        f = PdfPages(fname)
        for i in range(len(snaps)): 
            pic = pickle.loads(snaps[i])
            plt.imsave(f, pic, format='pdf')
        f.close()
    return sandpile

def render_sandpile(sandpile: list[list[int]]):

    # plot
    fig, ax = plt.subplots()
    ax.set_axis_off()
    im = ax.imshow(sandpile)

    # create legend
    values = np.unique(sandpile.ravel())
    colours = [im.cmap(im.norm(x)) for x in values]
    cutouts = [patches.Patch(color=colours[i], label=f'{i}') for i in range(len(colours))]
    plt.legend(handles=cutouts, bbox_to_anchor=(1.05,1), loc=2, title='Pile height', alignment='left', edgecolor='black')

    plt.show()
    return None



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

g = generate_sandpile((90,90), [[(50,50), (19,19)]], locations=True)
render_sandpile(g)
#sandpile_process(g, visual=True, iterations=40000)
