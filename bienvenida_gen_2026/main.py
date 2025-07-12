from core.launcher import SimulationLauncher
from core.session import GameSession

# ────────────────────────────────────────────────────────────────────────────
# USER GUIDE / PHYSICAL SETUP
#
# ➤ Coordinate System and Reference Frame
#   • Origin (0,0) is the pivot point of your catapult arm.
#   • +x axis: horizontal to the right from the pivot.
#   • +y axis: vertical upward.
#
# ➤ Energy & Launch Speed
#   The bungee cord (spring) stores energy ½·k·x² when stretched by
#     x = (stretched_length − l₀).
#   That energy converts into projectile kinetic energy ½·m·v₀² →
#     v₀ = √(k/m) · x.
#
# ➤ SETUP-PHASE INPUTS (asked once at start)
#   1. Precise mode? (y/n)
#      – If yes, under-/overshoots will narrow a θ-interval estimate.
#   2. Allow repeats? (y/n)
#      – Can participants shoot more than once?
#   3. Clear logs? (y/n)
#      – Deletes data/logs.csv & data/leaderboard.csv before starting.
#   4. Number of participants (integer)
#      – How many people will each take one guess per turn.
#   5. Use saved spring constant k? (y/n)
#      – If yes, choose from experimental/data/processed/…
#   6. Spring constant k (N/m)
#      – Hooke’s-law constant of your bungee cord.
#   7. Unstretched length l₀ (m)
#      – Natural (no-tension) length of the cord.
#   8. Projectile mass m (kg)
#      – Mass of the stone/ball you’re launching.
#   9. Stretch distance x (m)
#      – How far beyond l₀ you pull the cord before release.
#  10. Time-marker Δt (s)
#      – Interval between red dots on each trajectory plot.
#  11. Target distance target_x (m)
#      – Horizontal distance from pivot to your target (≤ max range).
#
# ➤ SESSION-PHASE INPUTS (asked once per session)
#  A. Histogram mode (A/B)
#      [A] Absolute‐error vs. target
#      [B] Landing‐positions (x)
#  B. Reveal true optimal angle φ*? (y/n)
#      – If yes, φ* (one or two solutions) is printed once before guessing.
#
# ➤ PER-SHOT INPUTS (asked once per turn)
#  I.  Arm-orientation φ (° CCW from +x; 90° ≤ φ ≤ 180°)
#      – φ=180° → arm fully back (horizontal); φ=90° → straight up.
#      – Internally we convert θ = φ − 90° to feed into the sim.
# II. Actual landing point hit_x (m)
#      – Measured horizontal distance from pivot where it landed.
#
# That’s **all** the inputs you’ll ever type. Enjoy plotting & guessing your way
# to the perfect launch angle!
# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    launcher = SimulationLauncher()
    launcher.run()

    # Step 2: Get all initialized components (now including time_sep)
    sim, shooter, selector, logger, v0, target_x, hit_tolerance, precise_mode, allow_repeats, time_sep, max_range = launcher.get_components()

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
        time_sep=time_sep,       # new parameter here
        max_range=max_range,
    )
    session.run()
