import Kat
import numpy as np

# Assume mutation of only one instruction (default) from each set
def mutate_kat(kat, mutate_fraction = .5):
    """Mutate the Kat agent by changing its instruction.

    Attributes
    ----------
    mutate_fraction
        the fraction of instructions to mutate
    """
    inst_size = len(kat.instruction_set_1)
    if(inst_size > 0):
        num_mutate = int(max(1,inst_size * mutate_fraction))

        change_state(kat, num_mutate,inst_size)
        rotate(kat, num_mutate,inst_size)
        flip(kat, num_mutate,inst_size)

def change_state(kat, num_mutate, instruction_1_size):
    """Mutate function that will randomly reasign the state of the given number
    of instructions.
    """
    rand_chosen_instr_set1 = np.random.randint(0, high=instruction_1_size, size=num_mutate)
    for instruction in rand_chosen_instr_set1:
        newState = np.random.randint(0,5)
        for i in range(4):
            newTuple = (kat.instruction_set_1[instruction][i][0][0][0], \
            kat.instruction_set_1[instruction][i][0][0][1], newState)
            kat.instruction_set_1[instruction][i][0][0] = newTuple


def rotate(kat, num_mutate, instruction_1_size):
    """Mutate function that will randomly rotate the decision of
    the given number of instructions
    """
    # Getting the size of the instruction set and choose instructions
    # randomly to mutate.
    rand_chosen_instr_set1 = np.random.randint(0, high=instruction_1_size, size=num_mutate)
    #NOTE: this is rotation mutation
    for instruction in rand_chosen_instr_set1:
        #saving last mirror
        temp_decision_set1 = kat.instruction_set_1[instruction][-1][1]
        #rotate from (second from last) to (last), (third from last) to (second from last),
        #(fourth from last) (i.e. first) to (third from last)
        for mirror in [2, 1, 0, -1]:
            kat.instruction_set_1[instruction][mirror+1][1] = \
            kat.instruction_set_1[instruction][mirror][1]
            #put the temp decision before for second for loop back in
            if mirror == -1:
                kat.instruction_set_1[instruction][mirror+1][1] = temp_decision_set1

def flip(kat, num_mutate, instruction_1_size):
        """Mutate function that will randomly flip the decision of the
        number given number of instructions

        """
        rand_chosen_instr_set1 = np.random.randint(0, high=instruction_1_size, size=num_mutate)
        for instruction in rand_chosen_instr_set1:
            #saving first mirror
            temp_decision_set1 = kat.instruction_set_1[instruction][0][1]

            #first time switch first with third, second time switch second with
            #fourth mirror
            for mirror in [0, 1]:
                if mirror == 1:
                    #saving second mirror
                    temp_decision_set1 = kat.instruction_set_1[instruction][1][1]

                #swith first with third mirror
                kat.instruction_set_1[instruction][mirror][1] = \
                kat.instruction_set_1[instruction][mirror+2][1]
                kat.instruction_set_1[instruction][mirror+2][1] = \
                temp_decision_set1

def create_compound(kat, num_mutate, instruction_1_size):
    pass
