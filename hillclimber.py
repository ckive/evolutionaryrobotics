from solution import Solution
import constants as c
import copy

class Hillclimber():
    def __init__(self) -> None:
        self.parent = Solution()


    def Evolve(self):
        # a new brain w/ new weights must be gen'd b4 simulating (done in Eval prior to os.sys())
        self.parent.Evaluate("DIRECT")

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
        self.child.Evaluate(sim_mode)
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.parent.fitness < self.child.fitness:
            # succession
            self.parent = self.child

    def Show_Best(self):
        self.parent.Evaluate("GUI")
        print('end of sim best', self.parent.fitness)

    def Print(self):
        print('parent fn:', self.parent.fitness)
        print('child fn:', self.child.fitness)

    