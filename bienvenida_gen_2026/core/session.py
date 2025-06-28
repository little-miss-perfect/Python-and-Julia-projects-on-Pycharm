import math                                   # ← ADD: needed for φ→θ conversion
import matplotlib.pyplot as plt
import numpy as np                             # for arange
from interaction.histogram import plot_error_histogram, plot_hit_x_histogram

class GameSession:
    """
    Manages the simulation session loop for all participants.
    Handles guessing, plotting, logging, and histogram updates.
    """

    def __init__(self, sim, shooter, selector, logger,
                 v0, target_x, hit_tolerance,
                 precise_mode, allow_repeats,
                 time_sep):
        # Initialize simulation tools and config
        self.sim = sim
        self.shooter = shooter
        self.selector = selector
        self.logger = logger
        self.v0 = v0
        self.target_x = target_x
        self.hit_tolerance = hit_tolerance
        self.precise_mode = precise_mode
        self.allow_repeats = allow_repeats

        # Time‐marker spacing Δt
        self.time_sep = time_sep

        # Track interval‐narrowing guesses (precise mode)
        self.min_angle = None
        self.max_angle = None

        # Choose which histogram to display during the game
        self.use_error_histogram = self._prompt_histogram_mode()

    def _prompt_histogram_mode(self):
        """Prompt user to choose histogram mode with input validation."""
        while True:
            choice = input(
                "\n📊 Would you like to see:\n"
                "[A] How far off each shot was from the target?\n"
                "[B] Where most projectiles landed (x positions)?\n"
                "Enter A or B: "
            ).strip().lower()
            if choice == 'a':
                return True   # Use error histogram
            elif choice == 'b':
                return False  # Use x-position histogram
            else:
                print("⚠️ Please enter 'A' or 'B'.")

    def run(self):
        """Run the interactive session loop."""
        while True:
            print("\n--- NEW TURN ---")

            # Select participant
            try:
                person = self.selector.pick_random()
                print(f"🎲 Selected participant: {person}")
            except ValueError:
                print("✅ Everyone has gone! Resetting list...")
                self.selector.reset()
                continue

            # Remove if no repeats allowed
            if not self.allow_repeats:
                self.selector.remove_participant(person)

            # Compute true optimal angle θ* (hidden from user)
            theta_opt, predicted_error = self.shooter.find_optimal_angle(
                v0=self.v0, target_x=self.target_x
            )
            # Convert to arm‐orientation φ* = θ* + 90°, for our own posterity
            phi_opt = theta_opt + 90

            # --- REPLACED: prompt for φ instead of θ ---
            try:
                user_phi = float(input(
                "📐 Enter the arm orientation φ (° CCW from +x, must be ≥90° and ≤180°): "
                ))
                if not (90 <= user_phi <= 180):
                    print("❗ φ must be between 90° (horizontal) and 180° (vertical up).")
                    continue
            except ValueError:
                print("⚠️ Invalid input. Skipping turn.")
                continue

            # Convert to simulator θ = φ – 90°
            user_theta = user_phi - 90
            # ------------------------------------------

            # Simulate guessed trajectory using user_theta
            t_vals, sol_vals = self.sim.simulate(user_theta, self.v0)
            x_vals, y_vals = sol_vals[0], sol_vals[1]

            # Plot trajectory preview
            plt.clf()
            plt.figure(figsize=(8, 4.5))
            plt.plot(
                x_vals, y_vals,
                label=f'Trajectory (φ={user_phi:.1f}° → θ={user_theta:.1f}°)'
            )
            plt.axvline(self.target_x, color='green', linestyle='--', label='🎯 Target')

            # scatter‐plot time markers
            if self.time_sep:
                marks = np.arange(0, t_vals[-1] + self.time_sep, self.time_sep)
                idxs = [np.abs(t_vals - tm).argmin() for tm in marks]
                plt.scatter(
                    x_vals[idxs], y_vals[idxs],
                    color='red', s=25,
                    label=f'Time marks (Δt={self.time_sep}s)'
                )

            plt.title(f"Trajectory Preview for {person}")
            plt.xlabel('x (m)')
            plt.ylabel('y (m)')
            plt.grid(True)
            plt.axis('equal')
            plt.legend()
            plt.show()

            # Prompt for actual landing point
            try:
                hit_x = float(input("📍 Enter where the projectile landed (x in meters): "))
                if hit_x < 0 or hit_x > 10:
                    print("⚠️ That seems out of range. Try again.")
                    continue
                hit_y = 0.0
            except ValueError:
                print("⚠️ Invalid input. Skipping turn.")
                continue

            # Log the result using the simulator‐angle θ
            self.logger.log_throw(
                participant=person,
                theta_deg=user_theta,      # ← use θ here
                v0=self.v0,
                hit_x=hit_x,
                hit_y=hit_y,
                target_x=self.target_x
            )
            print("✅ Throw logged to data/logs.csv.")

            # Compute error and report hit/miss
            error = hit_x - self.target_x
            abs_error = abs(error)
            if abs_error <= self.hit_tolerance:
                print("🎯 HIT!")
            else:
                print(f"❌ Missed by {abs_error:.2f} meters.")

            # Interval narrowing in precise mode
            if self.precise_mode:
                if error < 0 and (self.min_angle is None or user_phi > self.min_angle):
                    self.min_angle = user_phi
                elif error > 0 and (self.max_angle is None or user_phi < self.max_angle):
                    self.max_angle = user_phi

                if self.min_angle is not None and self.max_angle is not None:
                    low, high = sorted([self.min_angle, self.max_angle])
                    print(f"📉 The optimal arm‐orientation is between ({low:.2f}°, {high:.2f}°)")

            # Histogram update
            print("📊 Updating histograms...")
            if self.use_error_histogram:
                plot_error_histogram(
                    filepath='data/logs.csv',
                    threshold=self.hit_tolerance,
                    show_normalized=True
                )
            else:
                plot_hit_x_histogram(filepath='data/logs.csv')

            # Prompt to continue or quit
            while True:
                next_action = input(
                    "⏭️ Press Enter for next participant, or type 'q' to quit: "
                ).strip().lower()
                if next_action in ('', 'q'):
                    break
                print("⚠️ Invalid input. Please press Enter or type 'q'.")

            if next_action == 'q':
                print("👋 Goodbye!")

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

                # Final precise‐mode print
                if self.precise_mode:
                    print("\n🔍 Final interval estimate based on guesses:")
                    if self.min_angle is not None and self.max_angle is not None:
                        low, high = sorted([self.min_angle, self.max_angle])
                        print(f"   Estimated φ interval: ({low:.2f}°, {high:.2f}°)")
                    else:
                        print("   Not enough data to estimate an interval.")

                # Show **both** θ solutions, but convert back to φ display
                solutions = self.shooter.find_angle_solutions(
                    v0=self.v0,
                    target_x=self.target_x,
                    theta_bounds=(1, 89),
                    samples=181
                )
                if solutions:
                    # convert θs to φs = θ+90
                    phi_sols = [s + 90 for s in solutions]
                    sol_list = ", ".join(f"{φ:.2f}°" for φ in phi_sols)
                    print(f"\n📌 Arm orientations φ to hit {self.target_x} m: {sol_list}")
                else:
                    print(f"\n📌 No exact angle solutions found for {self.target_x} m.")

                # Offer the other histogram
                while True:
                    see_other = input(
                        "\nWould you like to also see the other histogram? (y/n): "
                    ).strip().lower()
                    if see_other in ('y', 'n'):
                        break
                    print("⚠️ Please enter 'y' or 'n'.")
                if see_other == 'y':
                    if self.use_error_histogram:
                        plot_hit_x_histogram(filepath='data/logs.csv')
                    else:
                        plot_error_histogram(
                            filepath='data/logs.csv',
                            threshold=self.hit_tolerance,
                            show_normalized=True
                        )
                break  # exit the main loop
