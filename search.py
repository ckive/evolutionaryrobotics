import os, random
import numpy as np
from hillclimber_parallel import ParallelHillclimber

# np.random.seed(8)
# random.seed(8)
for seed in range(10):
    np.random.seed(seed)
    random.seed(seed)

    # parallel HC
    phc = ParallelHillclimber()
    phc.Evolve()
    # phc.Show_Best(write=True)
    phc.plot(seed)

# make final plot