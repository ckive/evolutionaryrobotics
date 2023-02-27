import os, random
import numpy as np
from hillclimber_parallel import ParallelHillclimber

np.random.seed(0)
random.seed(0)

# parallel HC
phc = ParallelHillclimber()
phc.Evolve()
phc.Show_Best(write=True)
phc.plot()

