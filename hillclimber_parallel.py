from solution import Solution
from snake import SnakeSolution
import constants as c
import copy, os
import numpy as np
import matplotlib.pyplot as plt

class ParallelHillclimber():
    def __init__(self) -> None:
        # clear prev files (if any)
        os.system('rm brain*.nndf')
        os.system('rm fitness*.txt')

        self.fitnesshistory = np.zeros((c.POPULATIONSIZE, c.NUMGENS+1))

        self.nextparID = 0
        self.parents = {}
        for i in range(c.POPULATIONSIZE):
            # self.parents[i] = Solution(self.nextparID, self)
            self.parents[i] = SnakeSolution(self.nextparID, self, self, 0, i)
            self.nextparID += 1

        
        


    def Evolve(self):
        # call on parents
        self.Evaluate(self.parents)

        # mutate N generations
        for gen in range(c.NUMGENS):
            if gen == 0:
                # by L89, we want to 'see' 1st mutated generation
                self.Evolve_For_One_Generation("GUI")
            else:
                self.Evolve_For_One_Generation("DIRECT")



    def Evolve_For_One_Generation(self, sim_mode):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        # exit()
        # self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for i, parent in self.parents.items():
            self.children[i] = copy.deepcopy(parent)
            self.children[i].generation += 1
            # give children a differnt parID
            self.children[i].parID = self.nextparID
            self.nextparID += 1


    def Mutate(self):
        for child in self.children.values():
            child.Mutate()


    def Select(self):
        # select for moving towards (out of screen)
        # for i, parent in self.parents.items():
        #     if float(parent.fitness) < float(self.children[i].fitness):
        #         # succession
        #         self.parents[i] = self.children[i]

        # select for moving into the screen (away)
        for i, parent in self.parents.items():
            if float(self.children[i].fitness) < float(parent.fitness):
                # succession
                self.parents[i] = self.children[i]
                

    def Evaluate(self, solns):
        # make sure solns is the whole dict

        # evaluating all children in parallel
        # adam bc first generation
        for adam in solns.values():
            # print('evaluating!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # adam.Start_Simulation("GUI")
            adam.Start_Simulation("DIRECT")

        for adam in solns.values():
            # print('collecting.............................................')
            adam.Wait_For_Simulation_To_End()
            # print('adam fitness:', adam.fitness)



    def Show_Best(self):
        pfitnesses = [float(p.fitness) for p in self.parents.values()]
        # want most negative
        argm = pfitnesses.index(min(pfitnesses))
        # want most positive
        # argm = pfitnesses.index(max(pfitnesses))
        self.parents[argm].Start_Simulation("GUI")
        # print('end of sim best fitness:', self.parents[argm].fitness)

    def Print(self):
        print('')
        for i in self.parents:
            print('parent, child fn:', self.parents[i].fitness, self.children[i].fitness)
        print('')


    def plot(self):
        plt.title(f"Fitness Curve best creature in population in each of {c.NUMGENS} generations")
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        # plt.plot(range(c.NUMGENS+1), np.max(self.fitnesshistory, axis=0))
        for i, popgroup_fitnesshistory in enumerate(self.fitnesshistory):
            plt.plot(range(c.NUMGENS+1), popgroup_fitnesshistory, label=f"pop_group_{i}")
        plt.legend()
        plt.savefig('fitnesscurve.png')
        