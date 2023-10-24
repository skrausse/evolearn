from day import day
from creature import creature
import warnings
import numpy as np

#--------------------------------------------------------------------------------------------------------

def creature_inheritence(creatures, shelter, worldsize):
    # Only creatures at shelter survive
    selection_index = np.array([c.at_shelter(shelter) for c in creatures])
    creature_directions = np.array([c.direction for c in creatures])
    creature_reproduction_chances = np.array([c.reproduction_chance for c in creatures])

    remaining_directions = creature_directions[selection_index]
    remaining_reproduction_chances = creature_reproduction_chances[selection_index]

    # Initialize new random start position for the remaining cretures
    possible_positions = np.array([(y,x) for y in range(worldsize[0]) for x in range(worldsize[1])])
    random_indices = np.random.choice(range(len(possible_positions)), size=len(remaining_directions), replace=False)
    start_positions = possible_positions[random_indices]

    # Initialize new population
    new_creatures = [creature(position=p,
                              reproduction_chance=r,
                              direction=d) for p, r, d in zip(start_positions, remaining_reproduction_chances, remaining_directions)]

    return new_creatures


#----------------------------------------------------------------
#-----                          main                        -----
#----------------------------------------------------------------

def run_simulation(world, initial_creatures, n_days=10, n_timesteps=10):
    # For the first day, the initial creature population is also the working creature population
    simcreatures = initial_creatures
    
    # Run simulation over n_days and store results in initialized lists.
    days_in_simulation = []
    creatures_after_days = []
    for day_idx in range(n_days):

        # Initialize a new day
        simday = day(world=world,
                    creatures=simcreatures,
                    timesteps=n_timesteps)

        # Run the simulation of one day
        for t in range(n_timesteps):
            simday.run_timestep(t)

        # Store results of the day
        days_in_simulation.append(simday)
        creatures_after_days.append(simday.creatures)

        # Run inheritence rule to create creature population of the next day
        simcreatures = creature_inheritence(simday.creatures, world.shelter, world.size)

        # Check whether there are creatures remaining, if not end the simulation
        if len(simcreatures) == 0:
            warnings.warn(f'No creatures remaining after {day_idx+1}/{n_days} days. Simulation is therefore cut short.')
            break

    return days_in_simulation, creatures_after_days