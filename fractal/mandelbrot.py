import numpy as np
import matplotlib.pyplot as plt

# Function to determine if a point is in the Mandelbrot set
def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    if n == max_iter:
        return max_iter
    return n + 1 - np.log(np.log2(abs(z)))

# Image size (pixels)
width = 800
height = 800

# Plot window
real_axis = np.linspace(-2.0, 2.0, width)
imag_axis = np.linspace(-2.0, 2.0, height)

# Create a list of complex coordinates
c = np.array([r + 1j*i for r in real_axis for i in imag_axis])

# Compute Mandelbrot sequence
mandelbrot_vector = np.vectorize(mandelbrot)
escape_values = mandelbrot_vector(c, 256).reshape((height, width))

# Plotting
def plot_mandelbrot():
    plt.imshow(escape_values, extent=(-2.0, 1.0, -1.5, 1.5), cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title('Mandelbrot Set')
    plt.xlabel('Re')
    plt.ylabel('Im')
    plt.show()
