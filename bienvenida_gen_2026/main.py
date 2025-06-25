# main.py

from core.launcher import SimulationLauncher
from core.session import GameSession

if __name__ == "__main__":
    # Step 1: Collect setup via launcher (includes k, m, x, and v0 now)
    launcher = SimulationLauncher()
    launcher.run()

    # Step 2: Extract components and values
    sim, shooter, selector, logger, v0, target_x, hit_tolerance, precise_mode, allow_repeats = launcher.get_components()

    # Step 3: Start main game session
    session = GameSession(
        sim=sim,
        shooter=shooter,
        selector=selector,
        logger=logger,
        v0=v0,
        target_x=target_x,
        hit_tolerance=hit_tolerance,
        precise_mode=precise_mode,
        allow_repeats=allow_repeats
    )
    session.run()
