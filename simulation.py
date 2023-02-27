from world import World
from robot import Robot
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from constants import *
import time, os
import numpy as np

class Simulation:
    def __init__(self, sim_mode, parID, popgroup) -> None:
        self.ITER_STEPS = ITER_STEPS
        # connect to engine

        self.sim_mode = p.GUI if sim_mode == "GUI" else p.DIRECT
        physicsClient = p.connect(self.sim_mode)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        # set gravity
        p.setGravity(0,0,-9.8)
        self.world = World()

        # before entering into robot, should first generate the robot brain{parID} file (located in solution)
        self.robot = Robot(parID, popgroup) 

    def run(self):
        for t in range(ITER_STEPS):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            if self.sim_mode == p.GUI:
                # slow it down for viewing
                time.sleep(1/200)
            # print(t)
        

    def Save_Values(self):
        path = "data/h"
        os.makedirs(path, exist_ok=True)
        for sensor_name, sensor in self.robot.sensors.items():
            np.save(f"{path}/{sensor_name}.npy", sensor.values)
        for motor_name, motor in self.robot.motors.items():
            np.save(f"{path}/{sensor_name}.npy", motor.motorValues)

    def Get_Fitness(self):
        self.robot.Get_Fitness()


    def __del__(self):
        p.disconnect()