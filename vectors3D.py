import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

containerVector = {'coords': np.array([4, 5, 3]), 'color': 'red'}

item1 = {'coords': np.array([1.5, 1.5, 3]), 'color': 'blue'}
item2 = {'coords': np.array([2, 3, 1]), 'color': 'green'}
item3 = {'coords': np.array([1, 2, 4]), 'color': 'yellow'}

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d', aspect='equal')

class ItemVector:
    def __init__(self, coords, color):
        self.coords = coords
        self.color = color
        self.allowed_orientations = []

    def draw_vector(self, ax):
        ax.quiver(0, 0, 0, self.coords[0], self.coords[1], self.coords[2], color=self.color, arrow_length_ratio=0.1)

    def find_allowed_orientations(self, container, ax):

        item_permutations = np.array([[self.coords[0], self.coords[1], self.coords[2]],
                                    [self.coords[0], self.coords[2], self.coords[1]],
                                    [self.coords[1], self.coords[0], self.coords[2]],
                                    [self.coords[1], self.coords[2], self.coords[0]],
                                    [self.coords[2], self.coords[0], self.coords[1]],
                                    [self.coords[2], self.coords[1], self.coords[0]]])

        for perm in item_permutations:
            if perm[0] < container.coords[0] and perm[1] < container.coords[1] and perm[2] < container.coords[2]:
                vec = ItemVector(perm, self.color)
                vec.draw_vector(ax)
                vac = ContainerVector(perm, self.color)
                vac.draw_box(ax)
                self.allowed_orientations.append(perm)


class ContainerVector:
    def __init__(self, coords, color):
        self.coords = coords
        self.color = color

    def draw_box(self, ax):
        vertices = [
            [[0, 0, 0]],
            
            [[self.coords[0], 0, 0],
            [0, self.coords[1], 0],
            [0, 0, self.coords[2]],],

            [[self.coords[0], self.coords[1], 0],
            [self.coords[0], 0, self.coords[2]],
            [0, self.coords[1], self.coords[2]],],

            [[self.coords[0], self.coords[1], self.coords[2]]]
        ]

        for i in range(len(vertices)):
            if i == 0:
                continue
            else:
                set1 = vertices[i-1]
                set2 = vertices[i]
                for s1 in set1:
                    for s2 in set2:
                        if ((s1[0] != s2[0]) or (s1[1] != s2[1]) or (s1[2] != s2[2])) and ((s1[0] == s2[0]) or (s1[1] == s2[1]) and (s1[2] == s2[2])):
                            ax.quiver(s1[0], s1[1], s1[2], s2[0] - s1[0], s2[1] - s1[1], s2[2] - s1[2], color=self.color, arrow_length_ratio=0)


class ActiveVector:
    def __init__(self, item, allowed_orientations):
        self.item = item
        self.allowed_orientations = allowed_orientations


# draw_vector(containerVector, ax)
container = ContainerVector(containerVector['coords'], containerVector['color'])
container.draw_box(ax)

item1 = ItemVector(item1['coords'], item1['color'])
item2 = ItemVector(item2['coords'], item2['color'])
item3 = ItemVector(item3['coords'], item3['color'])

item1.find_allowed_orientations(container, ax)
item2.find_allowed_orientations(container, ax)
item3.find_allowed_orientations(container, ax)

active_vector = ActiveVector(item1, np.zeros(10))

for item in [item1, item2, item3]:
    if len(item.allowed_orientations) < len(active_vector.allowed_orientations):
        active_vector = ActiveVector(item, item.allowed_orientations)

print(active_vector)
print(active_vector.item.color)
print(active_vector.allowed_orientations)
print(len(active_vector.allowed_orientations))

plt.show()

