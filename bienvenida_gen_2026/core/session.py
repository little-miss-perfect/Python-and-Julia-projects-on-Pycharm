import matplotlib.pyplot as plt
from interaction.histogram import plot_error_histogram, plot_hit_x_histogram

class GameSession:
    """
    Manages the simulation session loop for all participants.
    Handles guessing, plotting, logging, and histogram updates.
    """

    def __init__(self, sim, shooter, selector, logger,
                 v0, target_x, hit_tolerance,
                 precise_mode, allow_repeats):
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

        # Track interval narrowing guesses (precise mode)
        self.min_angle = None
        self.max_angle = None

        # Choose which histogram to display during the game
        self.use_error_histogram = self._prompt_histogram_mode()

    def _prompt_histogram_mode(self):
        """Prompt user to choose histogram mode with input validation."""
        while True:
            choice = input("\n📊 Would you like to see:\n[A] How far off each shot was from the target?\n[B] Where most projectiles landed (x positions)?\nEnter A or B: ").strip().lower()
            if choice == 'a':
                return True  # Use error histogram
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

            # Compute true optimal angle (hidden from user)
            angle, predicted_error = self.shooter.find_optimal_angle(
                v0=self.v0, target_x=self.target_x
            )

            # Prompt user for their guess
            try:
                user_angle = float(input("📐 Guess the launch angle (in degrees): "))
            except ValueError:
                print("⚠️ Invalid angle input. Skipping turn.")
                continue

            # Simulate guessed trajectory
            t_vals, sol_vals = self.sim.simulate(user_angle, self.v0)
            x_vals, y_vals = sol_vals[0], sol_vals[1]

            # Plot trajectory preview
            plt.clf()
            plt.figure(figsize=(8, 4.5))
            plt.plot(x_vals, y_vals, label=f'Trajectory (θ = {user_angle:.1f}°)')
            plt.axvline(self.target_x, color='green', linestyle='--', label='🎯 Target')
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

            # Log the result
            self.logger.log_throw(
                participant=person,
                theta_deg=user_angle,
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

            # In precise mode, update min/max bounds and print sorted
            if self.precise_mode:
                if error < 0 and (self.min_angle is None or user_angle > self.min_angle):
                    self.min_angle = user_angle
                elif error > 0 and (self.max_angle is None or user_angle < self.max_angle):
                    self.max_angle = user_angle

                if self.min_angle is not None and self.max_angle is not None:
                    low, high = sorted([self.min_angle, self.max_angle])
                    print(f"📉 The optimal angle is likely between ({low:.2f}°, {high:.2f}°)")

            # *** Histogram update runs every turn, not only in precise mode ***
            print("📊 Updating histograms...")
            if self.use_error_histogram:
                plot_error_histogram(
                    filepath='data/logs.csv',
                    threshold=self.hit_tolerance,
                    show_normalized=True
                )
            else:
                plot_hit_x_histogram(filepath='data/logs.csv')

            # Prompt to continue or quit, with validation
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

                # Final precise‐mode interval print, sorted
                if self.precise_mode:
                    print("\n🔍 Final interval estimate based on guesses:")
                    if self.min_angle is not None and self.max_angle is not None:
                        low, high = sorted([self.min_angle, self.max_angle])
                        print(f"   Estimated angle interval: ({low:.2f}°, {high:.2f}°)")
                    else:
                        print("   Not enough data to estimate an interval.")

                # Report *all* solutions rather than just one
                solutions = self.shooter.find_angle_solutions(
                    v0=self.v0,
                    target_x=self.target_x,
                    theta_bounds=(1, 89),
                    samples=181
                )
                if solutions:
                    sol_list = ", ".join(f"{s:.2f}°" for s in solutions)
                    print(f"\n📌 Launch angle(s) to hit {self.target_x} m: {sol_list}")
                else:
                    print(f"\n📌 No exact angle solutions found for {self.target_x} m.")

                # Offer the other histogram one last time
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
                break  # exit the while True

