import numpy as np
from utils import scale_to_range

class brain():
    def __init__(self, creature):
        # ------------------------------------------------------------------
        #                       Initializing variables                    
        # ------------------------------------------------------------------
        
        self.synaptic_weights = np.zeros(shape=(256, 256))
        self.neuron_state = np.zeros(shape=(256))
        self.creature = creature
        self.genome = self.creature.genome
        # ------------------------------------------------------------------
        #                       Input checks                    
        # ------------------------------------------------------------------
        if len(self.genome)%6 != 0:
            raise ValueError(f'Genome not readable. Expected hex code with len multiple of 6, but got {self.genome} of len {len(self.genome)}.')

        # ------------------------------------------------------------------
        # Reading the genes in the genome and initializing the synaptic weight matrix
        # ------------------------------------------------------------------

        genes = [self.genome[i:i+6] for i in range(len(self.genome)/6)]

        for gene in genes:
            sending_neuron = int(gene[0:2], 16)
            
            receiving_neuron = int(gene[2:4], 16)

            weight = scale_to_range(int(gene[4:6], 16), 
                                    old_range=(0,255), 
                                    new_range=(-1,1))   

        self.synaptic_weights[sending_neuron, receiving_neuron] = weight

    # ------------------------------------------------------------------

    def read_sensory_input(self, world):
        """
        Values 0-63 encoding the sensory neurons in the brain.
            0  - obstacle forward
            1  - obstacle left
            2  - obstacle right
            3  - obstacle 
            4  - obstacle north
            5  - obstacle east
            6  - obstacle west
            7  - obstacle south
            
            8  - creature forward
            9  - creature left
            10 - creature right
            11 - creature backward
            12 - creature north
            13 - creature east
            14 - creature west
            15 - creature south
            
            16 - at shelter
            17 - shelter forward
            18 - shelter left
            19 - shelter right
            20 - shelter backward
            21 - shelter north
            22 - shelter east
            23 - shelter west
            24 - shelter south
            
            --- To give the absolut position I split the world in to quadrants recursively
            --- So quadrant 1 of grain n is the top left quadrant of the selected quadrant of grain n-1

            25 - grain 1 quadrant 1
            26 - grain 1 quadrant 2
            27 - grain 1 quadrant 3
            28 - grain 1 quadrant 4
            29 - grain 2 quadrant 1
            30 - grain 2 quadrant 2
            31 - grain 2 quadrant 3
            32 - grain 2 quadrant 4
            33 - grain 3 quadrant 1
            34 - grain 3 quadrant 2
            35 - grain 3 quadrant 3
            36 - grain 3 quadrant 4
            37 - grain 4 quadrant 1
            38 - grain 4 quadrant 2
            39 - grain 4 quadrant 3
            40 - grain 4 quadrant 4
            41 - grain 5 quadrant 1
            42 - grain 5 quadrant 2
            43 - grain 5 quadrant 3
            44 - grain 5 quadrant 4

            45 - facing north 
            46 - facing east
            47 - facing west
            48 - facing south

            --- Possible future sensory input neurons

            49 - oscillator (not implemented yet)
            50 - random firing (not implemented yet)
            51 - 
            52 - 
            53 - 
            54 - 
            55 -  
            56 - 
            57 - 
            58 - 
            59 - 
            60 - 
            61 - 
            62 - 
            63 -      
        """
        pass
    
    # ------------------------------------------------------------------

    def calculate_timestep(self, world, threshold):
        self.neuron_state[:64] = self.read_sensory_input(world)
        self.neuron_state = np.matmul(self.synaptic_weights, self.neuron_state)
        binarized_array = np.zeros(shape=self.neuron_state.shape)
        binarized_array[self.neuron_state > threshold] = 1
        self.neuron_state = binarized_array

    # ------------------------------------------------------------------

    def get_motor_output(self):
        """
        0-127: Senroy neurons
        128-191: Hidden neurons
        192-256: Motor neurons

        192: move forward
        193: move backwards
        194: move left
        195: move right
        196: do nothing
        
        """
        movement_vector = self.neuron_state[192:]
