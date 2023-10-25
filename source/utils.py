import numpy as np

def generate_random_starting_positions(worldsize, obstacles, n_creatures):
    possible_positions = np.array([(y,x) for y in range(worldsize[0]) for x in range(worldsize[1])])
    possible_positions = np.array([(t[0], t[1]) for t in possible_positions if obstacles[t[0], t[1]] == 0])
    random_indices = np.random.choice(range(len(possible_positions)), size=n_creatures, replace=False)
    start_positions = possible_positions[random_indices]
    return start_positions