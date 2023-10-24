from world import world
from creature import creature
from config import params


import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

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
    # Fix random seed
    np.random.seed(params['seed'])

    # Initialize first creature population
    initial_creatures = [creature(position=p,
                                  reproduction_chance=r,
                                  direction=d) for p, r, d in zip(*get_creature_initializations(params['n_creatures'], params['worldsize']))]
    
    # Initialize the simulation world
    simworld = world(size=params['worldsize'],
                     obstacles=params['obstacle_matrix'],
                     shelter=params['shelter_matrix'],
                     initial_creatures=initial_creatures,
                     n_days=params['n_days'],
                     n_timesteps=params['n_timesteps'])
    
    simworld.run_simulation()

    if not os.path.exists(f'world_{simworld.world_id}'):
        os.mkdir(f'world_{simworld.world_id}')

    # create a colormap object
    cmap_shelter = plt.get_cmap('Greens')
    cmap_shelter.set_under((0,0,0,0))

    cmap_obstacles = plt.get_cmap('Reds')
    cmap_obstacles.set_under((0,0,0,0))

    cmap_creatures = plt.get_cmap('Greys')
    cmap_creatures.set_under((0,0,0,0))

    for day_index, day in enumerate(simworld.simulated_days):
        fig, ax = plt.subplots()

        # Function to initialize the animation
        def init():
                
            ax.set_ylim((-1,simworld.size[0]+1))
            ax.set_xlim((-1,simworld.size[1]+1))
            ax.axis('off')
            ax.set_title(f'Day {day_index}')
            
            ax.imshow(np.flipud(simworld.shelter), origin='lower', cmap=cmap_shelter, vmin=0.1, vmax=1, alpha=0.5, zorder=-5)
            ax.imshow(np.flipud(simworld.obstacles), origin='lower', cmap=cmap_obstacles, vmin=0.1, vmax=1, alpha=0.5, zorder=-4)
            ax.imshow(np.flipud(day.creature_history[0]), origin='lower', cmap=cmap_creatures, vmin=0.1, vmax=1, alpha=1, zorder=5)
            return [ax]

        # Function to update the animation at each frame
        def update(frame):
            ax.clear()
            
            ax.set_ylim((-1,simworld.size[0]+1))
            ax.set_xlim((-1,simworld.size[1]+1))
            ax.axis('off')
            ax.set_title(f'Day {day_index}')
            
            ax.imshow(np.flipud(simworld.shelter), origin='lower', cmap=cmap_shelter, vmin=0.1, vmax=1, alpha=0.5, zorder=-5)
            ax.imshow(np.flipud(simworld.obstacles), origin='lower', cmap=cmap_obstacles, vmin=0.1, vmax=1, alpha=0.5, zorder=-4)
            ax.imshow(np.flipud(day.creature_history[frame]), origin='lower', cmap=cmap_creatures, vmin=0.1, vmax=1, alpha=1, zorder=5)
            return [ax]

        # Create the animation object
        fps = 25
        ani = FuncAnimation(fig, update, frames=len(day.creature_history), init_func=init, blit=True, interval=1000/fps, repeat=False)
        FFwriter = FFMpegWriter(fps=fps, codec='h264')
        ani.save(f'world_{simworld.world_id}/day_{day_index}.mp4', writer=FFwriter) 
        plt.show()