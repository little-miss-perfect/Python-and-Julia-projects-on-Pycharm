import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp


# TODO 1: define "dr/dx = F(x, r)" (in a class)
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
        this is the vectorized derivative used in "solve_ivp"
        given by "dr/dx = F(x, r)",
        where "r" has the form "r = [n, m, R, R1, P, Ms, Mb]"
        """

        n, m, R, R1, P, Ms, Mb = r  # "unpack" the elements of the array "r"

        dr = np.zeros_like(r, dtype=float)  # create an empty array of the same size as "r" whose entries have the data type "float"

        # next we define the components of "F(x, r)" (by "filling in" the empty array "dr" defined above)
        dr[0] = self.n1(x, n, m, R, R1, P, Ms, Mb)
        dr[1] = self.m1(x, n, m, R, R1, P, Ms, Mb)
        dr[2] = self.DR(x, n, m, R, R1, P, Ms, Mb)
        dr[3] = self.R2(x, n, m, R, R1, P, Ms, Mb)
        dr[4] = self.DP(x, n, m, R, R1, P, Ms, Mb)
        dr[5] = self.DMs(x, n, m, R, R1, P, Ms, Mb)
        dr[6] = self.DMb(x, n, m, R, R1, P, Ms, Mb)

        return dr

# TODO 2: define the numerical method (in a class)
class ShootingSolver:
    '''
    this is a class to define a "shooting" method solver
    that adjusts the initial Ricci scalar "R0" in a way that
    the solution hits a specific boundary value at "x = x_max"

    Attributes:
        F           : callable "F(x, r)" defining "dr/dx = F(x, r)"
        base_r0     : 1D ndarray, the base initial‐condition vector "[n, m, R, R1, P, Ms, Mb]"
        t_span      : tuple "(0, x_max)" representing the integration interval in "x"
        method      : str, the SciPy "solve_ivp" method to use (e.g. 'DOP853')
        rtol, atol  : floats, solver tolerances
        component   : int, which entry of "r" to adjust ("2" corresponds to "R")
        target      : float, desired value of "r[component]" at "x = x_max"
    '''

    # first, we initialize the object
    def __init__(self, F, base_r0, t_span, target,  # the target parameter is the "R0" value we want to tend to (this is the value at which the potential reaches a nontrivial minimum)
                 method='DOP853', rtol=1e-5, atol=1e-8):

        self.F = F  # given by "dr/dx = F(x, r)"
        self.base_r0 = np.copy(base_r0)  # the initial conditions (we copy them to not accidentally edit the original throughout the program)
        self.t_span = t_span  # our integration domain
        self.method = method  # the method the initial value problem solver (from SciPy uses
        self.rtol = rtol  # the relative tolerance
        self.atol = atol  # the absolute tolerance
        self.component = 2  # the component of "r" we're analyzing
        self.target = target  # here we initialize the "target"

    def residual_method(self, R0_guess):
        '''
        given a guess for the component of the
        initial value of "r[2]", this computes
        "how far off" the integrated solution is from
        hitting the target at the outer boundary.

        we'd like for this function to return something
        very close to zero (because of what it returns)

        :param R0_guess: a "guess" of the initial value of "r[2]"
        :return diff: the difference "R_final - R_target" (which we'd like to be as close to zero as possible)
        '''

        r0 = np.copy(self.base_r0)  # we copy for the same reason stated above
        r0[self.component] = R0_guess  # the component is set in the constructor of this class

        # now we solve our system of equations with this proposed value
        sol = solve_ivp(
            fun=self.F,
            t_span=self.t_span,
            y0=r0,
            method=self.method,
            rtol=self.rtol,
            atol=self.atol
        )

        # next keep in mind that "sol.y" is a "2D array" (like a matrix), that is,
        # each row is one component of the solution, and
        # each column is a value at a "grid point"
        # (the "grid" is defined by the steps taken during the integration -using the independent variable "x").
        diff = sol.y[self.component, -1] - self.target  # "sol.y[self.component, -1]" is the final value of the component considered here (i.e. "2")
        return diff
        # if this returns zero, it means that given an initial value
        # "R0_guess"
        # we ended up exactly at our target (which is what we want).
        # but a positive value means we overshot,
        # and a negative value means undershot.

    def solve(self, bracket, maxiter=100):
        '''
        this method finds, via bisection (using Brent’s method),
        the value of "R0_guess" within our bracket
        that makes the residual zero

        :param bracket: a tuple "(a, b)" such that "residual_method(a)" and "residual_method(b)"
                        have opposite signs; since we know we haven't yet found the
                        correct initial value, then the method "residual_method"
                        in the interval "(a, b)" must have a zero (the value we're looking for).
                        that's why we know they have opposite signs
        :param maxiter: the number of iterations Brent’s method will attempt
        :return: the best estimate of the initial Ricci scalar "R0" that "shoots" the solution to our desired boundary value
        '''

        root, result = brentq(
            self.residual_method,  # remember, we want "R_final - R_target" to be as close to zero as possible; so we'll look for the zero of this function defined by the method "residual_method"
            bracket[0],
            bracket[1],
            maxiter=maxiter,
            full_output=True  # this gives us a result object with convergence information
        )

        if not result.converged:

            raise RuntimeError(f"our root search did not converge: {result.flag}")

        return root  # the initial value we're looking for

# TODO 3: refine the initial guess
def find_valid_bracket(F, base_r0, target, initial_bracket, x_max, method='DOP853', rtol=1e-5, atol=1e-8, expansion_factor=2.0, max_expansions=10):
    """
    this function expands or contracts an initial guess bracket "[a, b]" until the shooting‐method
    residuals at the endpoints have opposite signs, which is required for
    root‐finding algorithms like Brent’s method (which we're mainly using)

    :param F               : callable "F(x, r)" defining "dr/dx = F(x, r)"
    :param base_r0         : ndarray, base initial‐condition vector (of length "7")
    :param target          : float, desired boundary value for "r[2]" at "x = x_max"
    :param initial_bracket : tuple(float, float), initial interval "(a, b)",
                             where we'd like to search the value of the initial condition,
                             where we hope "residual(a)" and "residual(b)" have opposite signs
    :param x_max           : float, the upper limit of the integration domain
    :param method          : str, name of the integrator to use (passed to "solve_ivp")
    :param rtol            : float, relative tolerance for the solver
    :param atol            : float, absolute tolerance for the solver
    :param expansion_factor: float, factor by which to expand or contract the bracket in each iteration
    :param max_expansions  : int, maximum number of expansion/contraction attempts
    :return: tuple (a, b)   where residual(a) and residual(b) have opposite signs
    :raises ValueError     if no valid bracket is found within max_expansions
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

    # if the residual returns zero, it means that given an initial value
    # we ended up exactly at our target (which is what we want).
    # but a positive value means we overshot,
    # and a negative value means undershot.
    a, b = initial_bracket  # we first unpack the interval where we'd like to begin searching
    f_a = solver.residual_method(a)
    f_b = solver.residual_method(b)

    if np.sign(f_a) != np.sign(f_b):  # different signs mean we still need to refine the initial value

        return (a, b)  # so we're okay with the current selected interval

    for i in range(max_expansions):

        a = a / expansion_factor
        b = b * expansion_factor + 10**i
        f_a = solver.residual_method(a)
        f_b = solver.residual_method(b)

        if np.sign(f_a) != np.sign(f_b):  # different signs mean we still need to refine the initial value

            return (a, b)  # so we're okay with the current selected interval

    # but... if no interval can be found, then we print this in the output
    raise ValueError(
        f'no valid bracket was found after "{max_expansions}" expansions. '
        f'the last residuals were: f({a})={f_a:.3e}, f({b})={f_b:.3e}'
    )

def refine_R0(base_r0, target_R, initial_bracket, F, x_max, refinement_steps=9, tol_residual=1e-6):
    """
    its purpose is to "refine" the shooting‐method bracket
    to find a better "R0".
    if both endpoint residuals ("solver._residual" at "a" and at "b")
    ever fall below "tol_residual",
    it stops.
    if the bracket ever becomes "same‐signed" (which means we can't find a root in the current interval),
    it returns the last root estimate.
    else, it solves for a new root and shrinks/expands the bracket

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

    # we first create an object with the parameters of this method
    solver = ShootingSolver(
        F       = F,
        base_r0 = base_r0,
        target  = target_R,
        t_span  = (0, x_max),
        rtol    = 1e-5,
        atol    = 1e-8,
    )

    # then we unpack the bracket's endpoints
    a, b        = initial_bracket

    # next, "current_R0" starts as "None" to mark that "no root has been found yet".
    # after the first call to "solver.solve()", it will hold the last good estimate.
    # we use this to:
    #  1) fall back to the midpoint -only on the very first iteration- if both ends are already within the specified tolerance
    #  2) recover the last estimate if the bracket ever becomes same‐signed later
    current_R0  = None

    # next comes the iterative refinement
    for step in range(refinement_steps):  # this is "how many times we'll refine" our initial condition
    # remember that indexing in Python starts from zero

        f_low  = solver.residual_method(a)
        f_high = solver.residual_method(b)

        # 1) if both boundary values of the current interval are already within the given tolerance, accept the "current_R0" value or take the midpoint of the current interval
        if abs(f_low) < tol_residual and abs(f_high) < tol_residual:

            result = current_R0 if current_R0 is not None else 0.5*(a + b)

            print(f'''step "{step+1}": the residuals are pretty small. let's stop the refinement at "R0 = {result:.12f}"''')

            return result

        # 2) if the bracket has same‐signed residuals (which means we can't use a root finding method), we'll return the last known estimate
        if np.sign(f_low) == np.sign(f_high):

            if current_R0 is not None:

                print(f"Step {step+1}: same‐sign bracket—using last R0 = {current_R0:.12f}")

                return current_R0

            else:

                raise ValueError(f"Invalid initial bracket: [{f_low:.3e}, {f_high:.3e}]")

        # 3) otherwise, we'll find the new root and "tighten" (decrease the "size" of) the current bracket
        current_R0 = solver.solve(bracket=(a, b))

        print(f"Step {step+1}: R0 = {current_R0:.12f}, Bracket: ({a:.12f}, {b:.12f})")

        # and to define a shrinking/expanding window size
        # around our latest root estimate,
        # assuming that the interval is in "a positive domain",
        # we'll do the following:

        # on each iteration we'll try to shrink the bracket tightly around our new best root guess,
        # using a "shrinking delta" that gets tinier each time (i.e. on each iteration).
        #
        # but by pairing that with a "fixed‐factor" expansion (a factor of "0.8" on the left, and a factor of "1.2" on the right),
        # we guarantee that the bracket can grow a bit if our "shrinking" (from one endpoint -or maybe both)
        # would accidentally exclude the actual root.
        #
        # so this hybrid "shrink‐but‐never‐too‐tight" strategy helps us keep Brent’s method "usable"
        # by always enclosing a "sign change" (which is what the method needs),
        # while still converging in around our estimate.

        # so, after one iteration, we'll start at "1%"
        # of the bracket's width and shrink it by a factor
        # of "10" in each iteration
        delta = 10 ** (-(step + 2)) * (b - a)  # remember that indexing starts at "0" (so in the first iteration we have "0 + 2")

        # to compute the new left endpoint:
        #   1) "current_R0 - delta" shrinks (from the left) "around the root"
        #   2) "a * 0.8" allows a "20%" slip outward from where it was before (it does this if shrinking would "cut the root out of the interval"). that is, it moves the left endpoint "a bit further to the left"
        # and we then take (of the two) the closest one to the root, to ensure the root remains bracketed by computing the following
        a = max(current_R0 - delta, a * 0.8)

        # to compute the new right endpoint:
        #   1) "current_R0 + delta" shrinks (from the right) "around the root"
        #   2) "b * 1.2" allows a "20%" slip outward from where it was before. that is, it moves the right endpoint "a bit further to the right"
        # take (of the two) the closest one to the root, to keep the bracket valid, by computing the following
        b = min(current_R0 + delta, b * 1.2)

    # if we finish all the refinement steps, we'll return the last estimate
    return current_R0
