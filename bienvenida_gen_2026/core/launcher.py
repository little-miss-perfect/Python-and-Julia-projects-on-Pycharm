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
    this class sets up the entire projectile simulation, it:
    - asks the user for inputs like whether to reuse k, or clear logs
    - prompts for the amount of participants and physical input values
    - validates that the target is within reach
    - initializes the simulation and logging components
    """

    def __init__(self):

        self.sim = None
        self.shooter = None
        self.selector = None
        self.logger = None
        self.v0 = None
        self.target_x = None
        self.hit_tolerance = None
        self.precise_mode = False
        self.allow_repeats = False
        self.participants = []          # it'll fill after asking for the amount of participants
        self.gamma = None               # the drag coefficient (not shown here)
        self.k = None                   # the spring constant
        self.time_sep = None            # the time‐marker interval "delta_t"
        self.arm_length = None          # we declare it here to avoid the "defined outside __init__" warning
        self.max_range = None           # same thing here

    def run(self):
        """
        the main setup logic: it prompts the user and builds the components.
        """

        print("launching the simulation setup...\n")

        # TODO run.1: use the "precise angle" interval mode
        self.precise_mode = prompt_yes_no(
            "enable 'precise angle' search mode?\n(this helps estimate the interval where an optimal angle lies)"
        )
        print()

        # TODO run.2: are repeats allowed?
        self.allow_repeats = prompt_yes_no("allow participants to take more than one shot?")
        print()

        # TODO run.3: clear the logs
        if prompt_yes_no("do you want to clear previous logs?"):
            for file in ['data/logs.csv', 'data/leaderboard.csv']:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"cleared file: {file}")
        print()

        # TODO run.4: ask for the amount of participants
        while True:
            try:
                n = int(input("how many participants are there? (input a natural number): "))
                if n > 0:
                    self.participants = [f"D{i+1}" for i in range(n)]  # which indicates one of the "desks" a participant sits in
                    break
                else:
                    print("please enter a natural number.")
            except ValueError:
                print("invalid input. please enter a valid number.")
        print()

        # TODO run.5: selection of the spring constant k (using a saved one or manually inputting one)
        if prompt_yes_no("do you want to use a saved spring constant 'k'?"):
            entry = load_saved_k(filepath="experimental/data/saved_k_values.csv")
            if entry:
                self.k = entry["k"]
                print(f"using saved 'k = {self.k:.2f} N/m' "
                      f"('{entry['name']}', l_0 = {entry['l0']} m)")
            else:
                print("no saved 'k' values available.")
        if self.k is None:
            # and for the manual entry we write
            while True:
                try:
                    val = float(input("enter the spring constant 'k (N/m)': "))
                    if val > 0:
                        self.k = val
                        break
                    else:
                        print("it must be positive.")
                except ValueError:
                    print("invalid input. please enter a positive number.")
        print()

        # TODO run.6: physical‐experimental inputs: l_0, m, x
        l0 = self._prompt_positive_float("enter the unstretched length of the spring (m): ")
        m  = self._prompt_positive_float("enter the projectile mass (kg): ")
        x  = self._prompt_positive_float("enter the stretched distance before launching (m): ")
        print()

        # TODO run.6.1: ask for the catapult's arm length
        arm_length = self._prompt_positive_float("enter the length of the catapult's arm (m): ")
        print()

        # TODO run.6.2: store the value for the simulator
        self.arm_length = arm_length


        # TODO run.7: compute the launch speed v_0 using energy conservation (from the potential energy in the spring to its kinetic energy once released)
        self.v0 = math.sqrt(self.k / m) * x
        print(f"computed launch speed (v0): {self.v0:.2f} m/s\n")

        # TODO run.8: ask for a "time‐marker" separation "delta_t"
        self.time_sep = self._prompt_positive_float("enter a time-marker separation for the plots (in seconds): ")
        print()

        # TODO run.9: this initializes the simulator now (so we can test reachability)
        self.sim = ProjectileSimulator(gamma=self.gamma, L=self.arm_length)
        self.shooter = ShootingEngine(self.sim)

        # TODO run.10: compute and store the horizontal range
        self.max_range = self._compute_max_range()
        print(f"maximum achievable horizontal distance: {self.max_range:.2f} m\n")

        # TODO run.11: prompt for "target_x", such that it's ≤ self.max_range
        while True:
            tgt = self._prompt_positive_float("enter the target horizontal distance (m): ")
            if tgt <= self.max_range:
                self.target_x = tgt
                break
            else:
                print(f"'{tgt:.2f} m' exceeds the maximum range ('{self.max_range:.2f} m'). please choose a lower value.\n")
        print()

        # TODO run.12: fix a "hit tolerance"
        self.hit_tolerance = 0.1  # hard coding is bad. we should eventually fix this and ask the user to define a "tolerance" for hitting the target

        # TODO run.13: finally, make a participant selector and logger
        self.selector = RandomSelector(self.participants)
        self.logger   = DataLogger()

    def get_components(self):
        """
        return the simulation components used in "main.py".
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
            self.allow_repeats,
            self.time_sep,
            self.max_range,
        )

    def _prompt_positive_float(self, message):
        """
        a helper method: keep asking until a positive float is entered.
        """

        while True:
            try:
                val = float(input(message + " "))
                if val > 0:
                    return val
                print("please enter a positive number.")
            except ValueError:
                print("invalid input. please enter a number.")

    def _compute_max_range(self, samples=90):
        """
        made to estimate the maximum horizontal distance by sampling angles
        evenly from 0° to 90° and taking the maximum final horizontal position
        at "y = 0" (at the moment, we've set this constraint to our model).
        """

        max_x = 0.0
        for theta in np.linspace(0, 90, samples):
            t_vals, sol_vals = self.sim.simulate(theta, self.v0)
            x_final = sol_vals[0, -1]
            if x_final > max_x:
                max_x = x_final
        return max_x
