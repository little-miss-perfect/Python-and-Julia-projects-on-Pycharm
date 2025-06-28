import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt

class ProjectileSimulator:
    def __init__(self, m=0.02, R=0.02, L=0.5, eta=1.8e-5, g=9.81, gamma=None):
        """
        Initialize the simulator with physical constants.

        Parameters:
        - m: mass of projectile (kg)
        - R: radius of projectile (m)
        - L: length of catapult arm (m)
        - eta: dynamic viscosity of air (Pa·s)
        - g: gravitational acceleration (m/s^2)
        - gamma: optional air resistance coefficient. If None, compute it using theoretical formula.

        Coordinate system:
        - x-axis: horizontal ground
        - y-axis: vertical (positive upward)
        - theta_deg: angle from the horizontal at launch (0° = horizontal, 90° = vertical)
        """
        self.m = m
        self.R = R
        self.L = L
        self.eta = eta
        self.g = g

        if gamma is not None:
            self.gamma = gamma  # Use provided gamma (experimental)
        else:
            self.gamma = 6 * np.pi * self.eta * self.R  # Use theoretical drag coefficient

    def initial_conditions(self, theta_deg, v0):
        """
        Compute initial conditions [x, y, vx, vy] from launch parameters.

        - theta_deg is the release angle (measured from horizontal)
        - v0 is the launch speed
        - Assumes launch height = length of the catapult arm (pivot height)
        """
        theta = np.radians(theta_deg)  # θ = φ – 90° when called from session.py
        vx0 = v0 * np.cos(theta)
        vy0 = v0 * np.sin(theta)
        x0 = 0.0
        # release height = arm length × sin(pi - φ) = arm length × sin(φ)
        # since here θ = φ–90°, sin(φ) = cos(θ)
        y0 = self.L * np.cos(theta)
        return [x0, y0, vx0, vy0]

    def equations_of_motion(self, t, u):
        """
        System of first-order ODEs:
        u = [x, y, vx, vy]
        Returns du/dt for each state variable.
        """
        x, y, vx, vy = u
        dxdt = vx
        dydt = vy
        dvxdt = - (self.gamma / self.m) * vx
        dvydt = - self.g - (self.gamma / self.m) * vy
        return [dxdt, dydt, dvxdt, dvydt]

    def simulate(self, theta_deg, v0, t_max=5.0):
        """
        Simulate projectile motion for a given launch angle and speed.
        Stops when projectile hits the ground (y ≤ 0).
        """
        u0 = self.initial_conditions(theta_deg, v0)
        sol = solve_ivp(self.equations_of_motion, [0, t_max], u0,
                        dense_output=True, max_step=0.01, rtol=1e-8, atol=1e-10)

        t_vals = np.linspace(0, t_max, 1000)
        sol_vals = sol.sol(t_vals)
        y_vals = sol_vals[1]

        # Stop at first contact with ground
        idx_ground = np.where(y_vals <= 0)[0]
        if len(idx_ground) > 0:
            idx_ground = idx_ground[0]
            t_vals = t_vals[:idx_ground+1]
            sol_vals = sol_vals[:, :idx_ground+1]

        return t_vals, sol_vals

    def find_optimal_angle(self, v0, target_x, theta_bounds=(10, 80)):
        """
        Find the angle (in degrees) that lands closest to a given horizontal distance.

        Uses a bounded scalar minimization (shooting method).
        """
        def objective(theta_deg):
            _, sol_vals = self.simulate(theta_deg, v0)
            x_final = sol_vals[0, -1]
            return abs(x_final - target_x)

        result = minimize_scalar(objective, bounds=theta_bounds, method='bounded')
        return result.x, result.fun

    def plot_trajectory(self, sol_vals, t_vals, label=None, time_sep=0.1):
        """
        Plot trajectory and highlight time-marked points every `time_sep` seconds.

        Parameters:
        - sol_vals: [x, y, vx, vy] over time
        - t_vals: time values
        - label: label for the trajectory
        - time_sep: time spacing between plotted markers
        """
        x_vals = sol_vals[0]
        y_vals = sol_vals[1]

        plt.plot(x_vals, y_vals, label=label)

        time_marks = np.arange(0, t_vals[-1], time_sep)
        mark_indices = [np.abs(t_vals - tm).argmin() for tm in time_marks]
        plt.scatter(x_vals[mark_indices], y_vals[mark_indices],
                    color='red', s=10, label='Time marks (Δt=0.1s)')

        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        plt.title('Projectile Trajectory with Time Markers')
        plt.grid(True)
        plt.axis('equal')
        plt.legend()
