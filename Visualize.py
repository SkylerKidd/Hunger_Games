import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
from hg_settings import *
LAVA_COLOR    = '#FF6600'
GRASS_COLOR   = '#A5D414'
BERRY_COLOR   = '#7722FF'
KATS_KOLOR    = '#552222'
WALL_COLOR    = '#898989'
HUNGER_COLOR = col.ListedColormap([GRASS_COLOR, LAVA_COLOR, BERRY_COLOR, KATS_KOLOR, WALL_COLOR])

class Visualizer():
    """Visualize the simulation.

    Attributes
    ----------
    grid : 2D numpy array
        The environment that Kat agent lives in.
    """
    def __init__(self, grid):
        self.fig = plt.figure(figsize=(12,6))
        self.ax = self.fig.add_axes((-.25,0,1,1))
        self.info = self.fig.add_axes((0,0,1,1))
        self.img = self.ax.imshow(grid.get_grid(), cmap= HUNGER_COLOR, interpolation='none')
        self.ax.axis('off')
        self.info.axis('off')

    def show(self, grid, kats, gen):
        self.img.set_data(grid)
        genNum = str("Generation " + str(gen))
        generation = self.info.text(.5,.95,genNum, fontsize = 18 )
        ins = ""
        if (type(kats)==list):
            for i in range(5):
               ins += str("PREVIOUS " +str(i) + " INSTRUCTION SET: " + kats[i].print_ins_1() + "\n")
        else:
            ins += str("PREVIOUS INSTRUCTION SET: " + kats.print_ins_1())
        ins_set = self.info.text(.5,.8,ins,  verticalalignment='top',
                    horizontalalignment='left', fontsize = 16)
        plt.draw()
        plt.pause(.01)
        generation.remove()
        ins_set.remove()

    def graph(self, array):
        #plt.figure(figsize=(6,6))
        #plt.axes([.1,.1,1,.8])
        #high_kat = np.amax(array[:])
        #high_kat += (high_kat *.1)
        plt.figure()
        for i in range(SEPERATE_MODELS): 
            plt.plot(array[i])
        #plt.plot(array[0])
        plt.title('Fitness over Generations')
        plt.xlabel('Number of generations')
        plt.ylabel('Fitness')
        #plt.ylim(0, high_kat)
        plt.show()
