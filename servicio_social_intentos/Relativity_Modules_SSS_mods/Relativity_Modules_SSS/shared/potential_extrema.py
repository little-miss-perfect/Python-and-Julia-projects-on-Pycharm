class PotentialDerivative:
    """
    A class for computing dV/dR in a scenario-agnostic way.
    It takes scenario-specific functions f and f1 (passed from main.py).
    """

    def __init__(self, f, f1):
        """
        Initialize the class with scenario-specific f and f1.

        :param f: A callable representing f(R)
        :param f1: A callable representing f'(R)
        """
        self.f = f
        self.f1 = f1

    def dVdR(self, R):
        """
        Computes dV/dR = (1/3) * (2*f(R) - R*f1(R))
        as described in the paper.

        :param R: The Ricci scalar
        :return: The value of dV/dR at R
        """
        return (1/3) * (2 * self.f(R) - self.f1(R) * R)

import numpy as np
from scipy.optimize import brentq


def find_roots(f, x_start, x_end, num_points=500):
    x_grid = np.linspace(x_start, x_end, num_points)
    roots = []

    for i in range(len(x_grid) - 1):
        x_left = x_grid[i]
        x_right = x_grid[i+1]
        f_left = f(x_left)
        f_right = f(x_right)

        # Check if either endpoint is effectively zero
        tol = 1e-12
        if abs(f_left) < tol:
            roots.append(x_left)
            continue
        if abs(f_right) < tol:
            roots.append(x_right)
            continue

        # Check for sign change
        if f_left * f_right < 0:
            try:
                root = brentq(f, x_left, x_right)
                roots.append(root)
            except ValueError:
                # This would be unusual if there's a genuine sign change
                pass

    return roots



