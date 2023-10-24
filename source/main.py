from world import world
from creature import creature
import numpy as np
from simulation import run_simulation

def get_params():
    worldsize                 = (100,100)
    obstacle_matrix           = np.zeros(shape=worldsize)
    shelter_matrix            = np.zeros(shape=worldsize)
    shelter_matrix[:, 20:]    = np.ones(shape=shelter_matrix[:, 20:].shape)

    params = {
        'seed': 1,
        'n_creatures': 100,
        'n_days': 100,
        'n_timesteps': 100,
        'worldsize': worldsize,
        'obstacle_matrix': obstacle_matrix,
        'shelter_matrix': shelter_matrix,
    }

    return params
#--------------------------------------------------------------------------------------------------------

def get_creature_initializations(n_creatures, worldsize):
    possible_positions = np.array([(y,x) for y in range(worldsize[0]) for x in range(worldsize[1])])
    random_indices = np.random.choice(range(len(possible_positions)), size=n_creatures, replace=False)
    start_positions = possible_positions[random_indices]

    # reproduction chances are so far only a dummy variable and are fixed to be 1.
    start_reproduction_chances = np.ones(shape=n_creatures)

    start_directions = np.random.choice(['up', 'down', 'left', 'right'], size=n_creatures, replace=True)

    return start_positions, start_reproduction_chances, start_directions


#----------------------------------------------------------------
#-----                          main                        -----
#----------------------------------------------------------------

if __name__=='__main__':
    params = get_params()
    np.random.seed(params['seed'])
    # Initialize world and creatures for the first time
    simworld = world(size=params['worldsize'],
                     obstacles=params['obstacle_matrix'],
                     shelter=params['shelter_matrix'])

    # Initialize first creature population
    initial_creatures = [creature(position=p,
                                  reproduction_chance=r,
                                  direction=d) for p, r, d in zip(*get_creature_initializations(params['n_creatures'], params['worldsize']))]
    
    simdays, simcreatures = run_simulation(world=simworld,
                                           initial_creatures=initial_creatures,
                                           n_days=params['n_days'],
                                           n_timesteps=params['n_timesteps'])