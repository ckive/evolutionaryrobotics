import numpy as np
import pyrosim.pyrosim as pyrosim
import random, os
import pybullet as p
from solution import Solution
from collections import defaultdict as dd

class SnakeSolution(Solution):
    def __init__(self, parID, ptr2phc) -> None:
        """
        random # of boxes, size of boxes, touch sensors
            limit to boxes, 
            randomsizes:[0.2, 2]
            random sensesensors, and motorsensors
        """
        self.parID = parID
        self.ptr2phc = ptr2phc

        # it is 2 + numlinks links
        # self.numlinks = random.randint(0,10)
        self.numlinks = 5
        # mp of link(int): sensors (listof(strs))
        self.link2sensors = dd(list)
        for i in range(2, self.numlinks+2):
            # note start at 2 bc we make first 2 permanent
            if random.randint(0,1):
                # add a sense sensor to link
                self.link2sensors[i] += ['sense']
            if random.randint(0,1):
                # add a motor sensor to link
                self.link2sensors[i] += ['motor']
            if i not in self.link2sensors:
                self.link2sensors[i] = ['none']
        # print('l2s', self.link2sensors)

        # weights is a {tupleof(senseNname,motorNname): float} mapping
        self.weights = {}

        # Generate the Body here, all descendents come from the same body, parents have different bodies?
        self.Generate_Body()
        # exit()

    def _rdmsize(self, l=0.5, h=1, rnd=1):
        # generates rndmsizes from l to h, sounded to rnd decimals
        return [round(random.uniform(l, h), rnd),round(random.uniform(l, h), rnd),round(random.uniform(l, h), rnd)]

    """
    Inherits these

    .Evaluate()
    .Mutate()       <- we change this
    .CreateWorld()
    """

    def Mutate(self):
        # randomly choose one of the keys to mutate its value
        mutatekey = random.choice(list(self.weights))
        self.weights[mutatekey] = random.random()*2-1


    def Generate_Body(self):
        """
        only generate to +x direction
        """
        pyrosim.Start_URDF("body.urdf")
        # manually add a root link and 2nd link starting at 0,0 with random size (placed above ground)
        # 2nd one needed bc need a root joint
        rootlksize = self._rdmsize()
        pyrosim.Send_Cube(name="0", size=rootlksize, pos=[0,0,rootlksize[2]/2], rgba=[0,1,0,1])
        pyrosim.Send_Joint(name = "0_1" , parent= "0" , child = "1" , type = "revolute", position = [rootlksize[0]/2,0,rootlksize[2]/2])
        lksize = self._rdmsize()
        pyrosim.Send_Cube(name="1", size=lksize, pos=[lksize[0]/2,0,0], rgba=[0,1,0,1])
        
        
        #0:x, 1:y, 2:z
        lastdir = 0
        
        for link, sensors in self.link2sensors.items():
            # only grows in positive x,y,z
            # randomly pick a direction
            direction = random.randint(0,2)
            
            #xy
            if lastdir == 0 and direction == 1:
                joint_pos = [lksize[0]/2,lksize[1]/2,0]
            #xz
            elif lastdir == 0 and direction == 2:
                joint_pos = [lksize[0]/2,0,lksize[2]/2]
            #yx
            elif lastdir == 1 and direction == 0:
                joint_pos = [lksize[0]/2,lksize[1]/2,0]
            #yz
            elif lastdir == 1 and direction == 2:
                joint_pos = [0,lksize[1]/2,lksize[2]/2]
            #zx
            elif lastdir == 2 and direction == 0:
                joint_pos = [lksize[0]/2,0,lksize[2]/2]
            #zy
            elif lastdir == 2 and direction == 1:
                joint_pos = [0,lksize[1]/2,lksize[2]/2]
            # continue in same dir
            else:
                joint_pos = [0,0,0]
                joint_pos[direction] = lksize[direction]

            # choose a random axis of rotation

            jA = random.choice(["0 1 0", "1 0 0", "0 0 1"])

            # # jointAxis: NO TWISTING, choose 1 of 2
            # if direction == 0:
            #     # choose between 0,1,0 and 
            #     jA = "0 1 0"
            # elif direction == 1:
            #     jA = "1 0 0"
            # else:
            #     jA = "0 0 1"
            
            pyrosim.Send_Joint(
                name = f"{link-1}_{link}" , parent= f"{link-1}" , 
                child = f"{link}" , type = "revolute", position = joint_pos, jointAxis=jA)    # axis of rotation...

            """
            REMEMBER
            basically whichever axis has 1 is the fixed axis
            0,1,0           y doesnt change, swings on x,z      (original leg)
            1,0,0           x doesnt change, swings on y,z      (wings flapping)
            0,0,1           z doesnt change, swings on x,y      (head shake side2side, sweeping)
            
            
            """
            
            lksize = self._rdmsize()
            link_pos = [0,0,0]
            link_pos[direction] = lksize[direction]/2

            # pyrosim.Send_Cube(name=str(link), pos=link_pos , size=lksize)

            # check for sensors and color it
            if "none" in sensors:
                # blue
                color = [0,0,1,1]
            else:
                # green
                color = [0,1,0,1]
            pyrosim.Send_Cube(name=str(link), pos=link_pos , size=lksize, rgba=color)
            
            lastdir = direction
        pyrosim.End()


    def Generate_Brain(self, parID):
        """
        create sensors and motors and generate weights for those synapses
        """
        pyrosim.Start_NeuralNetwork(f"brain{parID}.nndf")
        
        senseNnames = []
        motorNnames = []
        for link, sensors in self.link2sensors.items():
            for s in sensors:
                if s == 'sense':
                    pyrosim.Send_Sensor_Neuron(name = f"{link}_sense" , linkName = str(link))
                    senseNnames.append(f"{link}_sense")
                elif s == 'motor':
                    # assume its the one that connects to the link'th link
                    pyrosim.Send_Motor_Neuron( name = f"{link-1}_{link}_motor" , jointName = f"{link-1}_{link}")
                    motorNnames.append(f"{link-1}_{link}_motor")

        # to run phc, must ensure there are things to mutate upon (must have synapses ==> must have sense AND motors)
        # if no sensors or motors, create a motor of last 2 links
        if not senseNnames:
            pyrosim.Send_Sensor_Neuron(name = f"{link}_sense" , linkName = str(link))
            senseNnames.append(f"{link}_sense")
        if not motorNnames:
            pyrosim.Send_Motor_Neuron( name = f"{link-1}_{link}_motor" , jointName = f"{link-1}_{link}")
            motorNnames.append(f"{link-1}_{link}_motor")

        for senseNeuron in senseNnames:
            for motorNeuron in motorNnames:
                # generate the weights here
                rdm_wt = random.random()*2-1
                tuplekey = (senseNeuron, motorNeuron)
                self.weights[tuplekey] = rdm_wt
                pyrosim.Send_Synapse( sourceNeuronName = senseNeuron , targetNeuronName = motorNeuron , weight = self.weights[tuplekey] )
                
        pyrosim.End()