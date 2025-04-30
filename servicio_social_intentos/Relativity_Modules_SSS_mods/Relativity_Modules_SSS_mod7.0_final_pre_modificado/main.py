from shared.scenario_data import load_scenario
from shared.plots import plot_potential_derivative, plot_refined_solution
from shared.potential_extrema import PotentialDerivative, find_global_minimum
from scenarios.alpha_L_L_M.variables import R_star  # we need to be careful with the value of the logarithm
from shared.derivative_functions import DerivativeFunctions, refine_R0, find_valid_bracket, solve_ivp

import numpy as np


# TODO 1: choose a scenario
chosen_scenario = "alpha_L_L_M"  # we need to define this variable in order to make a comparison (between strings)
scene = load_scenario(chosen_scenario)  # "Hu_Sawicki", "alpha_L_L_M", "lambda_L_L_M"

# TODO 1.1: careful with "alpha_L_L_M"
# define the raw bracket we’d like to try
proposed_bracket = (0.1, 200)

if chosen_scenario == "alpha_L_L_M":
    start = -R_star + 0.1  # we need to only consider values of "R" such that "-R_star < R" (assuming that "0 < R_star")

    # check the lower end of the interval so it never falls below "–R_star"
    eps = 1e-8
    safe_bracket = (
        max(proposed_bracket[0], -R_star + eps),
        proposed_bracket[1]  # the upper end of the interval stays the same
    )

else:
    start = -0.05e1
    safe_bracket = proposed_bracket

# TODO 1.2: defining some variables
x_max = 1e12  # this shows up to where we truncate our "infinite" domain
stop, num_points = 0.15e2, 500  # for our "to do 4"

# TODO 2: define the derivative functions to be used
d_f = DerivativeFunctions(scene.f, scene.f1, scene.f2, scene.f3, scene.f32, scene.rho, scene.xrho, scene.T)
F = d_f.F
p_d = PotentialDerivative(scene.f, scene.f1, scene.f2)
dVdR = p_d.dVdR

# TODO 4: find the minimum to the given potential (with root finding)

try:
    R_for_min_of_potential = find_global_minimum(p_d, start, stop, num_points)  # "start" depends on the chosen "scene"
    print(f'the nontrivial minimum of the potential is at "R = {R_for_min_of_potential:.5f}"')
except Exception as e:
    print(f"our root finding failed: {e}")
    exit(1)

# TODO 4.1: plot "dV/dR" vs "R"
R_vals    = np.linspace(start, stop, num_points)
dVdR_vals = [dVdR(R) for R in R_vals]

plot_potential_derivative(dVdR, start, stop, num_points)

# TODO 7: finding (and fine tuning) "R0"

initial_bracket = find_valid_bracket(
    F              = F,
    base_r0        = scene.r0,
    target         = R_for_min_of_potential,
    initial_bracket= safe_bracket,  # the interval where we decide to "refine" the value of "R0"
    x_max          = x_max
)

optimal_R0 = refine_R0(
    base_r0        = scene.r0,
    target_R       = R_for_min_of_potential,
    initial_bracket= initial_bracket,
    F              = F,
    x_max          = x_max,
    refinement_steps= 10,
    tol_residual=1e-6
)

print(f"\n Final R0: {optimal_R0:.15f}")

# now let's plot the final solution
r0_refined = scene.r0.copy()  # this is to not modify the current solution
r0_refined[2] = optimal_R0

# TODO 8: plot the "refinement"

# and now we compute the solution with the refined "R0"
sol = solve_ivp(
    fun    = F,
    t_span = (0, x_max),
    y0     = r0_refined,
    method = 'DOP853',
    rtol   = 1e-6,
    atol   = 1e-9
)

# and, finally, we plot "R(x)"
plot_refined_solution(sol, R_for_min_of_potential, optimal_R0)
