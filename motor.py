import numpy as np
import pybullet as p
import pyrosim.pyrosim as pyrosim
from constants import *
import random

class Motor():
    def __init__(self, jointName) -> None:
        self.jointName = jointName
        self.amplitude, self.frequency, self.phaseshift = 1,10,0

        if self.jointName == b'BackLeg_Torso':
            self.frequency /= 2

        _, self.motorValues = self._create_wave(ITER_STEPS, self.frequency, self.amplitude, self.phaseshift)
        print('motor done')

    def _create_wave(self, N, freq=1, amp=1, shift=0):
        t = np.linspace(0,N,N)
        w = (2*np.pi)*freq/N #2pif/N
        signal = amp*np.sin(w*t + shift)
        return t, signal

    def SetValue(self, robot, t):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot.id, 
            jointName=self.jointName,   #.encode(),  # cuz needed byte string for some reason
            controlMode=p.POSITION_CONTROL, 
            targetPosition=self.motorValues[t], 
            maxForce=LEG_FORCE
            )