import pyrosim.pyrosim as pyrosim
import random, os
import pybullet as p
from solution import Solution
from collections import defaultdict as dd

def add_list(l1, l2):
    # does np list adding
    return [sum(x) for x in zip(l1, l2)]

class Box:
    def __init__(self, name, size, parbox, direc, sensors, myabsposn=[0,0,0]) -> None:
        # spawning post collision check
        self.name = name
        self.size = size
        self.sensors = sensors
        self.parbox = parbox

        if "none" in sensors:
            # blue
            color = [0,0,1,1]
        else:
            # green
            color = [0,1,0,1]
        
        if direc == 0:
            # root link
            self.abspos = [0,0,self.size[2]/2]
            self.relpos = [0,0,self.size[2]/2]      # relpos is to link
            # maybe [0,0,0] here
            self.jointpos = [0,0,0]
            pyrosim.Send_Cube(name="0", size=self.size, pos=self.abspos, rgba=color)
        else:
            negative = -1 if direc < 0 else 1
            axis = abs(direc)
            # joint_pos = parbox.relpos += dir halfsize
            
            joint_pos = parbox.relpos.copy()
            if axis == 1:
                joint_pos[0] += negative*parbox.size[0]/2
                self.relpos = [negative*self.size[0]/2, 0, 0]

            elif axis == 2:
                joint_pos[1] += negative*parbox.size[1]/2
                self.relpos = [0, negative*self.size[1]/2, 0]
            else:
                joint_pos[2] += negative*parbox.size[2]/2
                self.relpos = [0, 0, negative*self.size[2]/2]

            # self.abspos = add_list(joint_pos, self.relpos)
            self.abspos = myabsposn
            
            jA = random.choice(["0 1 0", "1 0 0", "0 0 1"])
            pyrosim.Send_Joint(
                name = f"{parbox.name}_{self.name}" , parent= f"{parbox.name}" , 
                child = f"{self.name}" , type = "revolute", position = joint_pos, jointAxis=jA)    # axis of rotation...

            pyrosim.Send_Cube(name=self.name, size=self.size, pos=self.relpos, rgba=color)
    
    def get_abspos(self):
        return self.abspos.copy()


    def collide(self, newboxsize, newboxposn) -> bool:
        # returns T if collides with me else False
        # https://stackoverflow.com/questions/5009526/overlapping-cubes
        # Determining overlap in the x plane
        c1 = self.abspos[0]+self.size[0]/2 > newboxposn[0]-newboxsize[0]/2
        c2 = self.abspos[0]-self.size[0]/2 < newboxposn[0]+newboxsize[0]/2
        # Determining overlap in the y plane
        c3 = self.abspos[1]+self.size[1]/2 > newboxposn[1]-newboxsize[1]/2
        c4 = self.abspos[1]-self.size[1]/2 < newboxposn[1]+newboxsize[1]/2
        # Determining overlap in the z plane
        c5 = self.abspos[2]+self.size[2]/2 > newboxposn[2]-newboxsize[2]/2
        c6 = self.abspos[2]-self.size[2]/2 < newboxposn[2]+newboxsize[2]/2

        return c1 and c2 and c3 and c4 and c5 and c6 

    


class SnakeSolution(Solution):
    def __init__(self, parID, gen, popgroup) -> None:
        """
        random # of boxes, size of boxes, touch sensors
            limit to boxes, 
            randomsizes:
            random sensesensors, and motorsensors
        """
        self.parID = parID
        # self.ptr2phc = ptr2phc
        self.generation = gen
        self.popgroup = popgroup

        self.numlinks = random.randint(5,15)
        # self.numlinks = 15
        # mp of link(int): sensors (listof(strs))
        self.link2sensors = dd(list)
        for i in range(0, self.numlinks):
            if i == 0:
                # don't allow root node to have motor
                self.link2sensors[i] = ['none']
                continue
            if random.randint(0,1):
                # add a sense sensor to link
                self.link2sensors[i] += ['sense']
            if random.randint(0,1):
                # add a motor sensor to link
                self.link2sensors[i] += ['motor']
            if i not in self.link2sensors:
                self.link2sensors[i] = ['none']

        # weights is a {tupleof(senseNname,motorNname): float} mapping
        self.weights = {}

        # Generate the Body here, all descendents come from the same body, parents have different bodies?
        self.Generate_Body(popgroup)
        # exit()

    

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


    def _rdmsize(self, l=0.5, h=1, rnd=1):
        # generates rndmsizes from l to h, sounded to rnd decimals
        return [round(random.uniform(l, h), rnd),round(random.uniform(l, h), rnd),round(random.uniform(l, h), rnd)]

    def spawn_next_link(self, linkname, sensors) -> None:
        """
        randomly chooses
            parent from realcubes
            cubesize
            direction
        until spawnable, spawns the box via instantiating Box()
        """
        spawnable = False
        while not spawnable:
            parent_name, parent_Box = random.choice(list(self.realcubes.items()))
            lksize = self._rdmsize()
            #1:x, 2:y, 3:z with corresponding negatives
            direction = random.choice([-1,1,-2,2,-3,3])
            # calc newbox_absposn -> parentbox in given direction + lksize
            axis = abs(direction)
            negative = -1 if direction < 0 else 1
            newbox_absposn = parent_Box.get_abspos()
            # if axis == 1: #x
            #     newbox_absposn[0] += parent_Box.size[0]/2 + negative*lksize[0]/2
            # elif axis == 2: #y
            #     newbox_absposn[1] += parent_Box.size[1]/2 + negative*lksize[1]/2
            # else: #z
            #     newbox_absposn[2] += parent_Box.size[2]/2 + negative*lksize[2]/2

            if axis == 1: #x
                newbox_absposn[0] += negative*(parent_Box.size[0]/2 + lksize[0]/2)
            elif axis == 2: #y
                newbox_absposn[1] += negative*(parent_Box.size[1]/2 + lksize[1]/2)
            else: #z
                newbox_absposn[2] += negative*(parent_Box.size[2]/2 + lksize[2]/2)
    
            spawnable = not self.collides_with_others(lksize, newbox_absposn) 
        # spawnable now
        newlink = Box(linkname, lksize, parent_Box, direction, sensors, newbox_absposn)
        self.realcubes[linkname] = newlink
        return

    def collides_with_others(self, newboxsize, newboxposn) -> bool:
        # goes thru list of spawned boxes and checks if box hits it
        if newboxposn[2]-newboxsize[2]/2 < 0:
            return True
        for realbox in self.realcubes.values():
            if realbox.collide(newboxsize, newboxposn):
                return True
        return False

    def Generate_Body(self, popgroup, mut=False):
        """
        generate like madman
        """
        # stores true spawned cubes (used for picking spawn point of next cube)
        # name: (size, absposition)
        self.realcubes = {}

        pyrosim.Start_URDF(f"body{popgroup}.urdf")
       
        
        for link, sensors in self.link2sensors.items():
            linkname = str(link)
            if link == 0:
                # generate root link
                self.realcubes[linkname] = Box(linkname, self._rdmsize(), None, 0, sensors)
            else:
                # subsequent links
                self.spawn_next_link(linkname, sensors)
        
        pyrosim.End()

    def _Mutate_Body(self, popgroup, p=0.5):
        if not random.choice(p):
            return
        # otherwise, mutate leaf parts
        ln, ll = self.realcubes.items()[-1]
        parboxes = [pb.parbox for pb in self.realcubes.values()]
        lfnodes = [ln for ln in self.realcubes.values() if ln not in parboxes]
        ln = random.choice(lfnodes)
        todeljt = []
        for jt in self.weights.keys():
            if ln in jt:
                todeljt.append(jt)

        for jt in todeljt:
            del self.weights[jt]
        
        # flush
        self.Write_Brain(popgroup)

        self.Generate_Body(popgroup, mut=True)




    def Write_Brain(self, popgroup, generate=False):
        """
        create sensors and motors and generate weights for those synapses
        Creates brain only done at beginning of a popgroup
        Mutates brain at subsequent calls
        """
        pyrosim.Start_NeuralNetwork(f"brain{popgroup}.nndf")
        
        senseNnames = []
        motorNnames = []
        for link, box in self.realcubes.items():
            for s in box.sensors:
                if s == 'sense':
                    pyrosim.Send_Sensor_Neuron(name = f"{link}_sense" , linkName = str(link))
                    senseNnames.append(f"{link}_sense")
                elif s == 'motor':
                    pyrosim.Send_Motor_Neuron( name = f"{box.parbox.name}_{box.name}_motor" , jointName = f"{box.parbox.name}_{box.name}")
                    motorNnames.append(f"{box.parbox.name}_{box.name}_motor")

        # to run phc, must ensure there are things to mutate upon (must have synapses ==> must have sense AND motors)
        # if no sensors or motors, create a motor of last 2 links
        if not senseNnames:
            pyrosim.Send_Sensor_Neuron(name = f"{link}_sense" , linkName = str(link))
            senseNnames.append(f"{link}_sense")
        if not motorNnames:
            pyrosim.Send_Motor_Neuron( name = f"{box.parbox.name}_{box.name}_motor" , jointName = f"{box.parbox.name}_{box.name}")
            motorNnames.append(f"{box.parbox.name}_{box.name}_motor")

        for senseNeuron in senseNnames:
            for motorNeuron in motorNnames:
                tuplekey = (senseNeuron, motorNeuron)
                if generate:
                    # generate the weights here
                    rdm_wt = random.random()*2-1
                    self.weights[tuplekey] = rdm_wt
                
                # otherwise, write weights into file based on mutation in self.weights
                pyrosim.Send_Synapse( sourceNeuronName = senseNeuron , targetNeuronName = motorNeuron , weight = self.weights[tuplekey] )
                
        pyrosim.End()

    def Mutate_Body(self):
        # self._Mutate_Body()
        return