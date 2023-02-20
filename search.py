import os
from hillclimber_parallel import ParallelHillclimber

# parallel HC
phc = ParallelHillclimber()
phc.Evolve()
phc.Show_Best()