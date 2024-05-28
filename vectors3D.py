import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

containerVector = {'coords': np.array([4, 5, 3]), 'color': 'red'}

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d', aspect='equal', xlim=[0, 5], ylim=[0, 5], zlim=[0, 5])


def draw_vector(ax, vector, color, position = [0,0,0]):
    coords = np.add(vector, position)
    ax.quiver(position[0], position[1], position[2], coords[0], coords[1], coords[2], color=color, arrow_length_ratio=0.1)

def draw_box(ax, vector, color, position = [0,0,0]):
    vertices = [
        [[0, 0, 0]],
        
        [[vector[0], 0, 0],
        [0, vector[1], 0],
        [0, 0, vector[2]],],

        [[vector[0], vector[1], 0],
        [vector[0], 0, vector[2]],
        [0, vector[1], vector[2]],],

        [[vector[0], vector[1], vector[2]]]
    ]

    vertices = [np.add(vertex, position) for vertex in vertices]

    for i in range(len(vertices)):
        if i == 0:
            continue
        else:
            set1 = vertices[i-1]
            set2 = vertices[i]
            for s1 in set1:
                for s2 in set2:
                    if ((s1[0] != s2[0]) or (s1[1] != s2[1]) or (s1[2] != s2[2])) and ((s1[0] == s2[0]) or (s1[1] == s2[1]) and (s1[2] == s2[2])):
                        ax.quiver(s1[0], s1[1], s1[2], s2[0] - s1[0], s2[1] - s1[1], s2[2] - s1[2], color=color, arrow_length_ratio=0)

class ItemVector:
    def __init__(self, coords, color):
        self.coords = coords
        self.color = color
        self.allowed_orientations = []
        self.search_space = []

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
                draw_vector(ax, perm, self.color)
                draw_box(ax, perm, self.color)
                self.allowed_orientations.append(perm)
        self.allowed_orientations = np.unique(self.allowed_orientations, axis=0)

    def find_search_space(self, container, active_orientation_vector):
        self.search_space = []
        root_search_vector = np.array([container.coords[0] - active_orientation_vector[0], container.coords[1] - active_orientation_vector[1], container.coords[2] - active_orientation_vector[2]])

        root_extensions_large, root_extensions_small, root_extension_constrained = extend_vector(root_search_vector, active_orientation_vector)

        active_extentions = [
            {"area": [root_search_vector[0], active_orientation_vector[1], active_orientation_vector[2]], "position": [active_orientation_vector[0],0,0]},
            {"area": [active_orientation_vector[0], root_search_vector[1], active_orientation_vector[2]], "position": [0,active_orientation_vector[1],0]},
            {"area": [active_orientation_vector[0], active_orientation_vector[1], root_search_vector[2]], "position": [0,0,active_orientation_vector[2]]},
        ]

        self.search_space = [root_extensions_large, active_extentions, root_extensions_small, root_extension_constrained]

def extend_vector(root_vector, orientation_vector):

    root_extensions_large = [
        {"area": [root_vector[0] + orientation_vector[0], root_vector[1], root_vector[2] + orientation_vector[2]], "position": [0,orientation_vector[1],0]},
        {"area": [root_vector[0], root_vector[1] + orientation_vector[1], root_vector[2] + orientation_vector[2]], "position": [orientation_vector[0],0,0]},
        {"area": [root_vector[0] + orientation_vector[0], root_vector[1] + orientation_vector[1], root_vector[2]], "position": [0,0,orientation_vector[2]]},
    ]
    
    root_extensions_small = [
        {"area": [root_vector[0] + orientation_vector[0], root_vector[1], root_vector[2]], "position": [0,orientation_vector[1],orientation_vector[2]]},
        {"area": [root_vector[0], root_vector[1] + orientation_vector[1], root_vector[2]], "position": [orientation_vector[0],0,orientation_vector[2]]},
        {"area": [root_vector[0], root_vector[1], root_vector[2] + orientation_vector[2]], "position": [orientation_vector[0],orientation_vector[1],0]},
    ]

    root_extension_constrained = [
        {"area": [root_vector[0], root_vector[1], root_vector[2]], "position": [orientation_vector[0],orientation_vector[1],orientation_vector[2]]},
    ]

    return root_extensions_large, root_extensions_small, root_extension_constrained


class ContainerVector:
    def __init__(self, coords, color):
        self.coords = coords
        self.color = color


def init_vectors():
    # draw_vector(containerVector, ax)
    container = ContainerVector(containerVector['coords'], containerVector['color'])

    draw_box(ax, container.coords, container.color)
    item1 = ItemVector(np.array([1.5, 1, 3]), 'blue')
    item2 = ItemVector(np.array([2, 3, 1]), 'green')
    item3 = ItemVector(np.array([1, 2, 4]), 'yellow')
    items = [item1, item2, item3]

    for item in items:
        item.find_allowed_orientations(container, ax)
    
    return items

def init_active_item(items):

    active_item = None
    for item in items:
        if active_item is None:
            active_item = items[0]
        elif len(item.allowed_orientations) < len(active_item.allowed_orientations):
            active_item = item

    return active_item

def plot_active_item(active_item_vector, container, ax):
    draw_box(ax, active_item_vector, "black")
    draw_vector(ax, active_item_vector, "black")
    draw_box(ax, container.coords, container.color)

def plot_search_space(search_space, ax):
    draw_box(ax, search_space["area"], "blue", search_space["position"])

def reset_plot():
    plt.clf()
    ax = fig.add_subplot(111, projection='3d', aspect='equal', xlim=[0, 5], ylim=[0, 5], zlim=[0, 5])
    return ax

def explore_subspace(searchAreaType, space, container_vector, active_orientation_vector):
    subspaces = []

    if searchAreaType == 0:
        axis_vector = container_vector - space["area"]

        if axis_vector[0] != 0:
            subspaceA = {"area": [axis_vector[0], container_vector[1] - active_orientation_vector[1], container_vector[2]], "position": [0,active_orientation_vector[1],0]}
            subspaceB = {"area": [axis_vector[0], container_vector[1], container_vector[2] - active_orientation_vector[2]], "position": [0,0,active_orientation_vector[2]]}
        elif axis_vector[1] != 0:
            subspaceA = {"area": [container_vector[0] - active_orientation_vector[0], axis_vector[1], container_vector[2]], "position": [active_orientation_vector[0],0,0]}
            subspaceB = {"area": [container_vector[0], axis_vector[1], container_vector[2] - active_orientation_vector[2]], "position": [0,0,active_orientation_vector[2]]}
        elif axis_vector[2] != 0:
            subspaceA = {"area": [container_vector[0] - active_orientation_vector[0], container_vector[1], axis_vector[2]], "position": [active_orientation_vector[0],0,0]}
            subspaceB = {"area": [container_vector[0], container_vector[1] - active_orientation_vector[1], axis_vector[2]], "position": [0,active_orientation_vector[1],0]}

        return [subspaceA, subspaceB]

    elif searchAreaType == 1:
        axis_vector = space["area"] - active_orientation_vector
        if axis_vector[0] == 0 and axis_vector[1] == 0 and axis_vector[2] == 0:
            axis_vector = [2 * axis for axis in space["position"]]
            
        print("Space area: "+str(space["area"]))
        print("Active orientation vector: "+str(active_orientation_vector))
        print("Axis vector: "+str(axis_vector))

        if axis_vector[0] != 0:
            subspaceA = {"area": [container_vector[0], container_vector[1] - active_orientation_vector[1], container_vector[2]], "position": [0,active_orientation_vector[1],0]}
            subspaceB = {"area": [container_vector[0], container_vector[1], container_vector[2] - active_orientation_vector[2]], "position": [0,0,active_orientation_vector[2]]}
        elif axis_vector[1] != 0:
            subspaceA = {"area": [container_vector[0] - active_orientation_vector[0], axis_vector[1], container_vector[2]], "position": [active_orientation_vector[0],0,0]}
            subspaceB = {"area": [container_vector[0], axis_vector[1], container_vector[2] - active_orientation_vector[2]], "position": [0,0,active_orientation_vector[2]]}
        elif axis_vector[2] != 0:
            subspaceA = {"area": [container_vector[0] - active_orientation_vector[0], container_vector[1], axis_vector[2]], "position": [active_orientation_vector[0],0,0]}
            subspaceB = {"area": [container_vector[0], container_vector[1] - active_orientation_vector[1], axis_vector[2]], "position": [0,active_orientation_vector[1],0]}
        

        return [subspaceA, subspaceB]

    elif searchAreaType == 2:
        # let active = [a,b,c], container = [d,e,f]
        # searchAreaType2 includes: [d-a, e-b, f], [d-a, e, f-c] and [d, e-b, f-c]

        axis_vector = space["area"] - container_vector

        if axis_vector[0] == 0 and axis_vector[1] == 0 and axis_vector[2] == 0:
            axis_vector = [2 * axis for axis in space["position"]]

        if axis_vector[0] == 0:

            subspaceA = {"area": [container_vector[0], container_vector[1] - active_orientation_vector[1], active_orientation_vector[2]], "position": [0,0,0]}
            subspaceB = {"area": [container_vector[0], active_orientation_vector[1], container_vector[2] - active_orientation_vector[2]], "position": [0,0,0]}

            subspaceC = {"area": [container_vector[0] - active_orientation_vector[0], active_orientation_vector[1], container_vector[2]], "position": [0,0,0]}
            subspaceD = {"area": [container_vector[0] - active_orientation_vector[0], container_vector[1], active_orientation_vector[2]], "position": [0,0,0]}
            
        if axis_vector[1] == 0:
            subspaceA = {"area": [container_vector[0] - active_orientation_vector[0], container_vector[1], container_vector[2]], "position": [0,0,0]}
            subspaceB = {"area": [active_orientation_vector[0], container_vector[1], container_vector[2] - active_orientation_vector[2]], "position": [0,0,0]}

            subspaceC = {"area": [active_orientation_vector[0], container_vector[1] - active_orientation_vector[1], container_vector[2] - active_orientation_vector[2]], "position": [0,0,0]}
            subspaceD = {"area": [container_vector[0], container_vector[1] - active_orientation_vector[1], active_orientation_vector[2]], "position": [0,0,0]}

        if axis_vector[2] == 0:
            subspaceA = {"area": [container_vector[0] - active_orientation_vector[0], container_vector[1] - active_orientation_vector[1], container_vector[2]], "position": [0,0,0]}
            subspaceB = {"area": [active_orientation_vector[0], container_vector[1] - active_orientation_vector[1], container_vector[2]], "position": [0,0,0]}

            subspaceC = {"area": [container_vector[0], active_orientation_vector[1], container_vector[2] - active_orientation_vector[2]], "position": [0,0,0]}
            subspaceD = {"area": [active_orientation_vector[0], container_vector[1], container_vector[2] - active_orientation_vector[2]], "position": [0,0,0]}

        return [subspaceA, subspaceB, subspaceC, subspaceD]

    else:
        subspaces = [{"area": [0,0,0], "position": [0,0,0]}]

    return subspaces

def main():
    container = ContainerVector(containerVector['coords'], containerVector['color'])
    items = init_vectors()
    active_item = init_active_item(items)
    orientation_index = 0

    solved = False
    plt.draw()
    plt.pause(2)
    reset_plot()

    while not solved:
        if orientation_index > len(active_item.allowed_orientations) - 1:
            # print("No more orientations")
            break
        active_orientation_vector = active_item.allowed_orientations[orientation_index]
        active_item.find_search_space(container, active_orientation_vector)

        for searchAreaType in range(len(active_item.search_space)):

            for space in active_item.search_space[searchAreaType]:
                ax = reset_plot()
                plot_active_item(active_orientation_vector, container, ax)
                plot_search_space(space, ax)
                subspaces = explore_subspace(searchAreaType, space, container.coords, active_orientation_vector)
                if subspaces == "[0,0,0]":
                    plt.pause(30)

                for item in items:
                    if item != active_item:
                        for item_orientation in item.allowed_orientations:
                            # print("Item1 Orientation: "+str(item_orientation))
                            # if item < search space x,y,z draw and continue
                            if item_orientation[0] < space["area"][0] and item_orientation[1] < space["area"][1] and item_orientation[2] < space["area"][2]:
                                draw_vector(ax, item_orientation, item.color, space["position"])
                                # draw_box(ax, allowed_orientation, item.color, space["position"])

                                for subspace in subspaces:
                                    draw_box(ax, subspace["area"], "orange", subspace["position"])
                                    if searchAreaType == 2: 
                                        plt.pause(30)
                                    for item2 in items:
                                        if item2 != active_item and item2 != item:
                                            for item2_orientation in item2.allowed_orientations:
                                                if item2_orientation[0] < subspace["area"][0] and item2_orientation[1] < subspace["area"][1] and item2_orientation[2] < subspace["area"][2]:
                                                    draw_vector(ax, item2_orientation, item2.color, subspace["position"])
                                                    # draw_box(ax, allowed_orientation, item.color, space["position"])
                                                    print("Solution found")
                                                    print(f"Container: {container.coords}, Item0 Orientation: {active_orientation_vector}, Item1 Orientation: {item_orientation}, Item2 Orientation: {item2_orientation}")
                                                    print("----------------------------")

                    plt.draw()
                    plt.pause(2)
                            
                            # else:
                            #     print("No solutions found with orientation: "+str(item_orientation))

        orientation_index += 1

main()

