from day import day
from creature import creature
import warnings
import numpy as np
from tqdm import tqdm
import datetime
from utils import generate_random_starting_positions

class world():
    
    def __init__(self, size, obstacles, shelter, initial_creatures, n_days, n_timesteps, world_id=None):     
        # Internal variables that need no initialization.
        self.simulated_days = []
        self.simulated_creatures = []
        self.day_counter = 0

        # Initialized parameters from the outside as function call to add unit tests.
        self.set_size(size)
        self.set_obstacles(obstacles)
        self.set_shelter(shelter)
        self.set_n_days(n_days)
        self.simcreatures = initial_creatures
        self.n_timesteps = n_timesteps

        # create unique identifier for each world based on the creation time
        if world_id is None:
            now = datetime.datetime.now()
            self.world_id = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond)
        else:
            self.world_id = str(world_id)
    
    #-----------------------------------------------------------
    
    def set_size(self, size):
        self.size = size
    
    #-----------------------------------------------------------
    
    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        if self.obstacles.shape != self.size:
            raise ValueError('Size of obstacle matrix does not match the world size. Please change initialization!')
        
    #-----------------------------------------------------------
    
    def set_shelter(self, shelter):
        self.shelter = shelter
        if self.shelter.shape != self.size:
            raise ValueError('Size of shelter matrix does not match the world size. Please change initialization!')        
        if np.sum(np.logical_and(self.obstacles, self.shelter)) > 0:
            raise ValueError('Obstacles and shelter matrix are overlapping. Please change initialization!')

    #-----------------------------------------------------------
    
    def set_n_days(self, n_days):
        self.n_days = n_days
        if self.day_counter >= self.n_days:
            warnings.warn(f'There are already at least as many simulated days ({self.day_counter}) as requested by the n_days paramter ({self.n_days}) in this world!.')
            

    #--------------------------------------------------------------------------------------------------------

    def creature_inheritence(self, creatures):
        # Create array index to select only surviving creatures
        selection_index = np.array([c.at_shelter(self.shelter) for c in creatures])

        # Select surviving directions and randomly pick from those for the next generation
        remaining_directions = np.array([c.direction for c in creatures])[selection_index]
        new_directions = np.random.choice(remaining_directions, len(creatures), replace=True)
        
        # Select surviving reproduction_chances and randomly pick from those for the next generation
        remaining_reproduction_chances = np.array([c.reproduction_chance for c in creatures])[selection_index]
        new_reproduction_chances = np.random.choice(remaining_reproduction_chances, len(creatures), replace=True)

        # Initialize new random start position for the remaining cretures
        new_positions = generate_random_starting_positions(worldsize=self.size, obstacles=self.obstacles, n_creatures=len(creatures))

        # Initialize new population
        new_creatures = [creature(position=p,
                                reproduction_chance=r,
                                direction=d) for p, r, d in zip(new_positions, new_reproduction_chances, new_directions)]
        return new_creatures
    
    #-----------------------------------------------------------

    def run_simulation(self):
        if self.day_counter != len(self.simulated_days):
            raise ValueError('The number of simulated days does not match the internal day counter. This is an internal error, sorry for that.')
        
        for day_idx in tqdm(range(self.day_counter, self.n_days, 1), 
                            desc=f'Simulating {np.max([0, self.n_days-self.day_counter])} new days ({self.day_counter} already simulated)',
                            total=np.max([0, self.n_days-self.day_counter]),
                            leave=None):
            
            # Initialize a new day
            simday = day(world=self,
                        creatures=self.simcreatures,
                        timesteps=self.n_timesteps)

            # Run the simulation of one day
            for t in range(self.n_timesteps):
                simday.run_timestep(t)

            # Store results of the day
            self.simulated_days.append(simday)
            self.simulated_creatures.append(simday.creatures)
            self.day_counter += 1
            
            # Run inheritence rule to create creature population of the next day
            self.simcreatures = self.creature_inheritence(creatures=simday.creatures)

            # Check whether there are creatures remaining, if not end the simulation
            if len(self.simcreatures) == 0:
                warnings.warn(f'No creatures remaining after {day_idx+1}/{self.n_days} days. Simulation is therefore cut short.')
                break

    #-----------------------------------------------------------

    def plot_days(self, savedir='./', fps=25, dpi=100, scale=10):
        for day_index, day in tqdm(enumerate(self.simulated_days),
                                   desc=f'Creating animation for {len(self.simulated_days)} days.',
                                   total=len(self.simulated_days),
                                   leave=None):
           
           day.plot_day(day_index, savedir=savedir, fps=fps, dpi=dpi, scale=scale)