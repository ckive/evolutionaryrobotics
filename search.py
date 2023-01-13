import os
from hillclimber import Hillclimber

# for _ in range(5):
#     os.system("/Users/dan/miniforge3/bin/python generate.py")
#     os.system("/Users/dan/miniforge3/bin/python simulate.py")

hc = Hillclimber()
hc.Evolve()