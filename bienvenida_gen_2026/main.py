from core.launcher import SimulationLauncher
from core.session import GameSession

if __name__ == "__main__":
    # ────────────────────────────────────────────────────────────────────────────
    # USER GUIDE / PHYSICAL SETUP
    #
    # ➤ Coordinate System and Reference Frame
    #   • Origin (0,0) is the pivot point of your catapult arm.
    #   • +x axis: horizontal to the right from the pivot.
    #   • +y axis: vertical upward.
    #
    # ➤ Energy & Launch Speed
    #   The bungee cord (spring) stores energy ½·k·x² when stretched by x = (stretched_length − l0).
    #   That energy converts to projectile kinetic energy ½·m·v0² →
    #     v0 = √(k/m) · x.
    #
    # ➤ SETUP-PHASE INPUTS (asked once at start)
    #   1. Precise mode? (y/n)
    #        – If yes, we’ll keep track of under- and overshoots to narrow the true angle interval.
    #   2. Allow repeats? (y/n)
    #        – Can participants shoot more than once?
    #   3. Clear logs? (y/n)
    #        – Deletes data/logs.csv & data/leaderboard.csv before starting.
    #   4. # of participants (integer)
    #        – How many people will take a turn?
    #   5. Use saved spring constant k? (y/n)
    #       • If yes, pick one from experimental/data/processed/…
    #       • If no or none saved, enter manually:
    #   6. Spring constant k (N/m)
    #       – Hooke’s-law constant of your bungee cord.
    #   7. Unstretched length l0 (m)
    #       – Natural length of the cord (no tension).
    #   8. Projectile mass m (kg)
    #       – Mass of the stone/ball you’re launching.
    #   9. Stretch distance x (m)
    #       – Extra length you pull the cord beyond l0 before release.
    #  10. Time‐marker Δt (s)
    #       – Interval between red dots on each trajectory plot.
    #  11. Target distance target_x (m)
    #       – Horizontal distance from pivot to your target (must be ≤ max range).
    #
    # ➤ PER-SHOT INPUTS (asked once per turn)
    #   A. Arm-orientation φ (° CCW from +x; 90° ≤ φ ≤ 180°)
    #        – φ=180° → arm horizontal (fully back), φ= 90° → vertical up.
    #        – Internally we convert θ = φ − 90° to feed into the sim (θ = launch angle from +x).
    #   B. Actual landing point hit_x (m)
    #        – Where the projectile actually hit (x on the ground).
    #
    # That’s **all** the inputs you’ll ever type.  Enjoy plotting & guessing your way
    # to the perfect launch angle!
    # ────────────────────────────────────────────────────────────────────────────

    # Step 1: Initialize launcher and collect setup from user
    launcher = SimulationLauncher()
    launcher.run()

    # Step 2: Get all initialized components (now including time_sep)
    sim, shooter, selector, logger, v0, target_x, hit_tolerance, precise_mode, allow_repeats, time_sep = launcher.get_components()

    # Step 3: Launch the main session loop, passing time_sep
    session = GameSession(
        sim=sim,
        shooter=shooter,
        selector=selector,
        logger=logger,
        v0=v0,
        target_x=target_x,
        hit_tolerance=hit_tolerance,
        precise_mode=precise_mode,
        allow_repeats=allow_repeats,
        time_sep=time_sep       # new parameter here
    )
    session.run()
