import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

class PotentialDerivative:
    """
    A class for computing dV/dR and its second derivative in a scenario-agnostic way.
    It takes scenario-specific f, f1, and f2.
    """
    def __init__(self, f, f1, f2):
        self.f  = f
        self.f1 = f1
        self.f2 = f2

    def dVdR(self, R):
        # dV/dR = (2*f(R) - R*f1(R)) / 3
        return (2*self.f(R) - R*self.f1(R)) / 3

    def d2VdR2(self, R):
        # d²V/dR² = (f1(R) - R*f2(R)) / 3
        return (self.f1(R) - R*self.f2(R)) / 3


def find_roots(h, start, stop, num_points=500):
    '''
    this is to find multiple roots in an interval; not just one

    :param h: the function to find its roots
    :param start: beginning of the interval
    :param stop: end of the interval
    :param num_points: how many points to include in the interval
    :return: the function returns the roots of "h" in the chosen interval
    '''

    xs = np.linspace(start, stop, num_points)
    roots = []
    tol = 1e-12

    for i in range(len(xs)-1):

        a, b = xs[i], xs[i+1]
        fa, fb = h(a), h(b)

        if abs(fa) < tol:

            roots.append(a)

            continue

        if abs(fb) < tol:

            roots.append(b)

            continue

        if fa*fb < 0:

            try:

                roots.append(brentq(h, a, b))

            except ValueError:

                pass

    return roots


def find_global_minimum(p, start, stop, num_points=500, eps=1e-8):
    """
    Find the *non-zero* critical point R in [start,stop] where V''(R)>0
    (i.e. a local minimum) and |R|>eps, then return the one furthest from
    zero (the global minimum on that interval).
    """

    # 1) find all dV/dR = 0
    crits = find_roots(p.dVdR, start, stop, num_points)

    if not crits:

        raise ValueError(f"No critical points in [{start},{stop}]")

    # 2) keep only those sufficiently far from zero
    crits = [r for r in crits if abs(r) > eps]

    if not crits:

        raise ValueError("All critical points too close to zero")

    # 3) filter to true minima (d2V/dR2 > 0)
    minima = [r for r in crits if p.d2VdR2(r) > 0]

    if not minima:

        raise ValueError("No local minima found in that interval")

    # 4) pick the one with the largest |R| (farthest from zero)
    return max(minima, key=abs)