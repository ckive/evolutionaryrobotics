import numpy as np
import pyrosim.pyrosim as pyrosim
import random, os, time
import pybullet as p

class Solution():
    def __init__(self, parID, ptr2phc, phcObj, gen, popgroup) -> None:
        self.weights = 2*np.random.rand(3,2)-1  #[-1,1]
        # NOTE, robot.id is robotID, solution.parID is for parallelism concept ID
        self.parID = parID
        self.ptr2phc = ptr2phc
        self.phcObj = phcObj
        self.generation = gen
        self.popgroup = popgroup

    def Start_Simulation(self, sim_mode="DIRECT"):
        self.Generate_Brain(self.parID)   # this changes since self.weights was altered
        # spawn a new process
        # silent
        os.system(f"/Users/dan/miniforge3/bin/python simulate.py {sim_mode} {str(self.parID)} &")
        # non silent
        # os.system(f"/Users/dan/miniforge3/bin/python simulate.py {sim_mode} {str(self.parID)}")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{str(self.parID)}.txt"):
            time.sleep(0.01)

        # read in new fitness score
        with open(f'fitness{self.parID}.txt', 'r') as f:
            self.fitness = f.read()
            # add into phcObj for tracking and plotting 
            self.phcObj.fitnesshistory[self.popgroup][self.generation] = self.fitness
            # exit()
        
        # delete after reading
        os.system(f'rm fitness{self.parID}.txt')


    def Mutate(self):
        mutRow, mutCol = random.randint(0,2), random.randint(0,1)
        self.weights[mutRow][mutCol] = random.random()*2-1

    def Set_ID(self):
        # updates PHC's self.nextID for every children we spawn
        self.ptr2phc.nextparID += 1


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


    def Generate_Brain(self, parID):
        pyrosim.Start_NeuralNetwork(f"brain{parID}.nndf")
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