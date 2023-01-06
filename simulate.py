import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time, random
import numpy as np

import matplotlib.pyplot as plt


ITER_STEPS = 1000
LEG_FORCE = 30

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

def create_wave(N, freq=1, amp=1, shift=0):
    t = np.linspace(0,N,N)
    w = (2*np.pi)*freq/N #2pif/N
    signal = amp*np.sin(w*t + shift)
    return t, signal

# x_wave, my_wave = create_wave(ITER_STEPS,freq=10)
# plt.plot(x_wave,my_wave)
# plt.show()
# exit()

x1, frontLegPowerWave = create_wave(ITER_STEPS,freq=10)
x2, backLegPowerWave = create_wave(ITER_STEPS,freq=5,shift=np.pi/2)




for i in range(ITER_STEPS):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    # inching forward
    # pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"BackLeg_Torso", controlMode=p.POSITION_CONTROL, targetPosition=random.uniform(-np.pi/2, np.pi/2), maxForce=LEG_FORCE)
    # pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"Torso_FrontLeg", controlMode=p.POSITION_CONTROL, targetPosition=random.uniform(-np.pi/2, np.pi/2), maxForce=LEG_FORCE)
    # sway back and forth
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"BackLeg_Torso", controlMode=p.POSITION_CONTROL, targetPosition=frontLegPowerWave[i], maxForce=LEG_FORCE)
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b"Torso_FrontLeg", controlMode=p.POSITION_CONTROL, targetPosition=-backLegPowerWave[i], maxForce=LEG_FORCE)
    time.sleep(1/100)
    print(i)
p.disconnect()

np.save('data/f/backLegSensorValues.npy', backLegSensorValues)
np.save('data/f/frontLegSensorValues.npy', frontLegSensorValues)