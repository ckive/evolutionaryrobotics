import numpy as np
import pyrosim.pyrosim as pyrosim
import random, os, time
import pybullet as p
import constants as c

class Solution():
    def __init__(self, parID, ptr2phc) -> None:
        self.weights = 2*np.random.rand(c.NUMSENSORNEURONS, c.NUMMOTORNEURONS)-1  #[-1,1]
        # NOTE, robot.id is robotID, solution.parID is for parallelism concept ID
        self.parID = parID
        self.ptr2phc = ptr2phc

    def Start_Simulation(self, sim_mode="DIRECT"):
        self.Generate_Body()
        self.Generate_Brain(self.parID)   # this changes since self.weights was altered
        # spawn a new process
        # silent
        os.system(f"/Users/dan/miniforge3/bin/python simulate.py {sim_mode} {str(self.parID)} &")
        # non silent
        # os.system(f"/Users/dan/miniforge3/bin/python simulate.py {sim_mode} {str(self.parID)}")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{str(self.parID)}.txt"):
            time.sleep(0.01)
        print('fitness file found')

        # read in new fitness score
        with open(f'fitness{self.parID}.txt', 'r') as f:
            self.fitness = f.read()
            print('soln fn:', self.fitness)
            # exit()
        
        # delete after reading
        os.system(f'rm fitness{self.parID}.txt')


    def Mutate(self):
        mutRow, mutCol = random.randint(0,c.NUMSENSORNEURONS-1), random.randint(0,c.NUMMOTORNEURONS-1)
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
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[1,1,1])
        pyrosim.Send_Cube(name="BackLeg", pos=[0,-0.5,0] , size=[0.2,1,0.2])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0] , size=[0.2,1,0.2])
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0,-0.5,1], jointAxis="1 0 0")
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,0.5,1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5,0,0] , size=[1,0.2,0.2])
        pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5,0,1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0,0] , size=[1.0,0.2,0.2])
        pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5,0,1], jointAxis="0 1 0")
        # Lower legs
        pyrosim.Send_Cube(name="lowerFrontLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        pyrosim.Send_Joint(name = "FrontLeg_lowerFrontLeg" , parent= "FrontLeg" , child = "lowerFrontLeg" , type = "revolute", position = [0,1,0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="lowerBackLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        pyrosim.Send_Joint(name = "BackLeg_lowerBackLeg" , parent= "BackLeg" , child = "lowerBackLeg" , type = "revolute", position = [0,-1,0], jointAxis="1 0 0")
        #
        pyrosim.Send_Cube(name="lowerLeftLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        pyrosim.Send_Joint(name = "LeftLeg_lowerLeftLeg" , parent= "LeftLeg" , child = "lowerLeftLeg" , type = "revolute", position = [-1,0,0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="lowerRightLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        pyrosim.Send_Joint(name = "RightLeg_lowerRightLeg" , parent= "RightLeg" , child = "lowerRightLeg" , type = "revolute", position = [1,0,0], jointAxis="0 1 0")

        pyrosim.End()

    def Generate_Brain(self, parID):
        ### All fully connected
        pyrosim.Start_NeuralNetwork(f"brain{parID}.nndf")
        # sensors
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "lowerFrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "lowerBackLeg")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "lowerLeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "lowerRightLeg")
        
        # motors
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 11, jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 12, jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron( name = 13 , jointName = "FrontLeg_lowerFrontLeg")
        pyrosim.Send_Motor_Neuron( name = 14 , jointName = "BackLeg_lowerBackLeg")
        pyrosim.Send_Motor_Neuron( name = 15 , jointName = "LeftLeg_lowerLeftLeg")
        pyrosim.Send_Motor_Neuron( name = 16 , jointName = "RightLeg_lowerRightLeg")
        
        for curRow in range(c.NUMSENSORNEURONS):
            for curCol in range(c.NUMMOTORNEURONS):
                pyrosim.Send_Synapse( sourceNeuronName = curRow , targetNeuronName = curCol+c.NUMSENSORNEURONS , weight = self.weights[curRow][curCol] )
        pyrosim.End()


        ### Only lower legs sensing, all joints moving
        # pyrosim.Send_Motor_Neuron( name = 0 , jointName = "Torso_BackLeg")
        # pyrosim.Send_Motor_Neuron( name = 1 , jointName = "Torso_FrontLeg")
        # pyrosim.Send_Motor_Neuron( name = 2 , jointName = "Torso_LeftLeg")
        # pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_RightLeg")

        # pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "lowerFrontLeg")
        # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "lowerBackLeg")
        # pyrosim.Send_Motor_Neuron( name = 10 , jointName = "FrontLeg_lowerFrontLeg")
        
        # pyrosim.Send_Motor_Neuron( name = 12 , jointName = "BackLeg_lowerBackLeg")
        # pyrosim.Send_Sensor_Neuron(name = 13 , linkName = "lowerLeftLeg")
        # pyrosim.Send_Motor_Neuron( name = 14 , jointName = "LeftLeg_lowerLeftLeg")
        # pyrosim.Send_Sensor_Neuron(name = 15 , linkName = "lowerRightLeg")
        # pyrosim.Send_Motor_Neuron( name = 16 , jointName = "RightLeg_lowerRightLeg")

        
        