from shared.scenario_data import load_scenario
from shared.plots import *
from shared.potential_extrema import PotentialDerivative, find_global_minimum
from scenarios.alpha_L_L_M.variables import R_star  # we need to be careful with the value of the logarithm
from shared.derivative_functions import DerivativeFunctions, refine_R0, find_valid_bracket, solve_ivp

import numpy as np


# TODO 1: choose a scenario
chosen_scenario = "alpha_L_L_M"  # we need to define this variable in order to make a comparison (between strings)
scene = load_scenario(chosen_scenario)  # "Hu_Sawicki", "alpha_L_L_M", "lambda_L_L_M"

# TODO 1.1: careful with "alpha_L_L_M"
# define the interval we’d like to try and search for the critical points of the potential associated to a minimum
proposed_bracket = (-10, 200)  #though we should state that: we haven't had the need to search in an interval "bigger than" the interval "(-1, 15)". but you never know...

if chosen_scenario == "alpha_L_L_M":
    start = -R_star + 0.1  # we need to only consider values of "R" such that "-R_star < R" (assuming that "0 < R_star")

    # check the lower end of the interval so it never falls below "–R_star"
    eps = 1e-8
    safe_bracket = (
        max(proposed_bracket[0], -R_star + eps),
        proposed_bracket[1]  # the upper end of the interval stays the same
                        )

else:
    start = -1  # defined as such because we haven't encountered a potential with critical points less than "-1"
    safe_bracket = proposed_bracket

# TODO 1.2: defining some variables
x_max = 1e12  # this shows up to where we truncate our "infinite" domain (although we haven't really had the need to go further than "10" to find a decent initial condition)
stop, num_points = 1e4, 50000  # for our "to do 4" (try and keep them in the same order of magnitude; "num_points" is to keep the interval "dense")
# although, for the previous line of code, we haven't had the need to search in an interval "bigger than" the interval "(-1, 15)"

# TODO 2: define the derivative functions to be used
d_f = DerivativeFunctions(scene.f, scene.f1, scene.f2, scene.f3, scene.f32, scene.rho, scene.xrho, scene.T)
F = d_f.F
p_d = PotentialDerivative(scene.f, scene.f1, scene.f2)
dVdR = p_d.dVdR

# TODO 3: find the minimum to the given potential (with root finding)

try:
    R_for_min_of_potential = find_global_minimum(p_d, start, stop, num_points)  # "start" depends on the chosen "scene"
    print(f'\n the nontrivial minimum of the potential is at "R = {R_for_min_of_potential:.3f}" \n')  # by "nontrivial minimum" we actually mean the extrema corresponding to a nonzero critical point (because that's how we were told to find this extremum)
except Exception as e:
    print(f"our root finding failed: {e}")
    exit(1)

stop = R_for_min_of_potential + 2  # defined as such because we haven't encountered a potential with more critical points after "R_for_min_of_potential" (which, up until now, has corresponded to the "maximum" of the set of critical points found)

# TODO 4.1: plot "V" vs "R"
#           (notice how up until now, all potential functions have an "upside down m" shape.
#            to see this, increase the size of the interval by decreasing the "start" and increasing the "stop" variables)
plot_potential(p_d, start, stop, num_points=1000)

# TODO 4.2: plot "dV/dR" vs "R"
R_vals    = np.linspace(start, stop, num_points)
dVdR_vals = [dVdR(R) for R in R_vals]

plot_potential_derivative(dVdR, start, stop, num_points)

# TODO 5: finding (and fine tuning) "R0"

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

print(f"\n Final R0: {optimal_R0:.15f} \n")

# now let's plot the final solution
r0_refined = scene.r0.copy()  # this is to not modify the current solution (it's just good practice)
r0_refined[2] = optimal_R0

# TODO 6: plot the "refinement"

# and now that we found a better initial value,
# we compute the solution with the refined "R0"
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

print(f"\n our solution approaches a value that is about"
      f" '{abs(R_for_min_of_potential - sol.y[2, -1]):.9f}' units away"
      f" from the target value at infinity \n")

# TODO 6.1: plot "P" vs "R"
prompt1 = "would you like to plot the pressure? press 'y' or 'n' to continue (i.e. choose 'yes' or 'no', respectively):   "
prompt2 = "would you like to plot the pressure? press 'y' or 'n' to continue:   "
inpt = input(prompt1)  # which returns a string

while inpt.lower() != "y" and inpt.lower() != "n":  # this means that as soon as the user's input matches one of the options (i.e. "y, n"), one of those two "!=" comparisons becomes "false", and since we use an "and": the entire statement becomes "false" and we exit the "while" loop

    input(prompt2)
    inpt = input(prompt2)

if inpt.lower() == "y":

    plt.figure()
    label = f'P(x), R0={optimal_R0:.3f}'
    plt.plot(sol.t, sol.y[4], label=label)  # to access what's going to be plotted
    plt.xscale('log')  # to better understand/visualize the behaviour of the solution
    plt.xlabel('x (distance)')
    plt.ylabel('P(x)')
    plt.title('refined solution for "P(x)"')
    plt.grid(False)
    plt.legend()
    plt.tight_layout()
    plt.show()
