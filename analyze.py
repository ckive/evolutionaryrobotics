import matplotlib.pyplot as plt
import numpy as np


frontleg = np.load('data/f/frontLegSensorValues.npy')
backleg = np.load('data/f/backLegSensorValues.npy')

# plt.plot(frontleg, linewidth=5, label='front')
# plt.plot(backleg, label='front')

cycles = 1 # how many sine cycles
resolution = 100 # how many datapoints to generate

length = np.pi * 2 * cycles
my_wave = np.sin(np.arange(0, length, length / resolution)) * np.pi/4

iters = 1000

x = np.arange(0, iters)

plt.plot(my_wave)

plt.legend()
plt.show()