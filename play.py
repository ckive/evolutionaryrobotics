
import os, sys

if len(sys.argv) < 2:
    with open("best.txt", "r") as fp:
        best = fp.read()
else:
    best = sys.argv[1]

os.system(f"/Users/dan/miniforge3/bin/python simulate.py GUI {0} {best}")
# else:
#     # sending it a path
#     seed = sys.argv[1]
#     os.system(f"/Users/dan/miniforge3/bin/python simulate.py GUI ")


