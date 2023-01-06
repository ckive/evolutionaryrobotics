import matplotlib.pyplot as plt
import numpy as np


frontleg = np.load('data/f/frontLegSensorValues.npy')
backleg = np.load('data/f/backLegSensorValues.npy')

plt.plot(frontleg, linewidth=5, label='front')
plt.plot(backleg, label='front')
plt.legend()
plt.show()