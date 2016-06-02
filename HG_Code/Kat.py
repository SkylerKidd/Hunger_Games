import random
import numpy as np
import copy
from hg_settings import *
# Condition (Grass:0| Lava:1| Berry:2| Kat:3| Wall:4)
# Decision Code (up:0| right:1| down:2| left:3)

class Kat(object):
    """Create and manage a Kat agent.

    Attributes
    ----------
    x : int
        The x location of the Kat agent.

    y : int
        The y location of the Kat agent.

    Other Attributes
    ----------------
    berries_eaten : int
        The number of berries that Kat agent has ate.

    steps_taken : int
        The number of steps that Kat agent has walked.

    instruction_set_1 : list
        A list of tier 1 instructions that Kat agent has.

    instruction_set_2 : list
        A list of tier 2 instructions that Kat agent has.

    instruction_set_3: list
        A list of tier 3 instructions that Kat agent has.

    dead : boolean
        A boolean value that indicate if the Kat agent is dead.
    """
    def __init__(self, x=0, y=0):
        self.xLoc = x
        self.yLoc = y
        self.instruction_set_1 = []
        self.instruction_set_2 = []
        self.instruction_set_3 = []
        self.reset()

    def __repr__(self):
        return "<Fitness: %s, End Loc: (%s,%s)>" % \
               (self.calculate_fitness(),self.yLoc,self.xLoc)

    def reset(self):
        """Reset the Kat agent's attributes and mirror's position.

        Attributes resettable are steps_taken, berries_eaten, and dead.
		Mirror's positions are sorted according to their index using sorted().
        """
        def get_key(mirror):
            return mirror[2]
        for instruction_set in [self.instruction_set_1, \
                                self.instruction_set_2, \
                                self.instruction_set_3]:
            for i in range(len(instruction_set)):
                instruction_set[i] = sorted(instruction_set[i], key=get_key)
        self.steps_taken = 0
        self.berries_eaten = 0
        self.dead = False

    def clone(self):
        self.reset()
        return copy.deepcopy(self)

    def calculate_fitness(self):
        """Calculate the fitness value of this Kat agent.

        The metrics to consider are the number of steps the Kat
        agent has taken and the amount of berries eaten.
        """
        return self.steps_taken * STEP_VALUE + (self.berries_eaten * BERRY_VALUE)

    # Only reads 1 instruction set at the moment
    def make_decision(self, grid):
        """The Kat makes a decision on its next move.

        This function works with SimManager module.
        Kats goes through list of instructions at each level
        and check if the any of the condition (place & state)
        is valid and the decision is a valid decision. If
        decision is not valid, shuffle the mirrors in that
        instruction and generate a new behavior.
        """
        for instruction_set in [self.instruction_set_3, self.instruction_set_2, self.instruction_set_1]:
            for instruction in instruction_set:
                #print("heheh")
                for i in range(len(instruction)): # mirror == instruction[i]
                    #print(mirror)
                    for plc_state in instruction[i][0]:
                        if not self.place_is_state(grid, plc_state):
                            if self.is_valid_move(grid, instruction[i][1]):
                                #print mirror[0]
                                temp_mirror = instruction.pop(i)
                                instruction.insert(0, temp_mirror)
                                return instruction[i][1] # Return its decision
                            else:
                                #np.random.shuffle(instruction) # Shuffle mirror
                                temp = instruction.pop(0)#new method for shuffling
                                instruction.append(temp)
                                return DO_NOTHING
                            
        #return self.generate_behavior(grid)
        return DO_NOTHING

    def place_is_state(self, grid, plc_state):
        """Check if the place (i.e. cell on a grid) is one of
        the expected state.
        """
        if (grid[(self.yLoc + plc_state[0]), (self.xLoc + plc_state[1])] == plc_state[2]):
            #print plc_state
            return True
        return False

    def is_valid_move(self, grid, move):
        """Check if the move is a valid move. If the
        desired spot is a wall or another Kat agent,
        it is considered an invalid move.
        """
        if move == DOWN:
            attempt = grid[self.yLoc+1, self.xLoc]
        elif move == RIGHT:
            attempt = grid[self.yLoc, self.xLoc+1]
        elif move == UP:
            attempt = grid[self.yLoc-1, self.xLoc]
        elif move == LEFT:
            attempt = grid[self.yLoc, self.xLoc-1]
        else:
            raise Exception("Move was an invalid code.")
        if attempt == WALL or attempt == KAT:
            return False
        else:
            return True

    def print_ins_1(self, PRINT = True):
        """Print Kat agent's tier 1 instructions

	Prints all the place, state, and decision of the instructions.
	
	"""
        if PRINT:
            print ("\nKat T1: ")
        if(len(self.instruction_set_1) == 0):
            full_report = "\nNO T1 INSTRUCTIONS"
            if PRINT:
                print full_report
            return full_report
        full_report = "\n"
        for i in range(len(self.instruction_set_1)):
            rel_coord = str((self.instruction_set_1[i][0][0][0][0],self.instruction_set_1[i][0][0][0][1]))
            tile_state = TILE_STRING[self.instruction_set_1[i][0][0][0][2]]
            move_string = MOVE_STRING[self.instruction_set_1[i][0][1]]
            ins_string = "%s.) IF %s IS %s %s" % (str(i), rel_coord, tile_state, move_string)
            if PRINT:
                print (ins_string)
            full_report += ins_string + "\n"
        return full_report

    def print_ins_2(self):
        """Print Kat agent's tier 2 instructions

        Prints all the place, state, and decision of the instructions.
        """
        print ("\nKat T2: ")
        print (self.instruction_set_2)

    def take_step(self,yLoc,xLoc):
        self.yLoc = yLoc
        self.xLoc = xLoc
        self.steps_taken +=  1

    def die(self):
        self.dead = True

    def eat_berry(self):
        self.berries_eaten += 1

    def generate_behavior(self, grid):
        """Generate a new behavior for the Kat agent.

        A cell is randomly selected with the state at
        that cell recorded. A new instruction is then
        created with the coordinates and the state.
        A decision for first mirror is randomly selected
        with other decision being mirrored decision.
        The new instruction becomes the Kat's first
        priority instruction.
        """
        def get_key(mirror):
            return mirror[2]
        yGrab, xGrab = 0, 0
        while (yGrab,xGrab) == (0,0):
			#randint is exclusive
			print "infinite loop in generate_behavior in kat"
            #yGrab = random.randint(-2,2)
            #xGrab = random.randint(-2,2)
        #init_decision = random.randint(0,3)
        state = grid[self.yLoc + yGrab][self.xLoc + xGrab]
        instruction = [[[( yGrab,  xGrab, state)],init_decision,0],\
                       [[( xGrab, -yGrab, state)],(init_decision+1)%4,1],\
                       [[(-yGrab, -xGrab, state)],(init_decision+2)%4,2],\
                       [[(-xGrab,  yGrab, state)],(init_decision+3)%4,3]]
        self.instruction_set_1 = [instruction] + self.instruction_set_1
        return init_decision

    def report_ins(self):
        report = np.zeros(6)
        for instruction_set in [self.instruction_set_3, self.instruction_set_2, self.instruction_set_1]:
            for instruction in instruction_set:
                report[instruction[0][0][0][2]] += 1
                report[5] += 1
        report[:5] /= report[5]
        return report
        
                    