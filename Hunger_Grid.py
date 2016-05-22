import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
# GRASS = 0
# LAVA = 1
# BERRIES = 2
# KATS = 3
# WALLS  = 4

LAVA_CHANCE = .02
BERRY_CHANCE = .05

def createHungerGrid(M = 34, N = 34, STATIC=True, P_LAVA = .02, P_BERRY = .05):
    """Create a grid of MxN size (default 34x34), 2 thick 'Wall' on the outside.
    Randomly place lava and berries based on the global LAVA/BERRY_CHANCE. STATIC
    determines how random numbers are generated, if TRUE, seed is 123456. Else
    make new seed each time.
    """
    tempGrid = np.zeros(shape=(M,N))
    if(STATIC):
        np.random.seed(123456)
    randLavaGrid = np.random.rand(M,N)
    np.place(tempGrid, randLavaGrid < P_LAVA, LAVA)
    randBerryGrid = np.random.rand(M,N)
    np.place(tempGrid, randBerryGrid < P_BERRY, BERRY)

    # Walls
    tempGrid[0:2, :] = WALL    # Top Row
    tempGrid[-2:, :] = WALL    # Bottom Row
    tempGrid[:, 0:2] = WALL    # Left Side
    tempGrid[:, -2:] = WALL    # Right Side

    hungGrid = np.array(tempGrid, dtype=int)
    return hungGrid
