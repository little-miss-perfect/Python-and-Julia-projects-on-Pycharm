import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

class PotentialDerivative:
    """
    dV/dR and d²V/dR² for V defined by your f(R), plus V(R) itself.
    """
    def __init__(self, f, f1, f2):
        self.f  = f
        self.f1 = f1
        self.f2 = f2

    def dVdR(self, R):
        # Eqn: (2 f(R) - R f1(R)) / 3
        return (2*self.f(R) - R*self.f1(R)) / 3

    def d2VdR2(self, R):
        # Eqn: (f1(R) - R f2(R)) / 3
        return (self.f1(R) - R*self.f2(R)) / 3

    def V(self, R, R0):
        """
        Potential difference V(R) - V(R0) = ∫[R0→R] dV/dR(x) dx
        """
        val, _ = quad(self.dVdR, R0, R)
        return val


def find_roots(h, start, stop, num_points=500):
    """
    Find *all* zeros of h(x) in [start, stop] by scanning subintervals
    and calling brentq where sign‐changes occur.
    """
    xs = np.linspace(start, stop, num_points)
    roots = []
    tol = 1e-12

    for i in range(len(xs) - 1):
        a, b = xs[i], xs[i+1]
        fa, fb = h(a), h(b)

        if abs(fa) < tol:
            roots.append(a)
            continue
        if abs(fb) < tol:
            roots.append(b)
            continue
        if fa * fb < 0:
            try:
                roots.append(brentq(h, a, b))
            except ValueError:
                pass

    return roots


def find_global_minimum(p, start, stop, num_points=500, eps=1e-8):
    """
    Return the R ∈ [start, stop] where V(R) is minimal, excluding R=0:
      1) find all roots of dV/dR
      2) drop any |R| < eps (to exclude zero)
      3) drop any |R - start| < eps (to exclude the left endpoint)
      4) keep only those with d2V/dR2 > 0 (local minima)
      5) evaluate V(R) = ∫[start→R] dV/dR
      6) pick the R with the smallest V
    """
    # 1) find critical points
    crits = find_roots(p.dVdR, start, stop, num_points)
    if not crits:
        raise ValueError(f"No critical points in [{start}, {stop}]")

    # 2) exclude zero
    crits = [r for r in crits if abs(r) > eps]
    if not crits:
        raise ValueError("All critical points too close to zero")

    # 3) exclude the left endpoint
    crits = [r for r in crits if abs(r - start) > eps]
    if not crits:
        raise ValueError("All critical points too close to the start")

    # 4) keep only true minima
    minima = [r for r in crits if p.d2VdR2(r) > 0]
    if not minima:
        raise ValueError("No local minima found in that interval")

    # 5) compute V at each candidate
    Vvals = [p.V(r, start) for r in minima]

    # 6) return the R with the smallest V
    return minima[int(np.argmin(Vvals))]
