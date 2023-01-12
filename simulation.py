
# from world import World
# from robot import Robot
# import pybullet as p
# import pybullet_data
# import pyrosim.pyrosim as pyrosim
# from constants import *
# import time, os
# import numpy as np

# class Simulation:
#     def __init__(self) -> None:
#         self.ITER_STEPS = ITER_STEPS

#         # connect to engine
#         physicsClient = p.connect(p.GUI)
#         p.setAdditionalSearchPath(pybullet_data.getDataPath())
#         # set gravity
#         p.setGravity(0,0,-9.8)
#         self.world = World()
#         self.robot = Robot() 
        
#     def run(self):
#         for t in range(ITER_STEPS):
#             p.stepSimulation()
#             self.robot.Sense(t)
#             self.robot.Think()
#             self.robot.Act(t)
#             time.sleep(1/200)
#             print(t)
#         # print([ssr.value for ssr in self.robot.sensors.values()])
        

#     def Save_Values(self):
#         path = "data/h"
#         os.makedirs(path, exist_ok=True)
#         for sensor_name, sensor in self.robot.sensors.items():
#             np.save(f"{path}/{sensor_name}.npy", sensor.values)
#         for motor_name, motor in self.robot.motors.items():
#             np.save(f"{path}/{sensor_name}.npy", motor.motorValues)


#     def __del__(self):
#         p.disconnect()

from world import World
from robot import Robot
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from constants import *
import time, os
import numpy as np

class Simulation:
    def __init__(self) -> None:
        self.ITER_STEPS = ITER_STEPS

        # connect to engine
        physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        # set gravity
        p.setGravity(0,0,-9.8)
        self.world = World()
        self.robot = Robot() 

    def run(self):
        for t in range(ITER_STEPS):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            time.sleep(1/5000)
            print(t)
        # print([ssr.value for ssr in self.robot.sensors.values()])
        

    def Save_Values(self):
        path = "data/h"
        os.makedirs(path, exist_ok=True)
        for sensor_name, sensor in self.robot.sensors.items():
            np.save(f"{path}/{sensor_name}.npy", sensor.values)
        for motor_name, motor in self.robot.motors.items():
            np.save(f"{path}/{sensor_name}.npy", motor.motorValues)


    def __del__(self):
        p.disconnect()