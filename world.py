import numpy as np

class world():
    
    def __init__(self, size, obstacles, shelter):     
        self.set_size(size)
        self.set_obstacles(obstacles)
        self.set_shelter(shelter)        
        
    #-----------------------------------------------------------
    
    def get_size(self):
        return self.size
    
    #-----------------------------------------------------------
    
    def get_obstacles(self):
        return self.obstacles
    
    #-----------------------------------------------------------
    
    def get_shelter(self):
        return self.shelter
    
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
        