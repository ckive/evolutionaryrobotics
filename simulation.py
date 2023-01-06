
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
            self.robot.Act(t)
            # backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            
            # inching forward
            # pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"BackLeg_Torso", controlMode=p.POSITION_CONTROL, targetPosition=random.uniform(-np.pi/2, np.pi/2), maxForce=LEG_FORCE)
            # pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"Torso_FrontLeg", controlMode=p.POSITION_CONTROL, targetPosition=random.uniform(-np.pi/2, np.pi/2), maxForce=LEG_FORCE)
            
            # sway back and forth
            # pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"BackLeg_Torso", controlMode=p.POSITION_CONTROL, targetPosition=frontLegPowerWave[i], maxForce=LEG_FORCE)
            # pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"Torso_FrontLeg", controlMode=p.POSITION_CONTROL, targetPosition=-backLegPowerWave[i], maxForce=LEG_FORCE)
            time.sleep(1/1000)
            print(t)
        print([ssr.value for ssr in self.robot.sensors.values()])

    def Save_Values(self):
        path = "data/h"
        os.makedirs(path, exist_ok=True)
        for sensor_name, sensor in self.robot.sensors.items():
            np.save(f"{path}/{sensor_name}.npy", sensor.values)
        for motor_name, motor in self.robot.motors.items():
            np.save(f"{path}/{sensor_name}.npy", motor.motorValues)


    def __del__(self):
        p.disconnect()