from shared.scenario_data import load_scenario
from shared.plots import *
from shared.potential_extrema import PotentialDerivative, find_global_minimum
from scenarios.alpha_L_L_M.variables import R_star  # we need to be careful with the value of the logarithm
from shared.derivative_functions import DerivativeFunctions, refine_R0, find_valid_bracket, solve_ivp

import numpy as np


# TODO 1: choose a scenario interactively
# add the names of current "models" (which are stored in the "scenarios" directory) to this following list
valid = ["Hu_Sawicki", "alpha_L_L_M", "lambda_L_L_M"]  # if you add a scenario/model (using the template in the directory "scenarios") then: add the name of that directory to this list
prompt1 = f"choose a scenario ({', '.join(valid)}): "  # join the strings using a comma
prompt2 = f"that's an invalid choice. the choices are {', '.join(valid)}: "

# first let's ask for a scenario
inpt = input(prompt1).strip()  # "strip" is just in case the user types something like " alpha_L_L_M" or maybe they type "alpha_L_L_M " (it'll remove those blank spaces and then compare). this method is here because we already encountered that small annoying bug of "not typing exactly what is needed", even by accident

# and keep asking while the user doesn't give a valid option
while inpt != valid[0] and inpt != valid[1] and inpt != valid[2]:
    inpt = input(prompt2).strip()

# once we have a valid string, assign and load
chosen_scenario = inpt
scene = load_scenario(chosen_scenario)

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

# TODO 6.1: interactively plot any of the 7 solution components
# since "r = [n, m, R, DR, P, Ms, Mb]", then we define
components = [
    ("n",  0, "n(x)"),
    ("m",  1, "m(x)"),  # if this component is not showing the expected plot, then try changing the default integration method used in "solve_ivp" in the file "derivative_functions.py" (even if the integration takes a bit longer)
    ("R",  2, "R(x)"),
    ("DR", 3, "dR/dx"),
    ("P",  4, "P(x)"),
    ("Ms", 5, "M_s(x)"),
    ("Mb", 6, "M_b(x)"),
]

for name, idx, ylabel in components:
    prompt1 = f"would you like to plot '{name}(x)'?  y/n (or 'q' to quit plotting):  "
    prompt2 = f"that was an invalid input. would you like to plot '{name}(x)'? type y/n/q:  "
    choice = input(prompt1).strip().lower()  # we use "lower()" in case the user types "Y" or "N"

    while choice not in ("y", "n", "q"):
        choice = input(prompt2).strip().lower()

    if choice == "q":
        print("exiting the plotting loop. thanks for using this program :)")
        break   # which exits the "for" loop entirely

    if choice == "y":
        plt.figure()
        plt.plot(sol.t, sol.y[idx], label=f"{ylabel}, R0={optimal_R0:.3f}")
        plt.xscale("log")
        plt.xlabel("x (distance)")
        plt.ylabel(ylabel)
        plt.title(f"the refined solution for {ylabel}")
        plt.grid(False)
        plt.legend()
        plt.tight_layout()
        plt.show()
