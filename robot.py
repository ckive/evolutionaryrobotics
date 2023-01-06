import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import Sensor
from motor import Motor

class Robot():
    def __init__(self) -> None:
        
        self.id = p.loadURDF("body.urdf")

        # pyrosim needs setup b4 using sensors
        pyrosim.Prepare_To_Simulate(self.id)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
    
    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = Sensor(linkName)
        print('my sensors',self.sensors)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.GetValue(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = Motor(jointName)

    def Act(self, t):
        for motor in self.motors.values():
            motor.SetValue(self, t)