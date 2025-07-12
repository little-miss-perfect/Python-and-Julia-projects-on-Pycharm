import matplotlib.pyplot as plt
import numpy as np
from interaction.histogram import plot_error_histogram, plot_hit_x_histogram


class GameSession:
    """
    manages the simulation session loop for all the participants.
    it also handles guessing, plotting, logging, and histogram updates.
    """

    def __init__(self, sim, shooter, selector, logger,
                 v0, target_x, hit_tolerance,
                 precise_mode, allow_repeats,
                 time_sep, max_range):

        # we first initialize the simulation tools and configuration
        self.sim = sim
        self.shooter = shooter
        self.selector = selector
        self.logger = logger
        self.v0 = v0
        self.target_x = target_x
        self.hit_tolerance = hit_tolerance
        self.precise_mode = precise_mode
        self.allow_repeats = allow_repeats

        # the time‐marker spacing
        self.time_sep = time_sep
        self.max_range = max_range

        # and to track the interval‐narrowing guesses (in "precise mode"), we define
        self.min_angle = None
        self.max_angle = None

        # and to choose which histogram to display during the game we write
        self.use_error_histogram = self._prompt_histogram_mode()

        # to ask if the user wants to see the true optimal φ* (the "angle of orientation for the catapult's arm") once we define
        answer = input(
            "\nreveal true optimal arm‐orientations φ* before guessing? (y/n): "
        ).strip().lower()
        self.reveal_optimal = (answer == 'y')

    def _prompt_histogram_mode(self):
        """
        defined to prompt the user to choose the histogram mode.
        """

        while True:
            choice = input(
                "\nwould you like to see:\n"
                "[A] how far off each shot was from the target?\n"
                "[B] where most projectiles landed ('x' positions)?\n"
                "enter A or B: "
            ).strip().lower()
            if choice == 'a':
                return True   # to use the error histogram
            elif choice == 'b':
                return False  # to use the x-position histogram
            else:
                print("please enter 'A' or 'B'.")

    def run(self):
        """
        defined to run the interactive session loop.
        """

        # compute both "theta" solutions once, convert to "phi = theta + 90°"
        solutions = self.shooter.find_angle_solutions(
            v0=self.v0,
            target_x=self.target_x,
            theta_bounds=(1, 89),
            samples=181
        )  # this method scans the interval from 1° to 89° in "samples=181" steps, looking for points where the function "f(theta) = x_final(theta) - target_x", changes sign. wherever it sees a sign change (or an exact zero), it runs a "bisection method" to find that root to within about 0.001°, giving every "theta" in that range whose trajectory lands exactly at "target_x". and finally, it returns a sorted list of those theta values "[theta_1, theta_2]" (one "low-angle" and one "high-angle" solution).

        # convert theta-solutions into phi-solutions
        phi_sols = [theta + 90 for theta in solutions]  # the resulting list contains the actual "arm-stop angles" we should input ("[phi_1, phi_2]") to hit our target.

        # reveal all φ* solutions once, before any guesses
        if self.reveal_optimal:
            sol_list = ", ".join(f"{phi:.2f}°" for phi in phi_sols)
            print(f"\n[hint] the true optimal arm‐orientations are φ* = {sol_list}\n")

        # TODO while.1: now, we enter the "per‐turn" loop
        while True:
            print("\n--- NEW TURN ---")

            # TODO while.1.1: select a participant at random
            try:
                person = self.selector.pick_random()
                print(f"selected participant: {person}")
            except ValueError:
                print("everyone has gone! resetting the list...")
                self.selector.reset()
                continue

            # TODO while.1.2: remove a chosen participant if no repeats are allowed
            if not self.allow_repeats:
                self.selector.remove_participant(person)

            # TODO while.1.3: prompt for phi instead of theta
            try:
                user_phi = float(input(
                    "enter the arm orientation 'phi'\n(in degrees, measured counterclockwise from the positive 'x-axis', in the interval '(90°, 180°)': "
                ))
                if not (90 <= user_phi <= 180):
                    print("phi must be between 90° and 180°.")
                    continue
            except ValueError:
                print("invalid input. skipping turn.")
                continue

            # TODO while.1.4: convert to the simulator's angle "theta = phi – 90°"
            user_theta = user_phi - 90

            # TODO while.1.5: simulate the guessed trajectory using "user_theta"
            t_vals, sol_vals = self.sim.simulate(user_theta, self.v0)
            x_vals, y_vals = sol_vals[0], sol_vals[1]

            # TODO while.1.6: plot the trajectory preview (for the guess)
            plt.clf()
            plt.figure(figsize=(8, 4.5))
            plt.plot(
                x_vals, y_vals,
                color='darkslateblue',
                label=f'trajectory (phi={user_phi:.1f}°, theta={user_theta:.1f}°)'
            )
            plt.axvline(self.target_x, color='olivedrab', linestyle='--', label='target')

            # TODO while.1.7: scatter/plot time-markers
            if self.time_sep:
                marks = np.arange(0, t_vals[-1] + self.time_sep, self.time_sep)
                idxs = [np.abs(t_vals - tm).argmin() for tm in marks]
                plt.scatter(
                    x_vals[idxs], y_vals[idxs],
                    color='orange', s=25,
                    label=f'time marks ("delta_t={self.time_sep}s")'
                )

            plt.title(f"trajectory preview for {person}")
            plt.xlabel('x (m)')
            plt.ylabel('y (m)')
            plt.grid(True)
            plt.axis('equal')  # to use the same scale on both axes
            plt.legend()
            plt.show()

            # TODO while.1.8: prompt for the actual landing point (more of an experimental thing)
            try:
                hit_x = float(input("enter where the projectile landed ('x' in meters): "))
                if hit_x < 0 or hit_x > self.max_range:  # we can't shoot backwards, and we can't shoot further than the maximum horizontal distance, so we write this line
                    print("that seems out of range. try again.")
                    continue
                hit_y = 0.0
            except ValueError:
                print("invalid input. skipping turn.")
                continue

            # TODO while.1.9: log the result using the simulator‐angle "theta"
            self.logger.log_throw(
                participant=person,
                theta_deg=user_theta,      # right here
                v0=self.v0,
                hit_x=hit_x,
                hit_y=hit_y,
                target_x=self.target_x
            )
            print("throw logged to data/logs.csv.")

            # TODO while.1.10: compute the error and report hit/miss
            error = hit_x - self.target_x
            abs_error = abs(error)
            if abs_error <= self.hit_tolerance:
                print("HIT!")
            else:
                print(f"MISSED! by '{abs_error:.2f} m'.")

            # TODO while.1.11: "interval narrowing" in "precise mode"
            if self.precise_mode:
                if error < 0 and (self.min_angle is None or user_phi > self.min_angle):
                    self.min_angle = user_phi
                elif error > 0 and (self.max_angle is None or user_phi < self.max_angle):
                    self.max_angle = user_phi

                if self.min_angle is not None and self.max_angle is not None:
                    low, high = sorted([self.min_angle, self.max_angle])
                    print(f"the optimal arm‐orientation is between '({low:.2f}°, {high:.2f}°)'")

            # TODO while.1.12: histogram update
            print("updating histograms...")
            if self.use_error_histogram:
                plot_error_histogram(
                    filepath='data/logs.csv',
                    threshold=self.hit_tolerance,
                    show_normalized=True
                )
            else:
                plot_hit_x_histogram(filepath='data/logs.csv')

            # TODO while.2: prompt to continue or quit
            while True:
                next_action = input(
                    "press 'enter' for the next participant, or type 'q' to quit: "
                ).strip().lower()
                if next_action in ('', 'q'):
                    break
                print("invalid input. please press 'enter' or type 'q'.")

            if next_action == 'q':
                print("goodbye! :)")

                # Show leaderboard
                from simulation.analysis import show_leaderboard
                show_leaderboard(
                    filepath='data/logs.csv',
                    top_n=5,
                    hit_only=True,
                    tolerance=self.hit_tolerance,
                    export_csv=True,
                    show_chart=True
                )

                # TODO while.2.1: final "precise mode" print
                if self.precise_mode:
                    print("\nfinal interval estimate based on guesses:")
                    if self.min_angle is not None and self.max_angle is not None:
                        low, high = sorted([self.min_angle, self.max_angle])
                        print(f"   estimated 'phi' interval: ({low:.2f}°, {high:.2f}°)")
                    else:
                        print("   there's not enough data to estimate an interval.")

                # TODO while.2.2: show **both** "theta" solutions, but convert back to "phi"
                solutions = self.shooter.find_angle_solutions(
                    v0=self.v0,
                    target_x=self.target_x,
                    theta_bounds=(1, 89),  # is this the most general interval to consider? maybe for the original experimental setup we have in mind. but it may not be so general as we think...
                    samples=181
                )
                if solutions:
                    # TODO while.2.2.1: convert "theta" angles to "phi" angles using that "phi = theta + 90"
                    phi_sols = [s + 90 for s in solutions]
                    sol_list = ", ".join(f"{φ:.2f}°" for φ in phi_sols)
                    print(f"\narm orientations 'phi' to hit '{self.target_x} m': {sol_list}")
                else:
                    print(f"\nno exact angle solutions found for '{self.target_x} m'.")

                # TODO while.2.2.3: offer the other histogram
                while True:
                    see_other = input(
                        "\nwould you like to also see the other histogram? (y/n): "
                    ).strip().lower()
                    if see_other in ('y', 'n'):
                        break
                    print("please enter 'y' or 'n'.")
                if see_other == 'y':
                    if self.use_error_histogram:
                        plot_hit_x_histogram(filepath='data/logs.csv')
                    else:
                        plot_error_histogram(
                            filepath='data/logs.csv',
                            threshold=self.hit_tolerance,
                            show_normalized=True
                        )
                break  # and finally, we exit the main loop
