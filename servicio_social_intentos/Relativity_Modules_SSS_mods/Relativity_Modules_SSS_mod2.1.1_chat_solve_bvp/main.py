import importlib
import timeit
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_bvp, solve_ivp
from scipy.interpolate import interp1d

from shared.derivative_functions import DerivativeFunctions
from shared.potential_extrema import PotentialDerivative, find_roots
from shared.scenario_data import Scenario

# -------------------------------------------------------
# Step 1: Create the scenario
# -------------------------------------------------------
scenarios_map = {
    "Hu_Sawicki": "scenarios.Hu_Sawicki.f_functions",
    "alpha_L_L_M": "scenarios.alpha_L_L_M.f_functions",
    "lambda_L_L_M": "scenarios.lambda_L_L_M.f_functions",
}
chosen_scenario = "lambda_L_L_M"

scenario_mod = importlib.import_module(scenarios_map[chosen_scenario])
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

# ODE definitions
d_f = DerivativeFunctions(scene.f, scene.f1, scene.f2, scene.f3, scene.f32,
                          scene.rho, scene.xrho, scene.T)
F = d_f.F  # this is the derivative wrt x

# Potential derivative (just for reference)
der_pot = PotentialDerivative(scene.f, scene.f1)
dVdR = der_pot.dVdR

# Find potential-min root
found_roots = find_roots(dVdR, -5.0, 15.0, 500)
R_potential_min = found_roots[-1]
print("R_potential_min=", R_potential_min)

# -------------------------------------------------------
# Step 2: Solve IVP up to x_max, if desired, for a better guess
# -------------------------------------------------------
x_max = 1e1
y0_ivp = scene.r0  # The initial condition at x=0
sol_ivp = solve_ivp(
    fun=F,
    t_span=(0, x_max),
    y0=y0_ivp,
    method='DOP853'
)
x_ivp = sol_ivp.t  # shape (N,)
r_ivp = sol_ivp.y  # shape (7, N)

# -------------------------------------------------------
# Step 3: Build a mesh in x, from 0 to x_max
# -------------------------------------------------------
x_mesh = np.linspace(0, x_max, 500)

# -------------------------------------------------------
# Step 4: Create an initial guess by interpolating IVP solution onto x_mesh
# -------------------------------------------------------
r_guess = np.zeros((7, len(x_mesh)))

# If the IVP succeeded in that range, we can just do an interpolation
# (If it fails or stops early, you might do something else.)
interp_funcs = []
for comp in range(7):
    interp_funcs.append(
        interp1d(x_ivp, r_ivp[comp, :], kind='cubic', fill_value='extrapolate')
    )
for comp in range(7):
    r_guess[comp, :] = interp_funcs[comp](x_mesh)


# -------------------------------------------------------
# Step 5: Define boundary conditions at x=0 and x=x_max
# -------------------------------------------------------
def bc(r_x0, r_xmax):
    """
    r_x0   = [n(0), m(0), R(0), R1(0), P(0), Ms(0), Mb(0)]
    r_xmax = [n(x_max), m(x_max), R(x_max), R1(x_max), P(x_max), Ms(x_max), Mb(x_max)]
    """
    res = []

    # At x=0
    res.append(r_x0[0] - scene.r0[0])  # n(0)
    res.append(r_x0[1] - scene.r0[1])  # m(0)
    res.append(r_x0[4] - scene.r0[4])  # P(0)
    res.append(r_x0[5] - scene.r0[5])  # Ms(0)
    res.append(r_x0[6] - scene.r0[6])  # Mb(0)

    # At x=x_max, we want R ~ R_potential_min and R'(x_max)=0
    # We'll approximate that as R(x_max) - R_potential_min = 0, R1(x_max)=0
    res.append(r_xmax[2] - R_potential_min)
    res.append(r_xmax[3] - 0.0)

    return np.array(res)


# -------------------------------------------------------
# Step 6: Solve the BVP using solve_bvp in terms of x
# -------------------------------------------------------
# The "fun" we pass to solve_bvp should accept x (shape (N,)) and y (shape (7, N)),
# and return dy/dx (shape (7,N)). That's exactly how d_f.F is structured.
sol_bvp = solve_bvp(
    fun=F,  # the derivative wrt x
    bc=bc,
    x=x_mesh,
    y=r_guess
)

# -------------------------------------------------------
# Step 7: Check results
# -------------------------------------------------------
if sol_bvp.status != 0:
    print("Warning: solve_bvp did not converge.")
else:
    print("Success: solve_bvp converged!")

# Evaluate the BVP solution at a finer mesh
x_fine = np.linspace(0, x_max, 300)
r_bvp = sol_bvp.sol(x_fine)
R_bvp = r_bvp[2, :]  # Suppose the 3rd component is R

# Plot
plt.figure()
plt.plot(x_fine, R_bvp, label='BVP solution for R(x)')
plt.xscale('log')
plt.xlabel('x')
plt.ylabel('R')
plt.grid()
plt.legend()
plt.show()
