import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import warnings

class day():
    def __init__(self, world, creatures, timesteps):
        self.world = world
        self.creatures = creatures
        self.creature_positions = self.calculate_creature_positions()
        self.timesteps = timesteps

        # creature_history is used to store the different creature_position_matrices of each timestep in a day.
        self.creature_history = np.empty(shape=(self.timesteps + 1, self.world.size[0], self.world.size[1]))
        self.creature_history.fill(np.nan)
        self.creature_history[0,:,:] = self.creature_positions

    #-----------------------------------------------------------
    
    def calculate_creature_positions(self):
        creature_positions = np.zeros(shape=self.world.size)
        for creature in self.creatures:
            creature_positions[creature.position[0], creature.position[1]] += 1

        # unit tests
        if np.max(creature_positions) > 1:
            raise ValueError('Multiple creatures on same position in the World. Please change initialization!')
        
        return creature_positions
    
    #-----------------------------------------------------------
    
    def update_creature_position(self, old_position, new_position):
        self.creature_positions[old_position[0], old_position[1]] = 0
        self.creature_positions[new_position[0], new_position[1]] = 1

    #-----------------------------------------------------------
    
    def run_timestep(self, t):
        if t >= self.timesteps:
            raise ValueError(f'Expected timestep index t to be below {self.timesteps}, but got {t}')
        for creature in self.creatures:
            old_position = creature.position
            creature.update_creature(self.creature_positions, self.world.obstacles, self.world.size)
            self.update_creature_position(old_position, creature.position)
        self.creature_history[t+1,:,:] = self.creature_positions

    #-------------------------------------------------------------

    def plot_day(self, day_index, savedir, fps, dpi, scale):
        if os.path.exists(f'{savedir}/day_{day_index}.mp4'):
            warnings.warn('Animation for this day has has already been created and will therefore be skipped.')
            return None
        elif not os.path.exists(f'{savedir}'):
            os.mkdir(f'{savedir}')

        # create a colormap object
        cmap_shelter = plt.get_cmap('Greens')
        cmap_shelter.set_under((0,0,0,0))

        cmap_obstacles = plt.get_cmap('Reds')
        cmap_obstacles.set_under((0,0,0,0))

        cmap_creatures = plt.get_cmap('Greys')
        cmap_creatures.set_under((0,0,0,0))

        aspect_ratio = self.world.size[0]/self.world.size[1]
        fig, ax = plt.subplots()#figsize=(scale,scale*aspect_ratio), dpi=dpi)

        frames = []
        for history in self.creature_history:
            ax.set_ylim((-1,self.world.size[0]+1))
            ax.set_xlim((-1,self.world.size[1]+1))
            ax.axis('off')
            ax.set_title(f'Day {day_index}')
            
            img1 = ax.imshow(self.world.shelter, cmap=cmap_shelter, vmin=0.1, vmax=1, alpha=0.5, zorder=-5, animated=True)
            img2 = ax.imshow(self.world.obstacles, cmap=cmap_obstacles, vmin=0.1, vmax=1, alpha=0.5, zorder=-4, animated=True)
            img3 = ax.imshow(history, cmap=cmap_creatures, vmin=0.1, vmax=1, alpha=1, zorder=5, animated=True)
            frames.append([img1, img2, img3])

        ani = animation.ArtistAnimation(fig, 
                                        frames, 
                                        blit=True, 
                                        interval=1000/fps, 
                                        repeat=False)

        ani.save(f'{savedir}\\day_{day_index}.mp4') 