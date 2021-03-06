import copy
import numpy as np
import Hunger_Grid as hg
import Mutate as m
from Kat import Kat
from Visualize import Visualizer
from hg_settings import *
import time


GRID_DIMENSION = 34
NUM_KATS = NUM_OF_INDIVIDUALS

# MOVE = {[-1,0]:"UP", [0,1]:"RIGHT", [1,0]:"DOWN", [0,-1]:"LEFT"}
MOVE = [[-1,0],[0,1],[1,0],[0,-1],[0,0]]

class sim_manager(object):
    """
    Attributes
    ----------
    seedKat : Kat
        The first Kat agent.

    Other Attributes
    ----------------
    grid : 2D numpy array
        The environment that Kats agents will live in, with the states
        of each cell already set.

    kats : list
        A list of Kats agent

    vis : Visualizer
	    A Visualizer class used to visualize simulation, observe
        simulation, and diagnose possible problem.
    """
    def __init__(self, seedKat, hunger_grid, mutate_var, multi_cat=False):
        self.grid = np.array(hunger_grid.get_grid())

        if not multi_cat:
            self.kats = [seedKat.clone() for i in range(NUM_KATS)]
        else:
            temp_kats = seedKat * (NUM_OF_INDIVIDUALS/5)
            self.kats = []
            for kat in temp_kats:
                self.kats.append(kat.clone())
        self.playback = []

        # Print Statements
        #seedKat.print_ins_1()
        #seedKat.print_ins_2()

        for i in range(NUM_KATS):
            #self.kats[i] = seedKat.clone()
            if(i >= AMT_CLONE):
                m.mutate_kat(self.kats[i], mutate_var)

        for k in self.kats:
            self.setKatPosition(k)

    #Was able to see kat's behavior near the wall,
    #which was exactly what we predicted, so thought to
    #keep it here for a bit
    def kat_surround(self, kat_num):
        print "Kat's current fitness is"
        print self.kats[kat_num].calculate_fitness
        print "Kat's surround grid state"
        print self.grid[self.kats[kat_num].yLoc-1, self.kats[kat_num].xLoc-1]
        print self.grid[self.kats[kat_num].yLoc-1, self.kats[kat_num].xLoc]
        print self.grid[self.kats[kat_num].yLoc-1, self.kats[kat_num].xLoc+1]
        print self.grid[self.kats[kat_num].yLoc, self.kats[kat_num].xLoc+1]
        print self.grid[self.kats[kat_num].yLoc+1, self.kats[kat_num].xLoc+1]
        print self.grid[self.kats[kat_num].yLoc+1, self.kats[kat_num].xLoc]
        print self.grid[self.kats[kat_num].yLoc+1, self.kats[kat_num].xLoc-1]
        print self.grid[self.kats[kat_num].yLoc, self.kats[kat_num].xLoc-1]

    def update(self, kat_num, step_num):
        """Update the Kat agents at each time step.

        Only update Kat agents that are alive. First ask
		Kat agent where they want to move, then record the
		next move's x and y location. According to different
		state of the next cell, different action will be taken.
        """
        if(self.kats[kat_num].dead == False):
            direction = MOVE[self.kats[kat_num].make_decision(self.grid)]
            nextX = self.kats[kat_num].xLoc + direction[1]
            nextY = self.kats[kat_num].yLoc + direction[0]
            if direction != MOVE[DO_NOTHING]:
                self.grid[self.kats[kat_num].yLoc, self.kats[kat_num].xLoc] = GRASS

                if(self.grid[nextY,nextX] == LAVA):
                    self.kats[kat_num].die()

                elif(self.grid[nextY, nextX] == BERRY):
                    self.kats[kat_num].eat_berry()
                    self.kats[kat_num].take_step(nextY, nextX)
                    self.grid[self.kats[kat_num].yLoc, self.kats[kat_num].xLoc] = KAT

                elif(self.grid[nextY, nextX] == GRASS):
                    self.kats[kat_num].take_step(nextY, nextX)
                    self.grid[self.kats[kat_num].yLoc, self.kats[kat_num].xLoc] = KAT
        
        self.playback.append([copy.deepcopy(self.grid), \
                            self.kats[kat_num].print_ins_1(PRINT = False),
                            kat_num,
                            step_num])
    
    def start_kat(self, kat_num):
        self.grid[self.kats[kat_num].yLoc, self.kats[kat_num].xLoc] = KAT
    
    def setKatPosition(self, kat):
        """Set the Kat agent's initial position to center of map.
        """
        kat.xLoc = GRID_DIMENSION/2
        kat.yLoc = GRID_DIMENSION/2


    def return_playback(self):
        return self.playback

    def top_kat(self):
        """Find the top fitness score of all Kat agents.

        First it takes the fitness score of first Kat in
		the list. As it loops through the list, when a higher
		fitness score found, top_score is updated, the Kat with
		the highest fitness score is cloned and returned along
		with the fitness score.
        """
        top_score = 0
        top_location = 0
        print "Kat Fitness: "
        for i in range(NUM_KATS):
            print i,": " ,self.kats[i].calculate_fitness()
            if(self.kats[i].calculate_fitness() > top_score):
                top_score = self.kats[i].calculate_fitness()
                top_location = i
        print "Winning Score KAT ", top_location, ": " , top_score
        print "TOP KAT INS1: "
        self.kats[top_location].print_ins_1()
        return copy.deepcopy(self.kats[top_location].clone()), top_score

    def top_kats(self):
        def get_key(kat):
            return kat.calculate_fitness()
        top_kats = sorted(self.kats, key=get_key)
        return top_kats[-5:]

    def average_fitness(self):
        total_fitness = sum([i.calculate_fitness() for i in self.kats])
        return total_fitness / float(len(self.kats))

    def clear_grid(self, hunger_grid):
        self.grid = np.array(hunger_grid.get_grid())
        
    def tk_breakdown(self):
        """
        Get the top kats instruction set by the amount of INS that use a 
        particular instrucion
        """
        tk = self.top_kats()
        return tk[0].report_ins()

