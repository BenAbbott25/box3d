import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

vector1 = {'coords': np.array([1, 1, 1]), 'color': 'blue'}

def draw_vector(vector, color):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(0, 0, 0, vector['coords'][0], vector['coords'][1], vector['coords'][2], color=color)

draw_vector(vector1, 'blue')

plt.show()

