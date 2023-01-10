import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy as np

ITER_STEPS = 1000

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")

robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

# pyrosim needs setup b4 using sensors
pyrosim.Prepare_To_Simulate(robotId)

# storing sensor values (w/ np)
backLegSensorValues = np.zeros(ITER_STEPS)
frontLegSensorValues = np.zeros(ITER_STEPS)


for i in range(ITER_STEPS):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Link0")
    # print(backLegSensorValues[i])
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Link2")
    # print(frontLegSensorValues[i])
    time.sleep(1/10)
    # print(i)
p.disconnect()

np.save('data/f/backLegSensorValues.npy', backLegSensorValues)
np.save('data/f/frontLegSensorValues.npy', frontLegSensorValues)