import importlib
import timeit
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ---------------------------------------------------------------------
# Import your scenario and derivative functions.
# ---------------------------------------------------------------------
from shared.derivative_functions import DerivativeFunctions, ShootingSolver
from shared.scenario_data import Scenario
from shared.potential_extrema import find_roots, PotentialDerivative

# Map your scenarios and choose one:
scenarios_map = {
    "Hu_Sawicki": "scenarios.Hu_Sawicki.f_functions",
    "alpha_L_L_M": "scenarios.alpha_L_L_M.f_functions",
    "lambda_L_L_M": "scenarios.lambda_L_L_M.f_functions",
}
chosen_scenario = "Hu_Sawicki"
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

x_max = 1e12  # this shows up to where we truncate our "infinite" domain

# ---------------------------------------------------------------------
# Find potential minimum (ROOT FINDING)
# ---------------------------------------------------------------------
start = -0.05e2
stop = 0.15e2
num_points = 500
try:
    found_roots = find_roots(dVdR, start, stop, num_points)
    R_potential_min = found_roots[-1]  # always use the last root. the first corresponds to a minimum at zero (which is trivial), the second is a local maximum, which forces the last to be a local minimum (if the potential always "increases")
    print(f"R_potential_min = {R_potential_min:.3e}")
    if R_potential_min < 0:
        raise ValueError("Non-physical target (R_potential_min < 0)")
except Exception as e:
    print(f"Root finding failed: {e}")
    exit(1)


# ---------------------------------------------------------------------
# SHOOTING METHOD IMPLEMENTATION (UPDATED)
# ---------------------------------------------------------------------
class ShootingSolver:
    def __init__(self, F, base_r0, target, t_span=(0, x_max),  # Increased to 1e5
                 method='DOP853', rtol=1e-6, atol=1e-9):
        self.F = F
        self.base_r0 = np.copy(base_r0)
        self.target = target
        self.t_span = t_span
        self.method = method
        self.rtol = rtol
        self.atol = atol
        self.component = 2

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
# BRACKET VALIDATION AND REFINEMENT (UPDATED)
# ---------------------------------------------------------------------
def refine_R0(base_r0, target_R, initial_bracket, refinement_steps=9):
    solver = ShootingSolver(
        F=d_f.F,
        base_r0=base_r0,
        target=target_R,
        t_span=(0, x_max),  # Increased integration range
        rtol=1e-6,
        atol=1e-6
    )

    current_R0 = np.nan
    current_bracket = initial_bracket

    for step in range(refinement_steps):
        f_low = solver._residual(current_bracket[0])
        f_high = solver._residual(current_bracket[1])

        if np.sign(f_low) == np.sign(f_high):
            # Diagnostic plot
            debug_R0s = np.linspace(current_bracket[0], current_bracket[1], 5)
            plt.figure()
            for R0_debug in debug_R0s:
                r0 = base_r0.copy()
                r0[2] = R0_debug
                sol = solve_ivp(F, (0, 1e5), r0, method='DOP853')
                plt.plot(sol.t, sol.y[2], label=f"R0={R0_debug:.1f}")
            plt.axhline(target_R, color='k', linestyle='--', label='Target')
            plt.xscale('log')
            plt.legend()
            plt.title(f"Step {step + 1} Diagnostic: R0 ∈ [{current_bracket[0]:.1f}, {current_bracket[1]:.1f}]")
            plt.show()

            raise ValueError(f"Bracket invalid. Residuals: [{f_low:.3e}, {f_high:.3e}]")

        try:
            current_R0 = solver.solve(bracket=current_bracket)
        except RuntimeError as e:
            print(f"Step {step + 1} failed: {e}")
            break

        delta = 10 ** (-step - 2) * (current_bracket[1] - current_bracket[0])

        current_bracket = (
            max(current_R0 - delta, current_bracket[0] * 0.8),  # Less aggressive narrowing
            min(current_R0 + delta, current_bracket[1] * 1.2)
        )

        print(f"Step {step + 1}: R0 = {current_R0:.12f}, Bracket: {current_bracket}")

    return current_R0


# ---------------------------------------------------------------------
# MAIN EXECUTION (UPDATED)
# ---------------------------------------------------------------------
initial_bracket = (0.1, 1e3)
solver = ShootingSolver(
    F=d_f.F,
    base_r0=scene.r0,
    target=R_potential_min,
    t_span=(0, x_max)
)

try:
    f_a = solver._residual(initial_bracket[0])
    f_b = solver._residual(initial_bracket[1])

    print(f"Initial residuals: f({initial_bracket[0]}) = {f_a:.3e}, f({initial_bracket[1]}) = {f_b:.3e}")

    if np.sign(f_a) == np.sign(f_b):
        print("⚠️ Expanding search range...")
        expansion_factor = 2.0
        max_expansions = 10  # Increased from 5
        for i in range(max_expansions):
            initial_bracket = (
                initial_bracket[0] / expansion_factor,
                initial_bracket[1] * expansion_factor + 10 ** i  # Add positive increment
            )
            f_a = solver._residual(initial_bracket[0])
            f_b = solver._residual(initial_bracket[1])
            print(f"Try {i + 1}: bracket={initial_bracket}, residuals=[{f_a:.3e}, {f_b:.3e}]")
            if np.sign(f_a) != np.sign(f_b):
                break
        else:
            raise ValueError(
                "No valid bracket found. Check: 1) Integration range 2) Target validity 3) Scenario parameters")

    optimal_R0 = refine_R0(
        base_r0=scene.r0,
        target_R=R_potential_min,
        initial_bracket=initial_bracket,
        refinement_steps=5  # Increased refinement steps
    )
    print(f"\n✅ Final R0: {optimal_R0:.15f}")

except Exception as e:
    print(f"\n❌ Critical error: {e}")
    print("Recommendations:")
    print("1. Verify scenario parameters in variables.py")
    print("2. Check potential minimum calculation")
    print("3. Increase t_span further if needed")
