import numpy as np
import pyrosim.pyrosim as pyrosim
import random, os
import pybullet as p

class Solution():
    def __init__(self) -> None:
        self.weights = 2*np.random.rand(3,2)-1  #[-1,1]


    def Evaluate(self, sim_mode="DIRECT"):
        # should prob regen the brain here?
        self.CreateWorld()      # no change here really
        self.Generate_Body()    # no change here really
        print("gen'd body")
        # exit()
        self.Generate_Brain()   # this changes since self.weights was altered
        os.system(f"/Users/dan/miniforge3/bin/python simulate.py {sim_mode}")

        # read in new fitness score
        with open('fitness.txt', 'r') as f:
            self.fitness = f.read()
            # print('soln fn:', self.fitness)

    def Mutate(self):
        mutRow, mutCol = random.randint(0,2), random.randint(0,1)
        self.weights[mutRow][mutCol] = random.random()*2-1



    def CreateWorld(self):
        pyrosim.Start_SDF("world.sdf")
        # pyrosim.Send_Cube(name="Box", pos=[0,0,0.5] , size=[1,1,1])
        pyrosim.Send_Cube(name="Box", pos=[10,10,0.5] , size=[1,1,1])
        pyrosim.End()


    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[1,1,1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5] , size=[1,1,1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5] , size=[1,1,1])
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1])
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1])
        pyrosim.End()


    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

        # K rdmsrch 
        for curRow in [0,1,2]:
            for curCol in [0,1]:
                pyrosim.Send_Synapse( sourceNeuronName = curRow , targetNeuronName = curCol+3 , weight = self.weights[curRow][curCol] )
        pyrosim.End()