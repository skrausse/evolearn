import numpy as np

# ------------------------------------------------------------------
#             UI to set the parameters for the simulation
#-------------------------------------------------------------------

# random seed for chance initialization of positions
seed                    = 1

# (y,x) size of the world
worldsize               = (100,100)

# Initial population size of creatures
n_creatures             = 100

# Number of days in the simulation
n_days                  = 100

# Number of timesteps in a day
n_timesteps             = 100

# !!!   Obstacles and shelter are defined in matrices with first index being y-corrdinate and second index x-coordinate   !!!
# No obstacles, therefore only zero matrix
obstacle_matrix         = np.zeros(shape=worldsize)

# Defining the right most 20 bins as shelter. 
shelter_matrix          = np.zeros(shape=worldsize)
shelter_matrix[:, 20:]  = np.ones(shape=shelter_matrix[:, 20:].shape)


# Gathering of the parameters into a diticionary to pass along
params = {
        'seed': seed,
        'n_creatures': n_creatures,
        'n_days': n_days,
        'n_timesteps': n_timesteps,
        'worldsize': worldsize,
        'obstacle_matrix': obstacle_matrix,
        'shelter_matrix': shelter_matrix,
    }