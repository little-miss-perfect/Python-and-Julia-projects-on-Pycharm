import importlib
import timeit
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import root_scalar
from scipy.integrate import solve_bvp,  solve_ivp

from shared.derivative_functions import DerivativeFunctions
from shared.potential_extrema import PotentialDerivative, find_roots


# TODO: give our code some modularity
scenarios_map = {
    "Hu_Sawicki": "scenarios.Hu_Sawicki.scenario_data",
    "alpha_L_L_M": "scenarios.alpha_L_L_M.scenario_data",
    "lambda_L_L_M": "scenarios.lambda_L_L_M.scenario_data",
                    }

chosen_scenario = "lambda_L_L_M"


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

# TODO: the potential (its derivative)
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
print("Found extrema at: R = ", found_roots)

# TODO: solve_IVP
# this is what we were initially doing

start_int = timeit.default_timer()

r0[2] = 2.289814669280
# newest values go from left to right (approaching the last root)

# para H-S usa estos valores # 12371.572599817799 # these values should approach "8.902634203309109"
# para la alpha usa estos valores # 1.660731799228 # these values should approach "1.4053829676864045"
# para la lamda usa estos valores # 2.289814669280 # these values should approach "1.983620395082102"

sol = solve_ivp(
            fun=F,
            t_span=(0, 1e7),
            y0=r0,
            method='DOP853',
            #rtol=,
            #atol=,
            #events=,
            #t_eval=,
        )

stop_int = timeit.default_timer()

execution_time = stop_int - start_int
print(f'it took "{execution_time}s" to integrate')

x = sol.t
r = sol.y

fig, ax = plt.subplots()
ax.plot(x, r[2, :])
ax.set_xlabel('distancia')
ax.set_ylabel('R')
ax.set_title('prueba')
ax.set_xscale('log')
plt.show()

print(f"it's integrating up to '({x[-1]}, {r[2, -1]})'")

# TODO: solve_BVP
# this is what we should've done from the get-go
