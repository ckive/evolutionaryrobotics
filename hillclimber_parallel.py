from solution import Solution
from snake import SnakeSolution
import constants as c
import copy, os
import numpy as np
import matplotlib.pyplot as plt

class ParallelHillclimber():
    def __init__(self) -> None:
        # clear prev files (if any)
        os.system('rm body*.urdf')
        os.system('rm brain*.nndf')
        os.system('rm fitness*.txt')

        # best_fitness_history
        self.bfh = [0]

        self.nextparID = 0
        self.parents = {}
        for i in range(c.POPULATIONSIZE):
            # self.parents[i] = Solution(self.nextparID, self)
            self.parents[i] = SnakeSolution(self.nextparID, self, 0, i)
            self.nextparID += 1

        
        


    def Evolve(self):
        # call on parents
        self.Evaluate(self.parents, parent=True)

        # mutate N generations
        for gen in range(c.NUMGENS):
            self.Evolve_For_One_Generation("DIRECT")



    def Evolve_For_One_Generation(self, sim_mode):
        print("C")
        self.Spawn()
        print("D")
        self.Mutate()
        print("E")
        self.Evaluate(self.children)
        print("F")
        # exit()
        # self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for i, parent in self.parents.items():
            print(parent.popgroup)
            self.children[i] = copy.deepcopy(parent)
            print(self.children[i].popgroup)
            print("F")
            self.children[i].generation += 1
            # give children a differnt parID
            self.children[i].parID = self.nextparID
            self.nextparID += 1


    def Mutate(self):
        for child in self.children.values():
            child.Mutate()
            child.Mutate_Body()


    def Select(self):
        # select for moving towards (out of screen)
        # for i, parent in self.parents.items():
        #     if float(parent.fitness) < float(self.children[i].fitness):
        #         # succession
        #         self.parents[i] = self.children[i]

        thisgenfitness = np.zeros(c.POPULATIONSIZE)

        # select for moving into the screen (away)
        for i, parent in self.parents.items():
            if float(self.children[i].fitness) < float(parent.fitness):
                # succession
                self.parents[i] = self.children[i]
            thisgenfitness[i] = float(self.children[i].fitness)
        
        highestfitness = min(self.bfh[-1], thisgenfitness.min())
        # assuming -1th is max
        
        self.bfh.append(highestfitness)
                

    def Evaluate(self, solns, parent=False):
        for adam in solns.values():
            # adam.Start_Simulation("GUI")
            adam.Start_Simulation("DIRECT", parent=parent)

        print("A")

        for adam in solns.values():
            adam.Wait_For_Simulation_To_End()
        print("B")



    def Show_Best(self, write=False):
        pfitnesses = [float(p.fitness) for p in self.parents.values()]
        # want most negative
        argm = pfitnesses.index(min(pfitnesses))
        # want most positive
        # argm = pfitnesses.index(max(pfitnesses))
        
        self.parents[argm].Start_Simulation("GUI")
        # print('end of sim best fitness:', self.parents[argm].fitness)
        if write:
            with open('best.txt', 'w') as fp:
                fp.write(f"{argm}")
        return argm

    def Print(self):
        print('')
        for i in self.parents:
            print('parent, child fn:', self.parents[i].fitness, self.children[i].fitness)
        print('')


    def plot(self):
        # *-1 bc we're looking for furthest -x
        self.bfh = np.array(self.bfh[1:])*-1
        # np.savetxt("ftinesshistory.csv", self.bfh, delimiter=",")
        # print(self.bfh)

        plt.title(f"Fitness Curve best creature in population in each of {c.NUMGENS} generations")
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        plt.plot(range(1,c.NUMGENS+1), self.bfh)

        plt.savefig('fitnesscurve.png')
        