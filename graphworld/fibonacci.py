# Generate n evenly-spaced points on the unit sphere using a Fibonacci spiral.

from math import sin, cos, sqrt, pi


def fibonacci_sphere(n: int):
    phi = (1 + sqrt(5)) / 2  # Golden ratio
    z = [1 - (1 + 2*i)/n for i in range(n)]
    x = [cos(2 * i * phi * pi) * sqrt(1 - z[i]**2) for i in range(n)]
    y = [sin(2 * i * phi * pi) * sqrt(1 - z[i]**2) for i in range(n)]
    return list(zip(x, y, z))
