# Introduction

I would like to build a simulator that plays around with the concepts of evolution and learning. For this simulator I would like to break it down into its most basic parts and see if I can build up some interesting behaviour from some first order principles of evolution and learning theory. The idea will be to have tiny creatures interact in some world. We can give them senses, motoric abilities and simple tasks within that world. I have in mind a grid world with square creatures that maybe can pick up some food to enhance their chance of reproduction, or some shelter they might need to find with some obstacles in the way. I am myself not quite sure of the details yet. Let me first introduce some basic principles and from there derive some basic plan to implement all of these ideas.

## Evolution

For evolution we need some crucial ingredients:
1. Information: Information of an organism must be stored in one place
2. Reproduction: This information has to be parsed on to some offspring
3. Variability: Errors in the information parsing lead to mutations that lead to genetic variability

For this our creatures need some blueprint, that encodes their whole information and is passed on to their children with slight mutations. The specific information needed for the creatures is dependent on the things they should be able to sense, execute or compute. 

## Learning

Learning is describing some knowledge gain from experience, that may or may not change the behaviour of our creature. Importantly, this change in behaviour may be achieved by one creature alone within its lifetime!

For our little scenario we may think of learning as changing the way we compute. To define this a little closer, let's describe the perception-execution loop of our creatures:
1. One or more senses get input and send signals
2. Computing nodes receive such a signal from the sensory parts and integrate / differentiate the information somehow
3. The output of step 2 is some signal that may be sent to the motor part of the system
4. The motor signal of step 3 is interpreted by the output system (motor system) and translated in some action that is then executed (e.g. move forward).
We can represent this sort of computation scheme very efficiently by a neural network with the sensory system being the input to the network and the motor system being the readout neurons of the network. The hidden units can perform any computation and may be connected in any way shape or form. 

Now to come back to the learning part: Learning (for our purposes) describes the change of the input-output relation based on prior knowledge/experience. Of course we have not even thought about a task for our creatures so far, so it is hard to imagine how learning would even work in such a scenario. But we can imagine our creatures as being completely unsupervised and therefore choose some learning rule from the realm of unsupervised learning. Spike timing dependent plasticity (STDP) seems to be a good candidate for this. STDP only considers the spike timing and adopts those for strengthening meaningful synapses and weakening meaningless ones.
$$
\Delta w = 
\begin{cases}
	\Delta w^+ = A^+e^{\frac{-\Delta t}{\tau_+}} &\text{ if } \Delta t > 0 \\
	\Delta w^- = -A^-e^{\frac{\Delta t}{\tau_-}} &\text{ if } \Delta t \leq 0
\end{cases}
$$
In this way the synaptic weights between our neurons act as our memory. Of course the word meaning should be treated with caution here. All STDP can say about meaning is that the one presynaptic spike had an influence on the membrane potential at the postsynaptic location and thereby helped it firing. Whether this signal transport was 'in the interest of survival' or our creature or not is an entirely different question!

## The world
The world should have some basic criteria:
- Easy to implement and navigate
- Able to give attributes to places in the world (food location, shelter, obstacle, creature at place, ...)
- Updatable and fast to access (creature positions and food locations in the world should be known worldwide so that the creatures can interact with it)
I therefore propose a grid system of a world with fixed dimensions, where each attribute can be represented as a matrix overlay of the world with attribute values per grid cell.

In the world there are days. Each creature lives for a single day before it dies. Between days, the offspring is created from the previous population. For this, there needs to be some reproduction behavior in place.

## The creatures
The creatures need a brain and for that they need a neural network
- Spiking neural network for biological plausability
- List of possible sensory neurons
	- ...
- Number of computing neurons: ...
- List of possible action neurons:
	- ...
The connections should represent brain like structures with a connectivity of ~10%. Also the connectivity matrix should build the genome of the creature and it may be inherited by the child between days.
Also the creature has to have some 'reproduction chance' attribute, that is not influenced by genes or computation. Rather, it is a function of the state of the creature in the world (Found food, at shelter,...). This factor should determine the reproduction chance between days.
Later the connectivity matrix should also be adapted by some learning rule. But learning is hard, so let's first implement the rest and then worry about learning.


# Version 0.1 (24.10.2023)
In a first implementation of the project I had a lot of fun with getting into object oriented programming. The code is separated into three objects and a main function that runs the simulation.

## The world object
For the world there is now a world class, that keeps track of all the constant stuff in the simulation. For now this is the position of shelter and the position of obstacles as well as some basic paramteres like worldsize. The worldclass also knows about the initial creature population from its initialization and keeps track of the simulated days and creatures. The simulation function runs the simulation of 'n_day' days and keeps the results in the objects history. The world is the global object with which the user interacts to start the simulation and look at the results. All global plotting functions should also be funneled through the world object in the future.


# the creature object
Additionally there is a creature object that defines the creatures that interact with the world. So far they are really basic. They have a direction and each timestep they move one step into this direction if it is possible (no creature or obstacle in the way). The initial creature population is also initialized by the user. In future, everything that should be related to the behavior of the creatures (neural net, senses, cost functions, learning, etc.) should be handled within this class.

## The day object
The third object is a day. A day takes a world and a list of creatures and runs the timesteps for these creatures in this world.
It also stores the global creature position matrix per timestep in its creature history. The separation of world and day was done mainly for understandability. Everything that affects the whole simulation should be part of the world. Everything that is changing with interactions over the course of a day is stored in the history of the day object. 

## The main and config
The config file gives the user easy access to the simulation parameters.
These are then parsed as a dictionary to the main script which initializes some starting population of creatures and an empty world and runs the simulation.

## Todos for version 0.2
- [x] Create plotter for a finished simulating world

## Next step for version 0.3
- [ ] Enhance the creature abilities
    - From hard-coded directions to some neural network that may sense surroundings and derive motor tasks
    - Give creature attributes like speed and inherit these features

## outlook for version 0.x
- [ ] Introduce food to increase reproduction chance
- [ ] Introduce learning to the network (either by optimizing some cost function like energy or by unsupervised learning)

---

# Version 0.2: Introducing animations
After quite a fight with matplotlib animations and ffmpeg I finally managed to create animations for each day.
Running the 'animate_days()' function of the world will create .mp4 files for each day displaying the behavior of the creature in the world.
Each item of the world and day is handled as an imshow overlay. This will hopefully make it easy in the future to add features to the world and the animation.

With this release, we finished the build of the basic simulation environment. The next steps are to make the world and the creatures in the world more interesting.
As of now, the creatures are merely running in one fixed direction or are standing still for the whole day. The best strategy does evolve over a few days, but this can really not be called interesting behavior. So next I want the creature to be able to adapt their behavior based on some input they get. The goal for release 0.3 therefore will be to have creatures that have some network-like structure that recieves input (position in the world, if they are currently at shelter, items on neighboring fields, ...). The output of the network should then be some behavior command (move forward, turn left, turn west, stand still, ...). 
For this part I must give large credit to the author of this project https://www.youtube.com/watch?v=N3tRFayqVtk, davidrandallmiller. He proposed a very cool scheme of encoding such networks using a hexadecimal code. This code can be thought of as a hex-DNA of each creature and can therefore be easily be inherited and mutated after each day. Mutation will be a key ingredient for this next step to be successful. Without mutations we will only ever find the best strategy that was already available from the initialization of the creatures and not optimize the strategy even further. I am planning to adopt a similar gene encoding procedure for my creatures.


## Next step for version 0.3
- [ ] Enhance the creature abilities
    - Design input and output neurons
	- Create a genome code for all possible networks
	- implement network class that takes a creatures genome and state as an input and produces some output based on that.
	- Hook up networks to creature decisions
	- Inherit creature genomes after a day
	- Create genome mutations while inheritence
	- Create a visualization for all different network strategies present based on the creatuers genomes.

- [ ] Some utility stuff to make our lives easier
	- Saving simulated worlds
	- Loading simulated worlds
	- Detecting the level of simulation and resuming simulation and animation after detecting

## outlook for version 0.x
- [ ] Advanced reproduction logic (energy function that is influenced by food, speed, ... and determines the reproduction chance)
- [ ] Introduce some way of communication between creatures (pheromone emission and sensing based on some world )
- [ ] Introduce learning to the network (either by optimizing some cost function like energy or by unsupervised learning)
- [ ] Introduce different creature types (like predetor-prey behavior). Maybe this could even be implemented by only letting the creatures fight and sometimes get a reward from it. This could then evolve into different types of creatures with different strategies. 

# Version 0.2.1 - Starting to work on brains (28.10.2023)
To get towards version 0.3.0 the next step is to create brains for the creatures. The brains should be implemented as spiking networks. 
As a first iteration I will just mean by that, that we have a synaptic weight matrix and a binary vector of each time step, where the neuron state is encoded.
A one encodes a spike in the timestep. The activation function therefore also only consists of a step function. The weights are normalized to [-1,1] so that we may have inhibitory and excitatory synapses. 
TODO: Maybe I need to scale up the range to allow single neurons to have more impact.
The list of sensory neurons so far can also be found in the brain class. However the implementation is not done yet and nothing is hooked up to the creature itself.
In future I plan to let the creature only move relative to some direction in which they are facing and they have to turn to change the possible move direction.