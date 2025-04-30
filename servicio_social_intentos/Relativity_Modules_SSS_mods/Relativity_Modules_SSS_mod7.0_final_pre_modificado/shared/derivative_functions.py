import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp


# TODO 1: define "dr/dx = F(x, r)" and the numerical method (in a class)
class DerivativeFunctions:
    '''
    this must be defined as a class, since
    we'd like to create various instances 
    of these objects depending on the chosen scenario.
    
    it gives us the functions needed to define our 
    system of differential equations (which takes the form
    "dr/dx = F(x, r)").
    it makes things "modular"
    '''
    
    def __init__(self, f, f1, f2, f3, f32, rho, xrho, T):
        
        self.f    = f
        self.f1   = f1
        self.f2   = f2
        self.f3   = f3
        self.f32  = f32
        self.rho  = rho
        self.xrho = xrho
        self.T    = T

    def n1(self, x, n, m, R, R1, P, Ms, Mb):

        kappa = 8 * np.pi
        sum11 = m * (x ** 2) * (self.f(R) - R * self.f1(R) + 2 * kappa * P)
        sum12 = m * (x ** 2) * (self.f(R) - R * self.f1(R))
        sum2 = 2 * self.f1(R) * (m - 1) - 4 * x * R1 * self.f2(R)

        if x == 0:  # as defined on page "3" of the article

            return 0.0

        elif P > 0:  # as defined on page "2" of the article

            coeff = n / (x * (2 * self.f1(R) + x * R1 * self.f2(R)))

            return coeff * (sum11 + sum2)

        else:  # as defined in the original Fortran program

            coeff = n / (x * (2 * self.f1(R) + x * R1 * self.f2(R)))

            return coeff * (sum12 + sum2)

    def m1(self, x, n, m, R, R1, P, Ms, Mb):

        coeff2 = x * R1 * (self.f2(R) / self.f1(R))
        coeff3 = (m * (x ** 2)) / 3
        kappa  = 8 * np.pi

        sum1 = 2 * self.f1(R) * (1 - m)
        sum2 = R * self.f1(R) + self.f(R)
        sum3 = 2 * R * self.f1(R) - self.f(R)
        sum4 = 2 * x * R1 * self.f2(R)

        if x == 0:  # as defined on page "3" of the article

            return 0.0

        elif P > 0:  # as defined on page "2" of the article

            coeff1 = m / (x * (2 * self.f1(R) + x * R1 * self.f2(R)))

            return (coeff1 *
                    (sum1 - 2 * m * (x**2) * kappa * (-self.rho) +
                    coeff3 * (sum2 + 2 * kappa * self.T) +
                    coeff2 *
                    (coeff3 * (sum3 + kappa * self.T) -
                     kappa * m * (x**2) * (-self.rho + P) +
                     sum1 + sum4)))

        else:  # as defined in the original Fortran program

            coeff1 = m / (x * (2 * self.f1(R) + x * R1 * self.f2(R)))

            return (coeff1 *
                    (sum1 +
                    coeff3 * sum2 +
                    coeff2 *
                    (coeff3 * sum3 +
                    sum1 + sum4)))

    def DR(self, x, n, m, R, R1, P, Ms, Mb):
        '''
        we need to add this function because 
        it makes the system of "7" equations with "7" unknowns
        able to be solved given a function of the form "dr/dx = F(x, r)"
        '''
        
        if x == 0:  # as defined on page "3" of the article

            return 0.0

        elif P > 0 or (x <= 0.1 and P <= 0):  # as defined in the original Fortran program (collapsing two "elif" statements into one, from the Fortran program)

            return R1

        else:  # as defined in the original Fortran program

            return 0.0

    def R2(self, x, n, m, R, R1, P, Ms, Mb):
        
        m1_val = self.m1(x, n, m, R, R1, P, Ms, Mb)
        n1_val = self.n1(x, n, m, R, R1, P, Ms, Mb)

        kappa  = 8 * np.pi

        sum1 = 2 * self.f(R) - R * self.f1(R)
        sum2 = 3 * self.f3(R) * (R1 ** 2)

        coeff1 = 1 / (3 * self.f2(R))

        if x == 0:  # as defined on page "3" of the article

            return (sum1 + kappa * self.T) / (9 * self.f2(R))

        elif P > 0:  # as defined on page "2" of the article

            sum3 = (m1_val/(2*m)) - (n1_val/(2*n)) - 2/x  # this condition happens after seeing that "x!=0"

            return coeff1 * (m * (kappa * self.T + sum1) - sum2) + sum3 * R1  # "+ sum3 * R1" coincides in this and the next case

        elif x <= 0.1 and P <= 0:  # as defined in the original Fortran program

            sum3 = (m1_val/(2*m)) - (n1_val/(2*n)) - 2/x  # this condition happens after seeing that "x!=0"

            return coeff1 * (m * sum1) - self.f32(R) * (R1**2) + sum3 * R1  # this is after distributing "coeff1" to "sum2"

        else:  # as defined in the original Fortran program

            return 0.0

    def DP(self, x, n, m, R, R1, P, Ms, Mb):

        if x == 0:  # as defined on page "3" of the article

            return 0.0  # because it's defined in terms of "n1", and at "0" this is "0"

        elif P > 0:  # as defined on page "3" of the article

            n1_val = self.n1(x, n, m, R, R1, P, Ms, Mb)

            return - (self.rho + P) * (n1_val / (2 * n))

        else:  # as defined in the original Fortran program

            return 0.0

    def DMs(self, x, n, m, R, R1, P, Ms, Mb):

        kappa = 8 * np.pi

        if x == 0:  # as defined in the original Fortran program

            return 0.0

        elif P > 0:  # as defined in the original Fortran program

            return (1/2) * kappa * (x**2) * self.rho

        else:  # as defined in the original Fortran program

            return 0.0

    def DMb(self, x, n, m, R, R1, P, Ms, Mb):

        return self.DMs(x, n, m, R, R1, P, Ms, Mb) * self.xrho  # as defined in the original Fortran program

    def F(self, x, r):
        """
        the vectorized derivative used in "solve_ivp"
         given by "dr/dx = F(x, r)". it returns "dr/dx".
        where has the form "r = [n, m, R, R1, P, Ms, Mb]"

        returns "F(x, r)"
        """

        n, m, R, R1, P, Ms, Mb = r  # "unpack" the elements of the array "r"

        dr = np.zeros_like(r, dtype=float)

        # next we define the components of "F(x, r)"
        dr[0] = self.n1(x, n, m, R, R1, P, Ms, Mb)
        dr[1] = self.m1(x, n, m, R, R1, P, Ms, Mb)
        dr[2] = self.DR(x, n, m, R, R1, P, Ms, Mb)
        dr[3] = self.R2(x, n, m, R, R1, P, Ms, Mb)
        dr[4] = self.DP(x, n, m, R, R1, P, Ms, Mb)
        dr[5] = self.DMs(x, n, m, R, R1, P, Ms, Mb)
        dr[6] = self.DMb(x, n, m, R, R1, P, Ms, Mb)

        return dr

class ShootingSolver:
    '''
    a class to define a "shooting method"
    '''
    # first, we initialize the object
    def __init__(self, F, base_r0, t_span, target,  # the target parameter is the "R0" value we want to tend to (this is the value at which the potential reaches a nontrivial minimum)
                 method='DOP853', rtol=1e-9, atol=1e-12):

        self.F = F  # given by "dr/dx = F(x, r)"
        self.base_r0 = np.copy(base_r0)  # the initial conditions (we copy them to not accidentally edit the original throughout the program)
        self.t_span = t_span  # our integration domain
        self.method = method  # the method the initial value problem solver (from SciPy uses
        self.rtol = rtol  # the relative tolerance
        self.atol = atol  # the absolute tolerance
        self.component = 2  # the component of "r" we're analyzing
        self.target = target  # here we initialize the "target"

    def _residual(self, R0_guess):
        '''
        Given a guess for the component of the
        initial value of "r[2]", this computes
        "how far off" the integrated solution is from
        hitting the target at the outer boundary.

        we'd like for this function to return something
        very close to zero (because of what it returns)
        '''

        r0 = np.copy(self.base_r0)
        r0[self.component] = R0_guess  # the component is set in the constructor of this class

        # now we solve or system of equations with this proposed value
        sol = solve_ivp(
            fun=self.F,
            t_span=self.t_span,
            y0=r0,
            method=self.method,
            rtol=self.rtol,
            atol=self.atol
        )

        # next keep in mind that "sol.y" is a "2D array", that is
        # each row is one component of the solution, and
        # each column is a value at a grid point
        # (the grid is defined by the steps taken during the integration -using the independent variable "x").
        return sol.y[self.component, -1] - self.target  # "sol.y[self.component, -1]" is the final value of the component considered here (i.e. "2")
        # if this returns zero, it means that given an initial value "R0_guess"
        # we ended up exactly at your target (which is what we want).
        # but a positive value means we overshot,
        # and a negative value means undershot.

    def solve(self, bracket, maxiter=100):
        '''
        this method finds, via bisection (using Brent’s method),
        the value of "R0_guess" within our bracket
        that makes the residual zero.
        :param bracket: a tuple "(a, b)" such that "_residual(a)" and "_residual(b)" have opposite signs (it represents an interval).
        :param maxiter: the number of iterations Brent’s method will try.
        :return: the best estimate of the initial Ricci scalar "R0" that "shoots" the solution to our desired boundary value
        '''
        root, result = brentq(
            self._residual,
            bracket[0],
            bracket[1],
            maxiter=maxiter,
            full_output=True  # gives us a result object with convergence information
        )

        if not result.converged:

            raise RuntimeError(f"convergence failed: {result.flag}")

        return root

# TODO 2: to refine the initial guess
def refine_R0(base_r0, target_R, initial_bracket, F, x_max, refinement_steps=9, tol_residual=1e-9):
    """
    its purpose is to "refine" the shooting‐method bracket
    to find a better "R0".
    if both endpoint residuals ("solver._residual" at "a" and at "b")
    ever fall below "tol_residual",
    it stops.
    if the bracket ever becomes "same‐signed",
    it returns the last root estimate.

    :param base_r0: the "initial condition" vector of length "7"
    :param target_R: the "target condition" (the desired boundary value for the component of index "2" at "x = x_max")
    :param initial_bracket: a tuple "(a, b)" such that we believe the correct "R0" lies between "a" and "b"
    :param F: defined by "dr/dx = F(x, r)"
    :param x_max: the end of the integration interval
    :param refinement_steps: defined as "how many times we 're-shrink' the bracket"
    :param tol_residual: (try not to use something below the integrator’s own accuracy. maybe "1e-12" is already small enough)
                         the threshold below which a residual (at the endpoints of the interval we're refining)
                         "|solver._residual(a) - 0|" or "|solver._residual(b) - 0|"
                         is "close enough" to zero
                         (which is what we want. we'd like for
                         the residuals to be zero, but numerically, that's hard,
                         so we aim to get something "close enough" to zero)
    """

    solver = ShootingSolver(
        F       = F,
        base_r0 = base_r0,
        target  = target_R,
        t_span  = (0, x_max),
        rtol    = 1e-9,
        atol    = 1e-12,
    )

    a, b        = initial_bracket
    current_R0  = None

    for step in range(refinement_steps):

        f_low  = solver._residual(a)
        f_high = solver._residual(b)

        # 1) If both ends are within tolerance, accept current_R0 / midpoint:
        if abs(f_low) < tol_residual and abs(f_high) < tol_residual:

            result = current_R0 if current_R0 is not None else 0.5*(a + b)

            print(f"Step {step+1}: residuals tiny—stopping at R0 = {result:.12f}")

            return result

        # 2) If bracket is same‐signed at any point, and we have a last estimate, return it:
        if np.sign(f_low) == np.sign(f_high):

            if current_R0 is not None:

                print(f"Step {step+1}: same‐sign bracket—using last R0 = {current_R0:.12f}")

                return current_R0

            else:

                raise ValueError(f"Invalid initial bracket: [{f_low:.3e}, {f_high:.3e}]")

        # 3) Otherwise find the new root and tighten the bracket
        current_R0 = solver.solve(bracket=(a, b))

        print(f"Step {step+1}: R0 = {current_R0:.12f}, Bracket: ({a:.12f}, {b:.12f})")

        delta = 10**(-step-2) * (b - a)
        a     = max(current_R0 - delta, a * 0.8)
        b     = min(current_R0 + delta, b * 1.2)

    # If we finish all steps, return the last estimate
    return current_R0

def find_valid_bracket(F, base_r0, target, initial_bracket, x_max, method='DOP853', rtol=1e-9, atol=1e-12, expansion_factor=2.0, max_expansions=10):
    """
    Given an ODE F, initial state base_r0 (whose index 2 we adjust),
    and a target value, expand or contract the bracket until
    f(a) and f(b) have opposite sign. Returns (a, b) or raises.
    """

    solver = ShootingSolver(
        F       = F,
        base_r0 = base_r0,
        target  = target,
        t_span  = (0, x_max),
        method  = method,
        rtol    = rtol,
        atol    = atol
    )

    a, b = initial_bracket
    f_a = solver._residual(a)
    f_b = solver._residual(b)

    if np.sign(f_a) != np.sign(f_b):

        return (a, b)

    for i in range(max_expansions):

        a = a / expansion_factor
        b = b * expansion_factor + 10**i
        f_a = solver._residual(a)
        f_b = solver._residual(b)

        if np.sign(f_a) != np.sign(f_b):

            return (a, b)

    raise ValueError(
        f"No valid bracket found after {max_expansions} expansions. "
        f"Last residuals: f({a})={f_a:.3e}, f({b})={f_b:.3e}"
    )
