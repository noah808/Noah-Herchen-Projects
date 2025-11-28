from math import *
import numpy as np

def create_sphere(theta, phi, r):
    points = []
    for p in phi:
        for t in theta:
            x = r * cos(t) * sin(p)
            y = r * sin(t) * sin(p)
            z = r * cos(p)
            points.append(np.matrix([x, y, z]))
    return points
