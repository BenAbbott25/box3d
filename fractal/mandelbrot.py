import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Function to determine if a point is in the Mandelbrot set
def mandelbrot(c, max_iter, power):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z**power + c
        n += 1
    if n == max_iter:
        return max_iter
    return n + 1 - np.log(np.log2(abs(z)))

# Plotting
def plot_mandelbrot(zoom, max_iter, power, real_offset, imag_offset, frame):
    width = 1200
    height = 1200
    real_axis = np.linspace(real_offset - zoom, real_offset + zoom, width)
    imag_axis = np.linspace(imag_offset - zoom, imag_offset + zoom, height)
    c = np.array([r + 1j*i for r in real_axis for i in imag_axis])
    mandelbrot_vector = np.vectorize(mandelbrot)
    escape_values = mandelbrot_vector(c, max_iter, power).reshape((height, width))
    plt.figure(figsize=(10, 8))
    plt.imshow(escape_values, extent=(real_offset - zoom, real_offset + zoom, imag_offset - zoom, imag_offset + zoom), cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title(f'Mandelbrot Set (max_iter: {max_iter}, power: {round(power, 2)})')
    plt.xlabel('Re')
    plt.ylabel('Im')
    if not os.path.exists('max_iter_' + str(max_iter)):
        os.makedirs('max_iter_' + str(max_iter))
    plt.savefig(f'max_iter_{max_iter}/max_iter_{max_iter}_run_2_frame_{frame}.png')
    # plt.show()
    plt.close()

zoom = 2.0
max_iter = 256
power = 1.0
real_offset = 0.0
imag_offset = 0.0

min_power = 1.0
max_power = 5.0
step = 0.01
max_iters = [64]
for max_iter in tqdm(max_iters):
    frame = 0
    for power in tqdm(np.arange(min_power, max_power + step, step)):
        plot_mandelbrot(zoom, max_iter, power, real_offset, imag_offset, frame)
        frame += 1
