# import pybullet as p
# import pybullet_data
# import pyrosim.pyrosim as pyrosim
# import time, random
# import numpy as np
import time, sys
from simulation import Simulation

# cli 
directOrGUI = sys.argv[1]

sim = Simulation(directOrGUI)
sim.run()
sim.Get_Fitness()