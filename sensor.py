import numpy as np
import pyrosim.pyrosim as pyrosim
from constants import *

class Sensor():
    def __init__(self, linkName) -> None:
        self.linkName = linkName
        self.value = np.zeros(ITER_STEPS)

    def GetValue(self, t):
        self.value[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")