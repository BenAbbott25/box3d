import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

vector1 = {'coords': np.array([1, 2, 3]), 'color': 'blue'}

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d', aspect='equal')

def draw_vector(vector, ax):
    ax.quiver(0, 0, 0, vector['coords'][0], vector['coords'][1], vector['coords'][2], color=vector['color'])

def draw_box(vector, ax):
    vertices = [
        [[0, 0, 0]],
        
        [[vector['coords'][0], 0, 0],
        [0, vector['coords'][1], 0],
        [0, 0, vector['coords'][2]],],

        [[vector['coords'][0], vector['coords'][1], 0],
        [vector['coords'][0], 0, vector['coords'][2]],
        [0, vector['coords'][1], vector['coords'][2]],],

        [[vector['coords'][0], vector['coords'][1], vector['coords'][2]]]
    ]

    for i in range(len(vertices)):
        print(i)
        print(vertices[i])
        if i == 0:
            continue
        else:
            set1 = vertices[i-1]
            set2 = vertices[i]
            print(set1)
            print(set2)
            for s1 in set1:
                for s2 in set2:
                    if ((s1[0] != s2[0]) or (s1[1] != s2[1]) or (s1[2] != s2[2])) and ((s1[0] == s2[0]) or (s1[1] == s2[1]) and (s1[2] == s2[2])):
                        ax.quiver(s1[0], s1[1], s1[2], s2[0] - s1[0], s2[1] - s1[1], s2[2] - s1[2], color='red', arrow_length_ratio=0)

draw_vector(vector1, ax)
draw_box(vector1, ax)

plt.show()

