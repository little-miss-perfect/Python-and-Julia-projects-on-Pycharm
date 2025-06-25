import os
import math
import numpy as np                              # For sampling angles
from helper_functions.k_database import load_saved_k
from helper_functions.prompt import prompt_yes_no
from simulation.projectile import ProjectileSimulator
from simulation.shooting import ShootingEngine
from interaction.random_selector import RandomSelector
from interaction.data_log import DataLogger


class SimulationLauncher:
    """
    This class sets up the entire projectile simulation:
    - Asks the user for inputs like whether to reuse k, or clear logs
    - Prompts for participant count and physics values
    - Validates that the target is within reach
    - Initializes simulation and logging components
    """

    def __init__(self):
        # Will hold our core objects
        self.sim = None
        self.shooter = None
        self.selector = None
        self.logger = None
        self.v0 = None
        self.target_x = None
        self.hit_tolerance = None
        self.precise_mode = False
        self.allow_repeats = False
        self.participants = []   # will fill after asking count
        self.gamma = None        # drag coefficient
        self.k = None            # spring constant

    def run(self):
        """Main setup logic: prompts the user and builds components."""
        print("🎬 Launching Simulation Setup...\n")

        # 1) Precise angle‐interval mode?
        self.precise_mode = prompt_yes_no(
            "Enable precise angle search mode?\nThis helps estimate the interval where the optimal angle lies"
        )
        print()

        # 2) Repeats allowed?
        self.allow_repeats = prompt_yes_no("Allow participants to take more than one shot?")
        print()

        # 3) Clear logs?
        if prompt_yes_no("Do you want to clear previous logs?"):
            for file in ['data/logs.csv', 'data/leaderboard.csv']:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"🧹 Cleared file: {file}")
        print()

        # 4) How many participants?
        while True:
            try:
                n = int(input("👥 How many participants are there? (positive integer): "))
                if n > 0:
                    self.participants = [f"D{i+1}" for i in range(n)]
                    break
                else:
                    print("❗ Please enter a natural number.")
            except ValueError:
                print("❗ Invalid input. Please enter a valid number.")
        print()

        # 5) Spring constant k selection (saved vs manual)
        if prompt_yes_no("Do you want to use a saved spring constant (k)?"):
            entry = load_saved_k(filepath="experimental/data/saved_k_values.csv")
            if entry:
                self.k = entry["k"]
                print(f"✅ Using saved k = {self.k:.2f} N/m "
                      f"('{entry['name']}', l₀ = {entry['l0']} m)")
            else:
                print("⚠️ No saved k values available.")
        if self.k is None:
            # Manual entry
            while True:
                try:
                    val = float(input("🔧 Enter the spring constant k (N/m): "))
                    if val > 0:
                        self.k = val
                        break
                    else:
                        print("❗ Must be positive.")
                except ValueError:
                    print("❗ Invalid input. Please enter a number.")
        print()

        # 6) Physical‐experiment inputs: l0, m, x
        l0 = self._prompt_positive_float("📏 Enter the unstretched length of the bungee cord (m): ")
        m  = self._prompt_positive_float("⚖️  Enter the projectile mass (kg): ")
        x  = self._prompt_positive_float("📐 Enter the stretch distance when launching (m): ")
        print()

        # 7) Compute launch speed v0 via energy conversion
        self.v0 = math.sqrt(self.k / m) * x
        print(f"💡 Computed launch speed (v0): {self.v0:.2f} m/s\n")

        # 8) Initialize the simulator now (so we can test reachability)
        self.sim     = ProjectileSimulator(gamma=self.gamma)  # gamma set earlier or default
        self.shooter = ShootingEngine(self.sim)

        # 9) Compute maximum achievable horizontal range
        max_range = self._compute_max_range()
        print(f"📈 Maximum achievable horizontal distance: {max_range:.2f} m\n")

        # 10) Prompt for target_x, enforce <= max_range
        while True:
            tgt = self._prompt_positive_float("🎯 Enter the target horizontal distance (m): ")
            if tgt <= max_range:
                self.target_x = tgt
                break
            else:
                print(f"❗ {tgt:.2f} m exceeds max range ({max_range:.2f} m). Please choose a lower value.\n")
        print()

        # 11) Fixed hit tolerance
        self.hit_tolerance = 0.1

        # 12) Finally build selector & logger
        self.selector = RandomSelector(self.participants)
        self.logger   = DataLogger()

    def get_components(self):
        """Return simulation components for main.py."""
        return (
            self.sim,
            self.shooter,
            self.selector,
            self.logger,
            self.v0,
            self.target_x,
            self.hit_tolerance,
            self.precise_mode,
            self.allow_repeats
        )

    def _prompt_positive_float(self, message):
        """Helper: keep asking until a positive float is entered."""
        while True:
            try:
                val = float(input(message + " "))
                if val > 0:
                    return val
                print("❗ Please enter a positive number.")
            except ValueError:
                print("❗ Invalid input. Please enter a number.")

    def _compute_max_range(self, samples=91):
        """
        Estimate the maximum horizontal distance by sampling angles
        evenly from 0° to 90° and taking the maximum final x.
        """
        max_x = 0.0
        for theta in np.linspace(0, 90, samples):
            t_vals, sol_vals = self.sim.simulate(theta, self.v0)
            x_final = sol_vals[0, -1]
            if x_final > max_x:
                max_x = x_final
        return max_x
