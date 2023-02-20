# Assignment 7

This project is an assignment for a course at Northwestern University, [CS 396 Artificial Life](https://www.mccormick.northwestern.edu/computer-science/academics/courses/descriptions/396-2.html). The assignments are based on [Ludobots](https://www.reddit.com/r/ludobots) and use [pyrosim](https://github.com/jbongard/pyrosim).

## What is this?

This is a simulation of randomly shaped 3D creatures. The creatures each have a number of randomly placed sensors along their bodies which control motors placed at their joints according to random weights in their brain.

## Morphospace

Creatures consist of anywhere between 5 to 20 body segments ('links'). Each body segment is a cube with each dimension randomly ranging from 0.5 to 1.0 unit. Each successive body part can be attached to any face of the cubes in the already existing body with a joint that rotates around the x, y, or z axis. This allows for an enormously large morphospace with relatively low complexity. One glaring restriction to the morphospace of these creatures is that the joint graph must be a DAG. These creatures are not capable of having cyclic joint connections, which could have opened the door to some really interesting results.

Each link's generation is checked against the links that have been generated to ensure no spawning parts that reside within the existing structure. (See examples)

![Morphospace](body.png)

Here is an example of how a creature could be generated. The blue and green squares are body parts and the red arrows show how the body parts are connected by joints.

## Brain

The brain is a matrix of weights connecting the sensors to the joints. Each creature has sensors randomly spread throughout its body. Each sensor affects every joint in the creature. The brain can be represented as a complete bipartite graph of sensors and joints.

![Brain](brain.png)

Here the yellow circles represent sensors and the red squares represent joints.

## Example Generation
![ex1](ex1.png)

## Running the project

In the project directory, run:

`
python search.py
`

Note: you may need to point the Python binary to something different as I use miniconda's python binary path