
import os

with open("best.txt", "r") as fp:
    best = fp.read()

os.system(f"/Users/dan/miniforge3/bin/python simulate.py GUI {0} {0}")
