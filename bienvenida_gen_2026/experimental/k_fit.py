import csv
import os
import matplotlib.pyplot as plt
import numpy as np

class SpringEstimator:
    """
    Class to collect and analyze bungee stretch data to estimate the spring constant k.
    """

    def __init__(self, l0, filename='experimental/data/raw_k_measurements.csv', load_previous=False):
        """
        Initialize the estimator.

        Parameters:
        - l0: unstretched length of the bungee cord (in meters)
        - filename: where to store/load stretch data
        - load_previous: whether to load existing measurements (default: False)
        """
        self.l0 = l0                      # Unstretched length of the cord
        self.filename = filename         # File where raw measurements will be stored
        self.data = []                   # In-memory list of (mass, stretched length)

        # Only load old data if explicitly requested
        if load_previous and os.path.exists(self.filename):
            self._load_existing()

    def _load_existing(self):
        """Load previous mass–length data from CSV file."""
        with open(self.filename, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append((float(row['mass_kg']), float(row['length_m'])))

    def add_measurement(self, mass, length):
        """
        Add one (mass, stretched_length) data point and append to the CSV.

        Parameters:
        - mass: mass used to stretch (kg)
        - length: resulting stretched length of the cord (m)
        """
        self.data.append((mass, length))

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        # Check whether header needs to be written
        file_exists = os.path.exists(self.filename)
        write_header = not file_exists or os.path.getsize(self.filename) == 0

        with open(self.filename, mode='a', newline='') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(['mass_kg', 'length_m'])  # Write header once
            writer.writerow([mass, length])

        print("✅ Measurement added to CSV.")

    def estimate_k(self):
        """
        Estimate the spring constant k using linear regression (F = kx).

        Returns:
        - Estimated k (float) or None if not enough data.
        """
        if len(self.data) < 2:
            return None

        g = 9.81  # Acceleration due to gravity (m/s^2)
        forces = []
        displacements = []

        for m, L in self.data:
            F = m * g                      # Convert mass to weight
            x = L - self.l0                # Stretch = length - unstretched
            forces.append(F)
            displacements.append(x)

        displacements = np.array(displacements)
        forces = np.array(forces)

        # Linear regression to get slope (k)
        k, intercept = np.polyfit(displacements, forces, 1)

        # Plot results
        plt.figure()
        plt.scatter(displacements, forces, color='blue', label='Measurements')
        plt.plot(displacements, k * displacements + intercept, color='red', label=f'Fit: F = {k:.2f}x')
        plt.xlabel('Displacement (m)')
        plt.ylabel('Force (N)')
        plt.title('Estimated Spring Constant k')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        print(f"🧮 Estimated spring constant k = {k:.2f} N/m")
        return k
