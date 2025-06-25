# main.py

from core.launcher import SimulationLauncher
from core.session import GameSession

if __name__ == "__main__":
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
