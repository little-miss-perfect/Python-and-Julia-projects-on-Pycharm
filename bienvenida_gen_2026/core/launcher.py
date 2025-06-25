# core/launcher.py

from helper_functions.k_database import load_saved_k  # To load saved k values from CSV
from helper_functions.prompt import prompt_yes_no     # To ask yes/no questions safely
from simulation.projectile import ProjectileSimulator
from simulation.shooting import ShootingEngine
from interaction.random_selector import RandomSelector
from interaction.data_log import DataLogger

import os
import math


class SimulationLauncher:
    """
    This class sets up the entire projectile simulation:
    - Asks the user for inputs like whether to reuse k, or clear logs
    - Prompts for participant count and physics values
    - Initializes simulation and logging components
    """

    def __init__(self):
        # We'll store all generated components here
        self.sim = None
        self.shooter = None
        self.selector = None
        self.logger = None
        self.v0 = None
        self.target_x = None
        self.hit_tolerance = None
        self.precise_mode = False
        self.allow_repeats = False

    def run(self):
        """Main setup logic: prompts the user and builds components."""
        print("🎬 Launching Simulation Setup...\n")

        # Ask if the user wants to search for optimal angle interval
        self.precise_mode = prompt_yes_no(
            "Enable precise angle search mode?\nThis helps estimate the interval where the optimal angle lies")
        print()

        # Ask if participants can go more than once
        self.allow_repeats = prompt_yes_no("Allow participants to take more than one shot?")
        print()

        # Ask if logs should be cleared
        reset_logs = prompt_yes_no("Do you want to clear previous logs?")
        if reset_logs:
            for file in ['data/logs.csv', 'data/leaderboard.csv']:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"🧹 Cleared file: {file}")
        print()

        # Ask how many participants there are
        while True:
            try:
                n = int(input("👥 How many participants are there? (positive integer): "))
                if n > 0:
                    break
                else:
                    print("❗ Please enter a natural number.")
            except ValueError:
                print("❗ Invalid input. Please enter a valid number.")

        participants = [f"D{i + 1}" for i in range(n)]

        # === SPRING CONSTANT SELECTION ===
        use_saved_k = prompt_yes_no("Do you want to use a saved spring constant (k)?")
        if use_saved_k:
            k_entry = load_saved_k(filepath="experimental/data/saved_k_values.csv")
            if k_entry is None:
                print("⚠️ No saved k values available. Please enter manually.")
                use_saved_k = False
            else:
                k = k_entry["k"]
                print(f"✅ Using saved k = {k:.2f} N/m (from '{k_entry['name']}', unstretched length = {k_entry['l0']} m)")

        if not use_saved_k:
            while True:
                try:
                    k = float(input("🔧 Enter the spring constant k (N/m): "))
                    if k > 0:
                        break
                    else:
                        print("❗ Please enter a positive number.")
                except ValueError:
                    print("❗ Invalid input. Please enter a number.")

        # === Ask for physical experiment inputs ===
        l0 = self._prompt_positive_float("📏 Enter the unstretched length of the bungee cord (in meters): ")
        m = self._prompt_positive_float("🎯 Enter the projectile mass (in kilograms): ")
        x = self._prompt_positive_float("📐 Enter the pullback distance (how far the bungee cord is stretched before release, in meters): ")
        self.target_x = self._prompt_positive_float("🎯 Enter the target horizontal distance (in meters): ")
        self.hit_tolerance = 0.1  # fixed tolerance for success

        # === Calculate launch speed based on energy conversion ===
        self.v0 = math.sqrt(k / m) * x
        print(f"\n💡 Computed launch speed (v0): {self.v0:.2f} m/s\n")

        # === Initialize the physics and logging objects ===
        self.sim = ProjectileSimulator()
        self.shooter = ShootingEngine(self.sim)
        self.selector = RandomSelector(participants)
        self.logger = DataLogger()

    def get_components(self):
        """
        Return all initialized simulation components to be used in main.py.
        """
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
        """Prompt the user until they give a valid positive float."""
        while True:
            try:
                value = float(input(message))
                if value > 0:
                    return value
                else:
                    print("❗ Please enter a positive number.")
            except ValueError:
                print("❗ Invalid input. Please enter a number.")
