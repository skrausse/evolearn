import numpy as np


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
    
    def get_creatures(self):
        return self.creatures
    
    #-----------------------------------------------------------
    
    def get_creature_positions(self):
        return self.creature_positions
    
    #-----------------------------------------------------------
    
    def get_obstacles(self):
        return self.world.obstacles
    
    #-----------------------------------------------------------
    
    def get_shelter(self):
        return self.world.shelter
    
    #-----------------------------------------------------------
    
    def get_worldsize(self):
        return self.world.size
    
    #-----------------------------------------------------------
    
    def get_creature_history(self):
        return self.creature_history

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