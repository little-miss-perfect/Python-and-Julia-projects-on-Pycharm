import importlib
import timeit
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import brentq

# ---------------------------------------------------------------------
# Import your scenario and derivative functions.
# ---------------------------------------------------------------------
from shared.derivative_functions import DerivativeFunctions, ShootingSolver
from shared.scenario_data import Scenario
from shared.potential_extrema import find_roots, PotentialDerivative  # Make sure this import exists

# Map your scenarios and choose one:
scenarios_map = {
    "Hu_Sawicki": "scenarios.Hu_Sawicki.f_functions",
    "alpha_L_L_M": "scenarios.alpha_L_L_M.f_functions",
    "lambda_L_L_M": "scenarios.lambda_L_L_M.f_functions",
}
chosen_scenario = "lambda_L_L_M"
scenario_mod = importlib.import_module(scenarios_map[chosen_scenario])

# Initialize scenario with module parameters
scene = Scenario(
    r0=scenario_mod.r0,
    R0=scenario_mod.R0,
    mHS=scenario_mod.mHS,
    rho=scenario_mod.rho,
    xrho=scenario_mod.xrho,
    T=scenario_mod.T,
    f=scenario_mod.f,
    f1=scenario_mod.f1,
    f2=scenario_mod.f2,
    f3=scenario_mod.f3,
    f32=scenario_mod.f32
)

# Set up derivative functions
d_f = DerivativeFunctions(scene.f, scene.f1, scene.f2, scene.f3, scene.f32,
                          scene.rho, scene.xrho, scene.T)
F = d_f.F

p_e = PotentialDerivative(scene.f, scene.f1)

dVdR = p_e.dVdR

# ---------------------------------------------------------------------
# Find potential minimum (ROOT FINDING)
# ---------------------------------------------------------------------
start = -0.05e2
stop = 0.15e2
num_points = 500
found_roots = find_roots(dVdR, start, stop, num_points)
R_potential_min = found_roots[-1]


# ---------------------------------------------------------------------
# SHOOTING METHOD IMPLEMENTATION
# ---------------------------------------------------------------------

class ShootingSolver:
    def __init__(self, F, base_r0, target, t_span=(0, 1e4),
                 method='DOP853', rtol=1e-6, atol=1e-9):
        self.F = F
        self.base_r0 = np.copy(base_r0)
        self.target = target
        self.t_span = t_span
        self.method = method
        self.rtol = rtol
        self.atol = atol
        self.component = 2  # Index for R0

    def _residual(self, R0_guess):
        r0 = np.copy(self.base_r0)
        r0[self.component] = R0_guess
        sol = solve_ivp(
            fun=self.F,
            t_span=self.t_span,
            y0=r0,
            method=self.method,
            rtol=self.rtol,
            atol=self.atol
        )
        return sol.y[self.component, -1] - self.target

    def solve(self, bracket, maxiter=100):
        root, result = brentq(
            self._residual,
            bracket[0],
            bracket[1],
            maxiter=maxiter,
            full_output=True
        )
        if not result.converged:
            raise RuntimeError(f"Convergence failed: {result.flag}")
        return root


# ---------------------------------------------------------------------
# BRACKET VALIDATION AND REFINEMENT
# ---------------------------------------------------------------------

def refine_R0(base_r0, target_R, initial_bracket, refinement_steps=3):
    solver = ShootingSolver(
        F=d_f.F,
        base_r0=base_r0,
        target=target_R,
        t_span=(0, 1e4),
        rtol=1e-6,
        atol=1e-6
    )

    current_R0 = np.nan
    current_bracket = initial_bracket

    for step in range(refinement_steps):
        # Validate bracket
        f_low = solver._residual(current_bracket[0])
        f_high = solver._residual(current_bracket[1])

        if np.sign(f_low) == np.sign(f_high):
            raise ValueError(
                f"Bracket {current_bracket} invalid. Residuals: [{f_low}, {f_high}]"
            )

        # Solve with current bracket
        try:
            current_R0 = solver.solve(bracket=current_bracket)
        except RuntimeError as e:
            print(f"Step {step + 1} failed: {e}")
            break

        # Narrow bracket
        delta = 10 ** (-step - 1) * (current_bracket[1] - current_bracket[0])
        current_bracket = (
            max(current_R0 - delta, current_bracket[0] * 0.9),
            min(current_R0 + delta, current_bracket[1] * 1.1)
        )

        print(f"Step {step + 1}: R0 = {current_R0:.12f}, Bracket: {current_bracket}")

    return current_R0


# ---------------------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------------------

# Initial parameters
initial_bracket = (1.9, 2.1)

# Validate initial bracket
solver = ShootingSolver(
    F=d_f.F,
    base_r0=scene.r0,
    target=R_potential_min,
    t_span=(0, 1e4)
)

f_a = solver._residual(initial_bracket[0])
f_b = solver._residual(initial_bracket[1])

print(f"Initial bracket residuals: f({initial_bracket[0]}) = {f_a:.3e}, "
      f"f({initial_bracket[1]}) = {f_b:.3e}")

if np.sign(f_a) == np.sign(f_b):
    print("⚠️ Initial bracket invalid. Expanding search range...")
    initial_bracket = (initial_bracket[0] * 0.5, initial_bracket[1] * 2.0)
    print(f"New bracket: {initial_bracket}")

# Run refinement
try:
    optimal_R0 = refine_R0(
        base_r0=scene.r0,
        target_R=R_potential_min,
        initial_bracket=initial_bracket,
        refinement_steps=4
    )
    print(f"\n✅ Final optimized R0: {optimal_R0:.15f}")
except Exception as e:
    print(f"\n❌ Error during refinement: {e}")

# ---------------------------------------------------------------------
# PLOTTING (uncomment when needed)
# ---------------------------------------------------------------------
# plotter = MultiSolutionRPlotter(solutions_list)
# plotter.plot_R_3D(component=2, x_log_scale=True, cmap='viridis')