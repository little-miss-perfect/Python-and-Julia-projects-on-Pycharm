import importlib
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import root_scalar
from scipy.integrate import solve_bvp

from shared.derivative_functions import DerivativeFunctions
from shared.potential_extrema import PotentialDerivative, find_roots


# TODO: give our code some modularity
scenarios_map = {
    "Hu_Sawicki": "scenarios.Hu_Sawicki.scenario_data",
    "alpha_L_L_M": "scenarios.alpha_L_L_M.scenario_data",
    "lambda_L_L_M": "scenarios.lambda_L_L_M.scenario_data",
                    }

chosen_scenario = "Hu_Sawicki"


# TODO: import the corresponding modules

# first the dictionary with the important data to be used per "scenario"
scenario_mod = importlib.import_module(scenarios_map[chosen_scenario])  # this gives the scenario’s "scenario_data.py" module (which has the dictionary)
scene_data = scenario_mod.scene_dict  # and this is said dictionary: "scene_dict"

# next, a function to plot
plot_mod = importlib.import_module("shared.plots")  # this gives the "plots.py" module (which contains a "plotting" function)
plot_func = plot_mod.plot_reg_func  # and here's said "plotting" function


# TODO: access the variables and functions in the dictionary and the class (for a specified scenario)

# from the dictionary:

r0 = scene_data["r0"]

R0 = scene_data["R0"] # a scenario’s initial conditions can be accessed like this
mHS = scene_data["mHS"]

rho = scene_data["rho"]
xrho = scene_data["xrho"]
T = scene_data["T"]

f = scene_data["f"]
f1 = scene_data["f1"]
f2 = scene_data["f2"]
f3 = scene_data["f3"]
f32 = scene_data["f32"]

# from the class:

d_f = DerivativeFunctions(f, f1, f2, f3, f32, rho, xrho, T)  # this gives us access to all the "derivative functions" as well as the "vectorized derivative" (which is used to solve the differential equation)

p_e = PotentialDerivative(f, f1)

dVdR = p_e.dVdR

F = d_f.F

# TODO: maybe plot some given function

# # the "f" function per "scenario"
# plot_func(
#     g=f,
#     ind_var='R',
#     min_val=-0.05e2,
#     max_val=0.05e2,
#     num_points=200,
#             )
#
# # the first derivative of "f(R)" should be positive (according to the paper)
# plot_func(
#     g=f1,
#     ind_var='R',
#     min_val=mHS,
#     max_val=0.10e2,
#     num_points=200,
#             )
#
# # the second derivative of "f(R)" should also be positive (according to the paper)
# plot_func(
#     g=f2,
#     ind_var='R',
#     min_val=mHS,
#     max_val=0.10e2,
#     num_points=200,
#             )

# TODO: the potential
plot_func(
    g=dVdR,
    ind_var='R',
    min_val=-0.1e2,
    max_val=0.15e2,
    num_points=200,
            )


# TODO: about three minima for the potential


start = -0.05e2
stop = 0.15e2
num_points = 500

found_roots = find_roots(dVdR, start, stop, num_points)
print("Found roots:", found_roots)

# TODO: solve_IVP
# this is what we were initially doing


# TODO: solve_BVP
# this is what we should've done from the get-go


Rlim = found_roots[1]    # Suppose as x->infinity, R->0
Xmax = 10.0   # We'll treat x=10 as "effectively infinity"

def bvp_system(x, Y):
    """
    x: array of shape (M,)
    Y: array of shape (7, M)  [since we have 7 unknowns]
    Returns: dY/dx, shape (7, M)
    """
    dY = np.zeros_like(Y)
    for i in range(x.size):
        # Extract the state [n, m, R, R1, P, Ms, Mb] at x[i]
        r = Y[:, i]
        # Evaluate the derivative using df.F(...)
        dY[:, i] = F(x[i], r)
    return dY

def bc(ya, yb):
    """
    ya = Y[:, 0] -> solution at x=0
    yb = Y[:, -1] -> solution at x=Xmax
    We'll impose:
        ya[0] = n0   -> n(0) = n0
        ya[1] = m0   -> m(0) = m0
        yb[2] = Rlim -> R(Xmax) = Rlim
    Fill in more as needed for your system.
    """
    return np.array([
        ya[0] - r0[0],  # n(0) - n0 = 0
        ya[1] - r0[1],  # m(0) - m0 = 0
        ya[2] - r0[2],
        ya[3] - r0[3],
        ya[4] - r0[4],
        ya[5] - r0[5],
        ya[6] - r0[6],

        yb[2] - Rlim,  # R(Xmax) - Rlim = 0
        yb[3] - 0,
        yb[4] - 0  # P(Xmax)=0 => yb[4] - 0 = 0
        # If you have more conditions, add them here
    ])


M = 50  # number of mesh points
x_guess = np.linspace(0, Xmax, M)

# shape (7, M) since we have 7 unknowns
y_guess = np.zeros((7, M))

# Provide a *rough guess* for each variable over the mesh:
# For instance, let's guess everything is constant:
# n(x) ~ n0, m(x) ~ m0, R(x) ~ Rlim, etc.
# Tweak as needed for your problem.

y_guess[0, :] = r0[0]
y_guess[1, :] = r0[1]
y_guess[2, :] = Rlim  # R
y_guess[3, :] = r0[3]   # R1
y_guess[4, :] = r0[4]   # P
y_guess[5, :] = r0[5]   # Ms
y_guess[6, :] = r0[6]   # Mb

sol = solve_bvp(bvp_system, bc, x_guess, y_guess)

# Check if it converged
if sol.status != 0:
    print("solve_bvp did NOT converge; status:", sol.status)
    print("Message:", sol.message)
else:
    print("BVP solved successfully. Message:", sol.message)

# -----------------------------------------
# 7) USE THE SOLUTION
# -----------------------------------------
# sol.x -> array of mesh points
# sol.y -> array of shape (7, len(sol.x)) with the solution
# Example: let's label them
n_sol  = sol.y[0, :]
m_sol  = sol.y[1, :]
R_sol  = sol.y[2, :]
R1_sol = sol.y[3, :]
P_sol  = sol.y[4, :]
Ms_sol = sol.y[5, :]
Mb_sol = sol.y[6, :]

# Plot a couple of them:
plt.plot(sol.x, R_sol, label="R(x)")
plt.plot(sol.x, P_sol, label="P(x)")
plt.legend()
plt.xlabel("x")
plt.ylabel("Solution variables")
plt.title("BVP Solution")
plt.show()
