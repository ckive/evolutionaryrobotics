import numpy as np
import pyrosim.pyrosim as pyrosim
import random, os
import pybullet as p
from solution import Solution
from collections import defaultdict as dd

class SnakeSolution(Solution):
    def __init__(self) -> None:
        """
        random # of boxes, size of boxes, touch sensors
            limit to boxes, 
            randomsizes:[0.2, 2]
            random sensesensors, and motorsensors
        """
        self.numlinks = random.randint(0,10)
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
        print('l2s', self.link2sensors)

        # weights is a {tupleof(senseNname,motorNname): float} mapping
        self.weights = {}

    def _rdmsize(self, l=1, h=3, rnd=1):
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
        pyrosim.Send_Cube(name="0", size=rootlksize, pos=[0,0,rootlksize[2]/2])
        pyrosim.Send_Joint(name = "0_1" , parent= "0" , child = "1" , type = "revolute", position = [rootlksize[0]/2,0,rootlksize[2]/2])
        lksize = self._rdmsize()
        pyrosim.Send_Cube(name="1", size=lksize, pos=[lksize[0]/2,0,0])
        
        for link, sensors in self.link2sensors.items():
            pyrosim.Send_Joint(name = f"{link-1}_{link}" , parent= f"{link-1}" , child = f"{link}" , type = "revolute", position = [lksize[0],0,0])
            lksize = self._rdmsize()
            pyrosim.Send_Cube(name=str(link), pos=[lksize[0]/2,0,0] , size=lksize)

        pyrosim.End()


    def Generate_Brain(self):
        """
        create sensors and motors and generate weights for those synapses
        """
        pyrosim.Start_NeuralNetwork("brain.nndf")
        
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


        for senseNeuron in senseNnames:
            for motorNeuron in motorNnames:
                # generate the weights here
                rdm_wt = random.random()*2-1
                tuplekey = (senseNeuron, motorNeuron)
                self.weights[tuplekey] = rdm_wt
                pyrosim.Send_Synapse( sourceNeuronName = senseNeuron , targetNeuronName = motorNeuron , weight = self.weights[tuplekey] )
                
        pyrosim.End()