import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import Sensor
from motor import Motor
import os

from pyrosim.neuralNetwork import NEURAL_NETWORK

class Robot():
    def __init__(self, parID, popgroup) -> None:
        # unique link identification
        self.id = p.loadURDF(f"body{popgroup}.urdf")
        # unique parallelization file identification
        self.parID = parID

        # ensure that brain{parID} exists prior to here (GenBrain called in Soln.Eval() which is called thru search -> PHC -> Soln)
        self.nn = NEURAL_NETWORK(f"brain{popgroup}.nndf")

        # pyrosim needs setup b4 using sensors
        pyrosim.Prepare_To_Simulate(self.id)    # this is link id (not parID)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
    
    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = Sensor(linkName)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.GetValue(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = Motor(jointName)


    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName.encode()].SetValue(self, desiredAngle)


    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.id,0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]

        # with open(f'fitness{str(self.parID)}.txt', 'w+') as f:
        #     f.write(str(xCoordinateOfLinkZero))

        with open(f'tmp{str(self.parID)}.txt', 'w+') as f:
            f.write(str(xCoordinateOfLinkZero))

        os.system(f"mv tmp{str(self.parID)}.txt fitness{str(self.parID)}.txt")
        
    
    def Think(self):
        self.nn.Update()