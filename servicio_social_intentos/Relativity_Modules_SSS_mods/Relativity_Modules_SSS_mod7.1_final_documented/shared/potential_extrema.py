import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad


class PotentialDerivative:
    """
    a class to define "V", "dV/dR" and "d²V/dR²"
    defined by a chosen "f(R)" model
    """

    def __init__(self, f, f1, f2):
        self.f  = f
        self.f1 = f1  # the first derivative of "f"
        self.f2 = f2  # the second derivative of "f"

    def V(self, R, R_ref):
        """
        given as the potential difference
        "V(R) - V(R_ref)" obtained by integrating
        "dV/dR" from a given reference point ("R_ref")

        :param R: the independent variable
        :param R_ref: the chosen reference point
        :return: this method returns the potential difference obtained by integrating "dV/dR" from a chosen reference point
        """

        val, _ = quad(self.dVdR, R_ref, R)  # since "quad" returns the pair "numerical value, estimate of the absolute error in the integral", and we only use the numerical value: the "_" tells our code to "ignore" the second output of "quad" and only store the first one

        return val

    def dVdR(self, R):
        # given in the article as: (2 f(R) - R f1(R)) / 3

        return (2*self.f(R) - R*self.f1(R)) / 3

    def d2VdR2(self, R):
        # given as: (2 f1(R) - (1 f1(R) + R f2(R))) / 3

        return (self.f1(R) - R*self.f2(R)) / 3

def find_roots(h, start, stop, num_points=500):
    """
    defined to locate all the roots of a scalar function h(x)
    within the interval "[start, stop]" by scanning subintervals
    and calling the individual root finding function "brentq"
    where sign changes occur

    :param h: a function "h" whose zeros we're looking for
    :param start: the lower bound of the search interval
    :param stop: the upper bound of the search interval
    :param num_points: the number of subintervals to scan for sign changes
    :return: a list of approximate roots of "h"
    """

    xs = np.linspace(start, stop, num_points)  # the interval "[start, stop]"
    roots = []
    tol = 1e-12  # the tolerance for treating a value as zero

    for i in range(len(xs) - 1):  # this scans each adjacent pair "(a,b)" for either an exact zero or a sign flip

        a, b = xs[i], xs[i+1]  # this defines each (current) subinterval
        fa, fb = h(a), h(b)  # this definition is purely aesthetic

        if abs(fa) < tol:  # if "h(a)" is "extremely small", treat "a" as a root

            roots.append(a)

            continue  # this skips the rest of this iteration

        if abs(fb) < tol:# if "h(b)" is "extremely small", treat "b" as a root

            roots.append(b)

            continue  # this skips the rest of this iteration

        if fa * fb < 0:  # if there's a sign change, use Brent's method to refine

            try:

                roots.append(brentq(h, a, b))

            except ValueError:

                pass  # this lets us skip problematic intervals and continue scanning the rest of the "big" interval for valid roots (if the function "brentq" fails to converge on a particular subinterval, the code doesn’t crash but simply skips over this iteration and keeps looking in the next subinterval)

    return roots  # this returns the list of roots found in the interval "[start, stop]"

def find_global_minimum(p, start, stop, num_points=500, eps=1e-8):
    """
    this function finds the local minimum (assuming there's "only one minimum") of "V(R)" in "[start, stop]", excluding
    trivial roots at "R = 0" or exactly at the reference point

    :param p: an instance of the class "PotentialDerivative"
    :param start: the lower boundary of the interval (and also the reference point (R_ref) for "V")
    :param stop: the upper boundary of the interval
    :param num_points: number of points for root scanning
    :param eps: a threshold to exclude points too close to zero or to "R_ref"
    :return: the local minimum
    """

    # first we find the critical points of the potential using its first derivative
    crits = find_roots(p.dVdR, start, stop, num_points)  # which is a list

    if not crits:  # an empty list ("[]") is considered "False" when written in a "Boolean" context; that's why it's used in these "if" statements

        raise ValueError(f'we found no critical points in "[{start}, {stop}]"')

    # then we exclude "R = 0" as being a critical point (this condition is stated/suggested in page "5" of the article).
    # but maybe there's a better condition like "find the positive points that produce a local minima"
    crits = [r for r in crits if abs(r - 0) > eps]  # we chose only critical points that are away from "zero"

    # but if "crits=[]", then "if not crits" is equivalent to "if not False", which is equivalent to "if True", and so the statement evaluates the following block of code
    if not crits:

        raise ValueError(f'all critical points found in "[{start}, {stop}]" were too close to zero')

    # (this following condition may be avoided by defining the reference point in another place, but that may induce other conditions to exclude certain vales of "R"; and surely there's a better explanation for defining this following line of code)
    # since here we choose "R_ref = start", then we'll exclude critical points too close to the left boundary
    crits = [r for r in crits if abs(r - start) > eps]

    if not crits:

        raise ValueError(f'all critical points found in "[{start}, {stop}]" were too close to the boundary "R = {start}"')

    # a condition for a critical point to be one that produces minima, is for the second derivative at these points to be positive.
    # so let's find the critical points that produce minima by defining the following
    minima = [r for r in crits if p.d2VdR2(r) > 0]

    if not minima:

        raise ValueError(f'no local minima found in "[{start}, {stop}]"')

    # we now evaluate the potential ("up to a  constant" -which in the end doesn't really affect how we compare a value of "V" to be smaller than another)
    # at each critical point that produces a minimum
    V_vals = [p.V(r, start) for r in minima]

    # and we then (assuming there's only one value that produces a local minima and not two or more values that produce minima of same value but different input)
    # return the element of the list "minima"
    # which produces the smallest value of "V" in the interval "[start, stop]",
    # through the index "int(np.argmin(V_vals))"
    return minima[int(np.argmin(V_vals))]  # we use "int" in order to assure the index is an integer (to avoid any problems)
