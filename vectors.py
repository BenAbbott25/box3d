import matplotlib.pyplot as plt
import numpy as np

def draw_vector(coords: list[np.array], color: str = 'black', fill: bool = False):
    plt.quiver(0, 0, coords[0], coords[1], angles='xy', scale_units='xy', scale=1, color=color)
    if fill:
        plt.fill([0, 0, coords[0], coords[0]], [0, coords[1], coords[1], 0], color=color, alpha=0.2)

container = {'coords': np.array([4, 3]), 'color': 'black', 'fill': True}
box1 = {'coords': np.array([3.5, 1.5]), 'color': 'blue'}
box1_inverse = {'coords': np.array([1.5, 3.5]), 'color': 'blue'}
box2 = {'coords': np.array([3, 1.5]), 'color': 'green'}
box2_inverse = {'coords': np.array([1.5, 3]), 'color': 'green'}

vectors = [
    container,
    box1,
    box2,
    box1_inverse,
    box2_inverse
]

x_limits = [vector['coords'][0] for vector in vectors]
y_limits = [vector['coords'][1] for vector in vectors]
max_limit = max(x_limits + y_limits)
plt.xlim(0, int(max_limit + 1))
plt.ylim(0, int(max_limit + 1))
# add gridlines
plt.grid(True)

for vector in vectors:
    draw_vector(vector['coords'], vector['color'], vector.get('fill', False))
    # refresh graph
    plt.draw()
    plt.pause(0.5)

# additional vectors based on remaining space left by container
# box1
space1 = np.array([container['coords'][0] - box1['coords'][0], container['coords'][1]])
space2 = np.array([container['coords'][0], container['coords'][1] - box1['coords'][1]])
draw_vector(space1, 'blue', True)
draw_vector(space2, 'blue', True)
plt.draw()
plt.pause(0.5)

plt.show()

