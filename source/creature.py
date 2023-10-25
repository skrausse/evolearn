class creature():
    def __init__(self, position, reproduction_chance, direction):
        self.set_position(position)
        self.set_reproduction_chance(reproduction_chance)
        self.set_direction(direction)
    
    #-----------------------------------------------------------
    
    def set_position(self, position):
        self.position = position
    
    #-----------------------------------------------------------
    
    def set_reproduction_chance(self, reproduction_chance):
        self.reproduction_chance = reproduction_chance
    
    #-----------------------------------------------------------

    def set_direction(self, direction):
        if direction not in ['up', 'down', 'left', 'right', 'None']:
            raise ValueError(f'Unknown direction provided. Expected element of ["up","down", "left", "right", "None"], but got "{direction}".')
        
        self.direction = direction
    
    #-----------------------------------------------------------
    
    def update_creature(self, creature_positions, obstacles, worldsize):

        match self.direction:
            case 'up':
                new_position = [self.position[0] + 1, self.position[1]]
            case 'down':
                new_position = [self.position[0] - 1, self.position[1]]
            case 'left':
                new_position = [self.position[0], self.position[1] - 1]
            case 'right':
                new_position = [self.position[0], self.position[1] + 1]
            case 'None':
                pass
            case 'other':
                raise ValueError(f'Unknown direction provided. Expected element of ["up","down", "left", "right", "None"], but got "{self.direction}".')
        
        if ((self.direction != 'None') and (self._valid_creature_move(new_position, creature_positions, obstacles, worldsize))):
            self.set_position(new_position)

    #-----------------------------------------------------------
    
    def _valid_creature_move(self, new_position, creature_positions, obstacles, worldsize):
        # List of illegal move conditions. If one is fulfilled, return False.
        if new_position[0] < 0:
            return False
        if new_position[1] < 0:
            return False
        if new_position[0] >= worldsize[0]:
            return False
        if new_position[1] >= worldsize[1]:
            return False
        if creature_positions[new_position[0], new_position[1]] > 0:
            return False
        if obstacles[new_position[0], new_position[1]] > 0:
            return False
        
        # If non of the illegal move conditions apply, return True
        return True

    #-----------------------------------------------------------
    
    def at_shelter(self, shelter):
        if shelter[self.position[0], self.position[1]] > 0:
            return True
        else:
            return False