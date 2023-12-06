import numpy as np

def generate_random_starting_positions(worldsize, obstacles, n_creatures):
    possible_positions = np.array([(y,x) for y in range(worldsize[0]) for x in range(worldsize[1])])
    possible_positions = np.array([(t[0], t[1]) for t in possible_positions if obstacles[t[0], t[1]] == 0])
    random_indices = np.random.choice(range(len(possible_positions)), size=n_creatures, replace=False)
    start_positions = possible_positions[random_indices]
    return start_positions

def scale_to_range(x, old_range, new_range):

    if old_range[0] > old_range[1]:
        raise ValueError(f'Expected (min, max) range, but got {old_range}')
    
    if new_range[0] > new_range[1]:
        raise ValueError(f'Expected (min, max) range, but got {new_range}')

    numerator = (new_range[1] - new_range[0]) * (x - old_range[0])
    denominator = old_range[1] - old_range[0]

    return numerator/denominator + old_range[0]