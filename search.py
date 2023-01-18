import os
from hillclimber import Hillclimber
from hillclimber_parallel import ParallelHillclimber

# # normal hill climber
# hc = Hillclimber()
# hc.Evolve()
# hc.Show_Best()

# parallel HC
phc = ParallelHillclimber()
phc.Evolve()
phc.Show_Best()