import numpy as np
from scipy.optimize import minimize_scalar, bisect
from .projectile import ProjectileSimulator

class ShootingEngine:
    """
    Class to compute optimal launch parameters (e.g., angle or speed) for hitting a horizontal target.

    This class wraps around an instance of `ProjectileSimulator` and performs optimization using
    numerical simulation and shooting methods.
    """

    def __init__(self, simulator: ProjectileSimulator):
        """
        Constructor to initialize with an instance of ProjectileSimulator.

        Parameters:
        - simulator: an object of ProjectileSimulator that handles the physics simulation.
        """
        self.sim = simulator  # Store the simulator instance

    def find_optimal_angle(self, v0, target_x, theta_bounds=(10, 80)):
        """
        Use a numerical shooting method to find the best launch angle (in degrees) to reach a target.

        Parameters:
        - v0: launch speed (m/s), kept fixed during optimization
        - target_x: horizontal distance to hit (in meters)
        - theta_bounds: tuple (min_angle, max_angle) in degrees, defines the search interval

        Returns:
        - best_theta: the optimal angle in degrees that lands closest to target_x
        - error: the absolute difference between the landing position and target_x
        """

        # This internal function computes the "error" for a given angle
        def error_function(theta_deg):
            # Simulate the projectile's trajectory with this angle and fixed speed
            _, sol_vals = self.sim.simulate(theta_deg, v0)
            x_final = sol_vals[0, -1]  # Final horizontal position of the projectile
            return abs(x_final - target_x)  # Return absolute distance from target

        # Use bounded minimization to find the angle that minimizes landing error
        result = minimize_scalar(error_function, bounds=theta_bounds, method='bounded')

        # Return the optimal angle and final error
        return result.x, result.fun

    def find_optimal_speed(self, theta_deg, target_x, v_bounds=(1, 15)):
        """
        Use a numerical shooting method to find the best launch speed (in m/s) to reach a target.

        Parameters:
        - theta_deg: launch angle (in degrees), kept fixed during optimization
        - target_x: horizontal distance to hit (in meters)
        - v_bounds: tuple (min_speed, max_speed), defines the speed range to search

        Returns:
        - best_v0: the optimal speed in m/s that lands closest to target_x
        - error: the absolute difference between the landing position and target_x
        """

        # This internal function computes the "error" for a given speed
        def error_function(v0):
            # Simulate the projectile's trajectory with this speed and fixed angle
            _, sol_vals = self.sim.simulate(theta_deg, v0)
            x_final = sol_vals[0, -1]  # Final horizontal position of the projectile
            return abs(x_final - target_x)  # Return absolute distance from target

        # Use bounded minimization to find the speed that minimizes landing error
        result = minimize_scalar(error_function, bounds=v_bounds, method='bounded')

        # Return the optimal speed and final error
        return result.x, result.fun

    def find_angle_solutions(self, v0, target_x, theta_bounds=(1, 89), samples=181):
        """
        Find *all* launch angles (in degrees) that land at target_x.
        Scans the interval [theta_bounds[0], theta_bounds[1]] in `samples` steps,
        identifies sign-changes of f(θ)=x_final(θ)−target_x, and then refines each
        bracket with bisection.

        Returns:
          - sorted list of unique angle(s) in degrees
        """

        # define f(θ)
        def f(theta_deg):
            _, sol = self.sim.simulate(theta_deg, v0)
            return sol[0, -1] - target_x

        # sample θ values and evaluate f
        thetas = np.linspace(theta_bounds[0], theta_bounds[1], samples)
        vals = [f(th) for th in thetas]

        roots = []
        for i in range(len(thetas) - 1):
            a, b = thetas[i], thetas[i + 1]
            fa, fb = vals[i], vals[i + 1]

            # exact hit at a sample point?
            if abs(fa) < 1e-6:
                roots.append(a)
            # bracketed zero crossing?
            elif fa * fb < 0:
                try:
                    root = bisect(f, a, b, xtol=1e-3)
                    roots.append(root)
                except ValueError:
                    pass

        # dedupe within 0.01° and sort
        unique = []
        for r in roots:
            if not any(abs(r - u) < 1e-2 for u in unique):
                unique.append(r)
        return sorted(unique)