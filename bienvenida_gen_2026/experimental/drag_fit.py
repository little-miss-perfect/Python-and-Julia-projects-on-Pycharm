import csv
import numpy as np
from scipy.optimize import minimize
from simulation.projectile import ProjectileSimulator

class DragEstimator:
    """
    Estimates the air resistance coefficient (gamma) by minimizing squared error
    between measured and simulated projectile landing positions.
    Also allows saving the result and appending to historical gamma values.
    """

    def __init__(self, filepath='data/logs.csv'):
        """Initialize with path to the CSV log."""
        self.filepath = filepath
        self.logs = self._load_data()
        self.simulator = ProjectileSimulator()

    def _load_data(self):
        """Load angle, speed, and hit_x from the CSV log."""
        data = []
        with open(self.filepath, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    angle = float(row['theta_deg'])
                    v0 = float(row['v0'])
                    hit_x = float(row['hit_x'])
                    data.append((angle, v0, hit_x))
                except (ValueError, KeyError):
                    continue  # Skip malformed rows
        return data

    def _total_squared_error(self, gamma):
        """
        Compute the total squared error for a given gamma.

        Parameters:
        - gamma: air resistance coefficient to test

        Returns:
        - Total squared error between simulated and real hit_x values
        """
        self.simulator.gamma = gamma  # Update drag coefficient in simulator
        error_sum = 0.0

        for angle, v0, measured_x in self.logs:
            t_vals, sol_vals = self.simulator.simulate(theta_deg=angle, v0=v0)
            sim_x = sol_vals[0][-1]  # Final x position from simulation
            error_sum += (sim_x - measured_x)**2

        return error_sum

    def estimate_gamma(self, initial_guess=0.1):
        """
        Perform optimization to estimate the best-fit gamma.

        Parameters:
        - initial_guess: starting value for gamma in minimization

        Returns:
        - Optimal gamma value (float)
        """
        result = minimize(self._total_squared_error, x0=[initial_guess], bounds=[(0, None)])
        return result.x[0] if result.success else None

    def save_gamma(self, gamma, savefile='data/estimated_gamma.csv'):
        """
        Append the estimated gamma to a CSV file for future use or averaging.

        Parameters:
        - gamma: the gamma value to save
        - savefile: path to output file where gammas are accumulated
        """
        with open(savefile, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([gamma])

    def load_average_gamma(self, savefile='data/estimated_gamma.csv'):
        """
        Load and return the average gamma from a saved CSV.
        Returns None if the file is missing or empty.
        """
        gammas = []
        try:
            with open(savefile, mode='r') as f:
                reader = csv.reader(f)
                for row in reader:
                    try:
                        gammas.append(float(row[0]))
                    except (ValueError, IndexError):
                        continue
        except FileNotFoundError:
            return None

        return np.mean(gammas) if gammas else None
