import importlib
import numpy as np
import scipy.integrate as integrate
import scipy.optimize as optimize
import matplotlib.pyplot as plt

# Import shared modules
from shared.derivative_functions import DerivativeFunctions
from shared.potential_extrema import find_roots, PotentialDerivative
from shared.scenario_data import Scenario

# 🎯 STEP 1: Select a Scenario
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

# 🎯 STEP 3: Find the extrema of the function (assuming `find_extrema` does this)
start = -0.05e2
stop = 0.15e2
num_points = 500

found_roots = find_roots(dVdR, start, stop, num_points)
R_extrema = found_roots[-1]
print(f"Found extrema at: {R_extrema}")

# 🎯 STEP 4: Set up the system of ODEs using DerivativeFunctions
def ODE_system(x, r):
    """
    Converts the system into a format usable by `solve_bvp`.
    Uses the `F(x, r)` method from `DerivativeFunctions` for correct calculations.
    """
    return F(x, r)  # ✅ Calls the correct function


# 🎯 STEP 5: Define the boundary conditions for solve_bvp
# def bc(r_u0, r_u1):
#     """
#     Boundary conditions for the BVP.
#     - r_u0: r at u=0 (initial point)
#     - r_u1: r at u=1 (infinity)
#
#     This function ensures that:
#     - Initial conditions at x=0 are satisfied.
#     - Asymptotic conditions at x → ∞ are satisfied.
#     """
#     residuals = []
#
#     # Conditions at x=0 (initial conditions)
#     residuals.append(r_u0[0] - scene.r0[0])  # n(0) - n0 = 0
#     residuals.append(r_u0[1] - scene.r0[1])  # m(0) - m0 = 0
#     residuals.append(r_u0[4] - scene.r0[4])  # P(0) - P0 = 0
#     residuals.append(r_u0[5] - scene.r0[5])  # Ms(0) - Ms0 = 0
#     residuals.append(r_u0[6] - scene.r0[6])  # Mb(0) - Mb0 = 0
#
#     # Conditions at x->∞
#     residuals.append(r_u1[2] - R_extrema)  # R(∞) - desired limit = 0
#     residuals.append(r_u1[3] - 0)  # R1(∞) - 0 = 0  (function levels off)
#
#     return np.array(residuals)  # Ensure this returns a (7,) array

def bc(r_u0, r_u1):
    residuals = []

    # Initial conditions (allow small tolerance)
    residuals.append(r_u0[0] - scene.r0[0])
    residuals.append(r_u0[1] - scene.r0[1])
    residuals.append(r_u0[4] - scene.r0[4])
    residuals.append(r_u0[5] - scene.r0[5])
    residuals.append(r_u0[6] - scene.r0[6])

    # Final conditions (allow small tolerance)
    residuals.append((r_u1[2] - R_extrema) / 1e10)  # ✅ Rescaled to prevent huge errors
    residuals.append(r_u1[3] / 1e10)  # ✅ Relaxed constraints

    return np.array(residuals)


# 🎯 STEP 6: Solve the BVP
x_span = np.linspace(0, 5000, 300)  # ✅ More room, finer resolution
# initial_guess = np.random.uniform(low=-1e-3, high=1e-3, size=(7, x_span.size))  # ✅ Better guess
initial_guess = np.ones((7, x_span.size)) * 1e-3  # ✅ Small nonzero values


solution = integrate.solve_bvp(ODE_system, bc, x_span, initial_guess)

# 🎯 STEP 7: Plot Results
if solution.status == 0:
    print("BVP solver converged successfully.")
else:
    print("BVP solver did NOT converge.")

print("Solver status:", solution.status)
print("Solver message:", solution.message)
print("Max residual:", np.max(np.abs(solution.rms_residuals)))
print("Solution shape:", solution.y.shape)
print("Boundary conditions residual:", bc(solution.y[:, 0], solution.y[:, -1]))


plt.figure(figsize=(8, 5))
plt.plot(solution.x, solution.y[2], label="r[2] (Curvature Scalar)")
plt.axhline(R_extrema, color='r', linestyle='--', label=f"Extremum at {R_extrema:.4f}")
plt.xlabel("x")
plt.ylabel("r[2] (Curvature)")
plt.title("BVP Solution for r[2]")
plt.legend()
plt.grid(True)
plt.show()
