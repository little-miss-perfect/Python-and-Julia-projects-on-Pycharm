import importlib
import timeit
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import root_scalar
from scipy.integrate import solve_bvp,  solve_ivp

from shared.derivative_functions import DerivativeFunctions
from shared.potential_extrema import PotentialDerivative, find_roots
from shared.scenario_data import Scenario


# TODO: give our code some modularity
scenarios_map = {
    "Hu_Sawicki":    "scenarios.Hu_Sawicki.f_functions",
    "alpha_L_L_M":   "scenarios.alpha_L_L_M.f_functions",
    "lambda_L_L_M":  "scenarios.lambda_L_L_M.f_functions",
                    }


chosen_scenario = "lambda_L_L_M"


# TODO: import the corresponding modules

# first create an object from the class with the important data to be used per "scenario"
scenario_mod = importlib.import_module(scenarios_map[chosen_scenario])  # this gives the scenario’s "scenario_data.py" module (which has the dictionary)

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

# next, a function to plot (for a quick visualization)
plot_mod = importlib.import_module("shared.plots")  # this gives the "plots.py" module (which contains a "plotting" function)
plot_func = plot_mod.plot_reg_func  # and here's said "plotting" function


# TODO: access the variables and functions in the dictionary and the class (for a specified scenario)

# # to access variables from a module we'll do something like:
# r0 = scene.r0
#
# # to access functions from a module we'll do something like:
# f = scene.f

# to access the functions defining the corresponding derivatives, from one of the classes, define the following:
d_f = DerivativeFunctions(scene.f, scene.f1, scene.f2, scene.f3, scene.f32, scene.rho, scene.xrho, scene.T)  # this gives us access to all the "derivative functions" as well as the "vectorized derivative" (which is used to solve the differential equation)

# to access the derivative of the potential (to find the extrema of the potential), from one of the classes, define the following:
der_pot = PotentialDerivative(scene.f, scene.f1)

dVdR = der_pot.dVdR  # this is just notation for us, it accesses the function "dVdR" in the corresponding class

# to access the vectorized derivative define the following:
F = d_f.F

# and for the change of variable to equivalently integrate over an infinite range, define the following:
G = d_f.G

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

# TODO: the potential (well, actually its derivative)
plot_func(
    g=dVdR,
    ind_var='R',
    min_val=-0.1e1,
    max_val=0.10e2,
    num_points=200,
            )

# maybe we could make this whole file into a class and in this "to do",
# first find the roots, then plot from the minimum ("min") of the roots to the maximum ("max") of the roots
# or plot within the interval "[min - epsilon, max + epsilon]" to get a better look at where the roots are

# TODO: about three minima for the potential


start = -0.05e2
stop = 0.15e2
num_points = 500

found_roots = find_roots(dVdR, start, stop, num_points)
print("Found roots:", found_roots)  # "found_roots" is a list containing the values of the roots found in the specified interval

# the roots we find are possible "limit values" of the solution to "R".
# the first root seems to be trivial (at zero)
# the second root might correspond to a local maximum
# but the third root might correspond to the nontrivial limit value we're looking for.
# anyway, always check with the corresponding plot of the potential (which we don't have, so... we need to ask her how we define those functions).
# so we'll try:

R_potential_min = found_roots[-1]

print("R_potential_min:", R_potential_min)

# TODO: solve_BVP, to find the correct initial value
# this is what we should've done from the get-go
# so let's start with the following:

# 3) Define the boundary condition function:
def bc(r_u0, r_u1):
    """
    r_u0 = r(u=0) = [n(0), m(0), R(0), R1(0), P(0), Ms(0), Mb(0)]
    r_u1 = r(u=1) = [n(∞), m(∞), R(∞), R1(∞), P(∞), Ms(∞), Mb(∞)]

    this function seems to allow "solve_bvp" to find the zeros of these expressions.
    in a way, we're saying "these are the best guesses of the values I know for each
    corresponding variable I'd like to consider in the initial condition"
    """
    residuals = []

    # Conditions at x=0 => u=0 (where the outputs of "r" are the same for either independent variable "x" or "u")
    # remember that we guess the initial condition to be "r0 = np.array([n0, m0, R0, DR0, P0, Ms0, Mb0], float)", so:
    residuals.append(r_u0[0] - scene.r0[0])  # n(0) - n0 = 0
    residuals.append(r_u0[1] - scene.r0[1])  # m(0) - m0 = 0
    residuals.append(r_u0[4] - scene.r0[4])  # P(0) - P0 = 0
    residuals.append(r_u0[5] - scene.r0[5])  # Ms(0) - Ms0 = 0
    residuals.append(r_u0[6] - scene.r0[6])  # Mb(0) - Mb0 = 0

    # Conditions at x->∞ => u=1
    residuals.append(r_u1[2] - R_potential_min)  # R(∞) - desired limit = 0
    residuals.append(r_u1[3] - 0)  # R1(∞) - 0 = 0  (i.e. the curve becomes horizontal at infinity)

    return np.array(residuals)

# 4) Make a mesh in u from 0 to 1:
u_mesh = np.linspace(0, 1 - 1e-10, 200)  # Avoid u = 1


# 5) Provide an initial guess for the solution shape: (7, len(u_mesh))
# For example, you might guess them all as constants or do something a bit smarter.
# remember that we guess the initial condition to be "r0 = np.array([n0, m0, R0, DR0, P0, Ms0, Mb0], float)", so:
r_guess = np.zeros((7, len(u_mesh)))
r_guess[0, :] = scene.r0[0]  # n0
r_guess[1, :] = scene.r0[1]  # m0
r_guess[2, :] = np.linspace(scene.r0[2], R_potential_min, len(u_mesh))  # R(u)
r_guess[3, :] = np.linspace(scene.r0[3], 0, len(u_mesh))  # R1(u)
r_guess[4, :] = scene.r0[4]  # P0
r_guess[5, :] = scene.r0[5]  # Ms0
r_guess[6, :] = scene.r0[6]  # Mb0


print("Initial guess for R(u):", r_guess[2, :])
print("Initial guess for R1(u):", r_guess[3, :])

# 6) Call solve_bvp using df.G (the chain-rule-wrapped derivative):
sol = solve_bvp(
    fun=d_f.G,    # dr/du
    bc=bc,       # boundary conditions function
    x=u_mesh,
    y=r_guess
)

# 7) Check whether the solver succeeded:
if sol.status != 0:
    print("Warning: solve_bvp did not converge to a solution.")
else:
    print("Success: solve_bvp converged.")

# 8) Evaluate the solution at desired points of u in [0,1].
u_fine = np.linspace(0, 1 - 1e-10, 300)  # Avoid u = 1
r_of_u = sol.sol(u_fine)  # shape: (7, len(u_fine))

# 9) Convert back to x if you want:
#    x = u / (1 - u)
eps = 1e-10  # Small epsilon to avoid division by zero
x_fine = u_fine / (1 - u_fine + eps)
r_of_x = r_of_u  # same array, just interpret the horizontal axis as x_fine. because all we did was "stretch/compress" the horizontal axis, not the vertical axis

# For convenience, you could do something like:
# n_of_x = r_of_x[0, :]
# m_of_x = r_of_x[1, :]
# R_of_x = r_of_x[2, :], etc.


# TODO: plot solve_BVP

# specifically want to see what the solver found at "u=0" (which corresponds to "x=0"), you can look at:
r0 = r_of_u[:, 0]  # or "r0 = sol.sol(0)"

# "r_guess" is your "initial guess" for the entire solution curve "r(u)".
# "r_of_u = sol.sol(u_fine)" is the actual solution that "solve_bvp" converged to.
# "r_of_u[:, 0]" is the portion of that solution at "u=0". That might differ our original guess if the solver adjusted it to meet the far-end boundary conditions at "u=1".

R_of_x = r_of_x[2, :]

fig, ax = plt.subplots()
ax.plot(x_fine, R_of_x)
ax.set_xlabel('distancia')
ax.set_ylabel('R')
ax.set_title('prueba')
ax.set_xscale('log')
plt.show()


# TODO: solve_IVP, to check that we have the correct initial value
# # this is what we were initially doing
#
# start_int = timeit.default_timer()
#
# sol = solve_ivp(
#             fun=F,
#             t_span=(0, 3e1),
#             y0=scene.r0,
#             method='DOP853',
#             #rtol=,
#             #atol=,
#             #events=,
#             #t_eval=,
#         )
#
# stop_int = timeit.default_timer()
#
# execution_time = stop_int - start_int
# print(f'it took "{execution_time}s" to integrate')
#
# x = sol.t
# r = sol.y
#
# fig, ax = plt.subplots()
# ax.plot(x, r[2, :])
# ax.set_xlabel('distancia')
# ax.set_ylabel('R')
# ax.set_title('prueba')
# ax.set_xscale('log')
# plt.show()
