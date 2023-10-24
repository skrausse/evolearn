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
In a first implementation of the project I had a lot of fun with getting into object oriented programming.
For the world there is now a world class, that keeps track of all the constant stuff in the simulation. For now this is the position of shelter and the position of obstacles as well as some basic paramteres like worldsize.

Additionally there is a creature object that defines the creatures that interact with the world. So far they are really basic.
They have a direction and each timestep they move one step into this direction if it is possible (no creature or obstacle in the way).

The third object is a day. A day takes a world and a list of creatures and runs the timesteps for these creatures in this world.
It also stores the global creature position matrix per timestep in its creature history. The separation of world and day was done mainly for understandability. Everything that is constant over the whole simulation should be part of the world. Everything that is changing with interactions over the course of a day is stored in the history of the day object. 

Beyond this objects there is the simulation function, which creates an initial world and an initial population of creatures and runs the whole simulation.
TODO: This could maybe become part of the world class to run the simulation of the world. This way the world knows about days and creatures in the world and the only thing to handle in the end is the world object.

The parameters and simulation call are done in the main script.
TODO: Create yaml config file that handles the parameters.


## Todos for version 0.2
- [ ] Handle TODOs above
- [ ] Create plotter for a finished simulating world

## Next step for version 0.3
- [ ] Enhance the creature abilities
    - From hard-coded directions to some neural network that may sense surroundings and derive motor tasks
    - Give creature attributes like speed and inherit these features

## outlook for version 0.x
- [ ] Introduce food to increase reproduction chance
- [ ] Introduce learning to the network (either by optimizing some cost function like energy or by unsupervised learning)

