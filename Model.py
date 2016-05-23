import numpy as np
import copy
from Kat import Kat
from Visualize import Visualizer
from SimManager import sim_manager
from hg_settings import *
import Hunger_Grid as hg

top_kats = []
avg_kats = []
NUM_SIMS = 300
STEPS_PER_SIM = 300
STEP_SIZE = -1 # 0 = only last frame,
                # 1 = every frame,
                # N = every N frames
                # -1 = don't show

def one_sim(seed_kat):
    """Run one simulation of number of time steps (default: 300)

    First initialize a sim_manager with first Kat agent.
	Then update at each time steps, finally taking the top
	Kat and top fitness score, returns it.
    """
    sim_temp = sim_manager(seed_kat)
    for i in range(NUM_OF_TRIALS):
        sim_temp.clear_grid()
        for j in range(STEPS_PER_SIM):
            if(sim_temp.kats[i].dead == False):
                sim_temp.update(i)
            else:
                break

    avg_fitness = sim_temp.average_fitness()
    kat_temp, score_temp = sim_temp.top_kat()
    return copy.deepcopy(kat_temp), score_temp, sim_temp.return_playback(), avg_fitness

def playback(vis, pb):
    if (STEP_SIZE == -1):
        return
    if (STEP_SIZE == 0):
        vis.show(pb[-1])
    else:
        for i in np.arange(0,len(pb), STEP_SIZE):
            vis.show(pb[i])


def model(seed_kat, vis):
    """Run multiple simulation of number of time steps each,
	(default: 300 simulations).

    In a loop, keep running each simulation of 300
	number of time steps, append the top fitness score,
	and after loops ended, graph the fitness score over
	generations (simulations).
    """
    for i in np.arange(1, NUM_SIMS):
        print "Gen:", i
        seed_kat, fit_score, play, avg_fitness = one_sim(seed_kat)
        top_kats.append(fit_score)
        avg_kats.append(avg_fitness)
        playback(vis, play)
    vis.graph(top_kats)


progenitor = Kat(0,0)
vis = Visualizer(hg.createHungerGrid())
model(progenitor, vis)
