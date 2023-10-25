from world import world
from creature import creature
from config import params

import numpy as np

#--------------------------------------------------------------------------------------------------------

def creature_initializations(n_creatures, worldsize):
    possible_positions = np.array([(y,x) for y in range(worldsize[0]) for x in range(worldsize[1])])
    random_indices = np.random.choice(range(len(possible_positions)), size=n_creatures, replace=False)
    start_positions = possible_positions[random_indices]

    # reproduction chances are so far only a dummy variable and are fixed to be 1.
    start_reproduction_chances = np.ones(shape=n_creatures)

    start_directions = np.random.choice(['up', 'down', 'left', 'right', 'None'], size=n_creatures, replace=True)

    return start_positions, start_reproduction_chances, start_directions


#----------------------------------------------------------------
#-----                          main                        -----
#----------------------------------------------------------------

if __name__=='__main__':
    # Fix random seed
    np.random.seed(params['seed'])

    # Initialize first creature population
    initial_creatures = [creature(position=p,
                                  reproduction_chance=r,
                                  direction=d) for p, r, d in zip(*creature_initializations(params['n_creatures'], params['worldsize']))]
    
    # Initialize the simulation world
    simworld = world(size=params['worldsize'],
                     obstacles=params['obstacle_matrix'],
                     shelter=params['shelter_matrix'],
                     initial_creatures=initial_creatures,
                     n_days=params['n_days'],
                     n_timesteps=params['n_timesteps'])
    
    simworld.run_simulation()
    simworld.plot_days(savedir=f'{params["output_path"]}\\world_{simworld.world_id}',
                       fps=30,
                       dpi=50,
                       scale=10)