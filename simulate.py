import pybullet as p
import pybullet_data
import time

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")


for i in range(5000):
    p.stepSimulation()
    time.sleep(1/1000)
    print(i)
p.disconnect()