import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import Sensor
from motor import Motor

from pyrosim.neuralNetwork import NEURAL_NETWORK

class Robot():
    def __init__(self) -> None:
        
        self.id = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK("brain.nndf")

        # pyrosim needs setup b4 using sensors
        pyrosim.Prepare_To_Simulate(self.id)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
    
    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = Sensor(linkName)
        # print('my sensors',self.sensors)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.GetValue(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = Motor(jointName)
        # print(self.motors.keys())

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                # neuronName is int, motors.key is b"torso_etc"
                self.motors[jointName.encode()].SetValue(self, desiredAngle)
                # print(neuronName)
                # print('Act Priting', neuronName, jointName, desiredAngle)

        # self.nn.Print()
        # for motor in self.motors.values():
        #     motor.SetValue(self, t)
    
    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.id, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]

        print('im children, writing my fitness:', xCoordinateOfLinkZero)
        # children should be writing over previous generations' fitness scores here
        with open('fitness.txt', 'w+') as f:
            f.write(str(xCoordinateOfLinkZero))
            # f.write(str(100000))