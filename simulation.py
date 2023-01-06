
from world import World
from robot import Robot
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from constants import *
import time

class Simulation:
    def __init__(self) -> None:
        self.ITER_STEPS = ITER_STEPS

        # connect to engine
        physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        # set gravity
        p.setGravity(0,0,-9.8)

        self.world = World()
        # self.robot = Robot()

        # pyrosim needs setup b4 using sensors
        # pyrosim.Prepare_To_Simulate(self.robot.id)

    def run(self):
        for i in range(ITER_STEPS):
            p.stepSimulation()
            # backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            # inching forward
            # pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"BackLeg_Torso", controlMode=p.POSITION_CONTROL, targetPosition=random.uniform(-np.pi/2, np.pi/2), maxForce=LEG_FORCE)
            # pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"Torso_FrontLeg", controlMode=p.POSITION_CONTROL, targetPosition=random.uniform(-np.pi/2, np.pi/2), maxForce=LEG_FORCE)
            # sway back and forth
            # pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"BackLeg_Torso", controlMode=p.POSITION_CONTROL, targetPosition=frontLegPowerWave[i], maxForce=LEG_FORCE)
            # pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"Torso_FrontLeg", controlMode=p.POSITION_CONTROL, targetPosition=-backLegPowerWave[i], maxForce=LEG_FORCE)
            time.sleep(1/100)
            print(i)
        p.disconnect()