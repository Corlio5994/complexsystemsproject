import random as rand 

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

def sandpile_step():
    '''
    Updates sandpile according to rules.
    '''
    pass 

def visualise_sandpile():
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

class Sandpile: 
    '''
    My instincts say we should wrap this all in an object. 
    '''
    pass

print(generate_sandpile((8,9)))