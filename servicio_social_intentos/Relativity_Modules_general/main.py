import importlib
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate


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
scene_data = scenario_mod.scene_dict  # and this is said dictionary

# next, a function to plot
plot_mod = importlib.import_module("shared.plots")  # this gives the "plots.py" module (which contains a "plotting" function)
plot_func = plot_mod.plot_reg_func  # and here's said "plotting" function


# TODO: access the variables and functions in the dictionary (for a specified scenario)
R0 = scene_data["R0"] # a scenario’s initial conditions can be accessed like this
mHS = scene_data["mHS"]

f = scene_data["f"]
f1 = scene_data["f1"]
f2 = scene_data["f2"]
f3 = scene_data["f3"]

F  = scene_data["F"] # the scenario-specific ODE function


# TODO: maybe plot some given function

# the "f" function per "scenario"
plot_func(
    g=f,
    ind_var='R',
    min=-0.05e2,
    max=0.05e2,
    num_points=200,
            )

# the first derivative of "f(R)" should be positive (according to the paper)
plot_func(
    g=f1,
    ind_var='R',
    min=mHS,
    max=0.10e2,
    num_points=200,
            )

# the second derivative of "f(R)" should also be positive (according to the paper)
plot_func(
    g=f2,
    ind_var='R',
    min=mHS,
    max=0.10e2,
    num_points=200,
            )

# TODO: solve_IVP
# this is what we were initially doing


# TODO: solve_BVP
# this is what we should've done from the get-go


