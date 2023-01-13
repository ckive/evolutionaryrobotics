from solution import Solution
import copy, random
import constants as c 

class Hillclimber():
    def __init__(self) -> None:
        self.parent = Solution()

    def Evolve(self):
        self.parent.Evaluate()
        with open('fitness.txt', 'r') as f:
            fn = f.read()
        print('contents of fitness before evolution', fn)
        # exit()
        for curGen in range(c.NUMGENS):
            self.Evolve_For_One_Generation()


    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        pre = self.child.weights.copy()
        print('premutate child weights', pre)
        self.child.Mutate()
        post = self.child.weights
        print('postmutate child weights', post)
        if (pre == post).all():
            exit()

    def Select(self):
        if self.parent.fitness < self.child.fitness:
            # succession
            print('evolution!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            exit()
            self.parent = self.child

    
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate()
        self.Print()

        self.Select()

    def Print(self):
        print('fitness p,c:', self.parent.fitness, self.child.fitness)