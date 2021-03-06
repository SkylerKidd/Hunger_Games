import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
import os 
from hg_settings import *

LAVA_COLOR    = '#FF6600'
GRASS_COLOR   = '#A5D414'
BERRY_COLOR   = '#7722FF'
KATS_KOLOR    = '#552222'
WALL_COLOR    = '#898989'
HUNGER_COLOR = col.ListedColormap([GRASS_COLOR, LAVA_COLOR, BERRY_COLOR, \
                                KATS_KOLOR, WALL_COLOR])

class Visualizer(object):
    """Visualize the simulation.

    Attributes
    ----------
    grid : 2D numpy array
        The environment that Kat agent lives in.
    """
    def __init__(self, grid):
        self.fig = plt.figure(1, figsize=(12,6))
        self.ax = self.fig.add_axes((-.25,0,1,1))
        self.info = self.fig.add_axes((0,0,1,1))
        self.img = self.ax.imshow(grid.get_grid(), cmap= HUNGER_COLOR,\
                    interpolation='none')
        self.ax.axis('off')
        self.info.axis('off')

    def show(self, grid, kats, gen, specie, t_name):
        """
        Show the current Kat and the current grid
        
        Attributes
        ----------
        grid: a 2d array of the 'map' the Kat has spawned on, colored using a
                cmap to represent walls, kats, lava, grass, and berries
        kats: array containing the winning kats
        gen: the current Kat generation.
        specie: Current specie gen is in
        t_name: Test Name if running mulitple tests in a row
        """
        self.img.set_data(grid[0])
        genNum = str("Specie " + str(specie) +" | Generation " + str(gen) +\
                " | Kat " + str(grid[2]+1) + " | Step " + str(grid[3]+1) + \
                "\n" + t_name)
        generation = self.info.text(.5,.90,genNum, fontsize = 18 )
        ins = str("CURRENT INSTRUCTION SET: " + grid[1])
        ins_set = self.info.text(.5,.88,ins,  verticalalignment='top',
                    horizontalalignment='left', fontsize = 16)
        plt.draw()
        plt.pause(.01)
        generation.remove()
        ins_set.remove()

    def graph(self, array, p_array, t_name):
        """
        Plot the graph of the highest kat scores over generations and species
        
        Attributes
        ----------
        array : a numpy array containing all the 'Winning' Kat fitness scores
        p_array: a numpy array containing the lava and berry chances that
                hunger_grid used on map generation
        t_name: Test Name if running mulitple tests in a row
        """
        fig_title = t_name + " Fitness over time"
        plt.figure(fig_title, figsize=(14,6))
        plt.subplot(121)
        for i in range(NUM_OF_SPECIES): 
            legend = str("Specie " + str(i) + ": Lava = " + \
                str(p_array[i][0] * 100) +  "% | Berry = " + \
                str(p_array[i][1]*100) + "%, Max Fitness:" + \
                str(np.max(array[i])))
            plt.plot(array[i], label = legend)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        title = str('Fitness over ' + str(NUM_OF_SPECIES) + ' Species, and ' +\
                str(NUM_OF_GENERATIONS) + ' Generations\n' + t_name )
        plt.title(title)
        plt.xlabel('Number of generations')
        plt.ylabel('Fitness')
        plt.ylim(0, (np.max(array) + 10))
        saveFile = str(os.path.dirname(os.path.realpath(__file__)) +\
                '\\Graph_Output\\'  +  t_name + ' - Fitness over time.png')
        plt.savefig(saveFile)    
        
    def chance_vs_fitness(self, array, p_array, m_array, g_array,t_name):
        """
        Plot 2 bar graphs of avg and max fitness vs lava and berry chance
        
        Attributes
        ----------
        array : a numpy array containing all the 'Winning' Kat fitness scores
        p_array: a numpy array containing the lava and berry chances that
                hunger_grid used on map generation
        t_name: Test Name if running mulitple tests in a row
        m_array: array containing chance of certain mutations occuring
        g_array: array containing chance of generate behaviors occuring
        """
        fig_title = t_name + " Chance vs Fitness"
        plt.figure(fig_title) 
        plt.subplot(311)
        index = np.arange(NUM_OF_SPECIES)
        max_fitness = np.amax(array, axis = 1)
        avg_fitness = np.average(array, axis = 1)
        title = str('Avg and Max Fitness over ' + str(NUM_OF_SPECIES) + ' Species, and ' +\
                str(NUM_OF_GENERATIONS) + ' Generations\n' + t_name )        
        width = 0.35       # the width of the bars
        plt.bar(index, max_fitness, width, color='r', \
                    label = 'MAX Fitness')
        plt.bar(index + width, avg_fitness, width, color='y', \
                    label = 'AVG Fitness')
        plt.ylabel('Fitness Score')
        plt.title(title)
        if DISPLAY_LEGENDS:
            plt.legend()
        plt.subplot(312)
        lava_array = p_array[:,0]
        berry_array = p_array[:,1]
        plt.bar(index, lava_array, width, color = LAVA_COLOR, label='Lava Chance')
        plt.bar(index+width, berry_array, width, color = BERRY_COLOR, label='Berry Chance')
        if DISPLAY_LEGENDS:
            plt.legend()
        plt.xlabel('Simulations')
        plt.ylabel('Percent Chance')
        plt.subplot(313)
        plt.bar(index, (m_array/100), width, color = '#32CD32', label = "Mutation Probability")
        print len(m_array)
        plt.bar(index+width, (g_array/100), width, color = '#551A8B', label = "Generate Probability")
        print len(g_array)
        if DISPLAY_LEGENDS:
            plt.legend()
        plt.xlabel('Simulations')
        plt.ylabel('Percent Chance')
        saveFile =  str(os.path.dirname(os.path.realpath(__file__)) + \
                '\\Graph_Output\\'  + t_name + ' - chance vs fitness.png')
        plt.savefig(saveFile)    

    
    def ins_graph(self, array, t_name):
        """
        Plot the graph of the average types of instructions winning Kats had
        
        Attributes
        ----------
        array : 2d array containing the number of instructions a Kat had and a
                breakdown of the percentage of each instruction type
        t_name: Test Name if running mulitple tests in a row
        """
        fig_title = t_name + " Avg Instructions"
        plt.figure(fig_title)
        
        plt.subplot(211)
        title = str('AVG: # Of Instructions VS % Of Instruction Types FOR [' + \
                str(NUM_OF_GENERATIONS) + '] GENERATIONS\n'+ t_name)
        plt.title(title)
        plt.ylabel('# Of Instructions')
        plt.ylim(0, np.max(array[:,5])+1)
        plt.plot(array[:,5])
        
        plt.subplot(212)
        plt.xlabel('Number of generations')
        plt.ylabel('% Of Instrucitions')
        plt.plot(array[:,0], color=GRASS_COLOR, label = 'AVG Grass Instructions')
        plt.plot(array[:,1], color=LAVA_COLOR, label = 'AVG Lava Instructions' )
        plt.plot(array[:,2], color=BERRY_COLOR, label = 'AVG Berry Instructions')
        plt.plot(array[:,3], color=KATS_KOLOR, label = 'AVG Kats Instructions')
        plt.plot(array[:,4], color=WALL_COLOR, label = 'AVG Wall Instructions')
        if DISPLAY_LEGENDS:
            plt.legend()
        saveFile = str(os.path.dirname(os.path.realpath(__file__)) + \
                '\\Graph_Output\\'  + t_name + ' - instruction graph.png')
        plt.savefig(saveFile)    

    def show_plots(self):
        plt.close(1)
        if (DISPLAY_GRAPHS):
            plt.show()
        else:
            plt.close()