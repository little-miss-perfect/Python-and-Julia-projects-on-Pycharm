import numpy as np
import matplotlib.pyplot as plt

def plot_potential(p, start, stop, num_points=500, R_ref=None):
    """
    defined to plot the potential "V(R) - V(R_ref)" vs "R" over "[start, stop]"
    given a reference point, which makes it so that the solution only differs
    by a constant from other solutions
    (but we don't need to worry about that since we're interested in its derivative; we consider this constant to be zero)

    :param p: an instance of the class "PotentialDerivative"
    :param start: lower bound of the interval (by default it's "0" if "R_ref = None")
    :param stop: upper bound of the interval
    :param num_points: number of points in the plot
    :param R_ref: reference "R" value for "V(R_ref)"; if it's "None", it uses "0" by default
    """

    # reference point
    R0_ref = 0 if R_ref is None else R_ref

    # define the points to be plotted
    R_vals = np.linspace(start, stop, num_points)  # the independent variables
    V_vals = [p.V(R, R0_ref) for R in R_vals]  # the dependent variables

    plt.figure()
    label = f'V(R) - V({R_ref})' if R_ref is not None else 'V(R) - V(0)'
    plt.plot(R_vals, V_vals, label=label)
    plt.axhline(p.V(R0_ref, R0_ref), linestyle=':', color='black')
    plt.xlabel('R')
    plt.ylabel('V(R)')
    plt.title('potential')
    plt.grid(False)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_potential_derivative(dVdR, start, stop, num_points=500):
    """
    defined to plot "dV/dR" vs "R" over the interval "[start, stop]",
    with a dotted horizontal line at zero
    to visualize where the critical points are

    :param dVdR: a function to plot; preferably "dV/dR"
    :param start: the start of the interval
    :param stop: the end of the interval
    :param num_points: the number of points to plot
    """

    # define the points to be plotted
    R_vals    = np.linspace(start, stop, num_points)
    dVdR_vals = [dVdR(R) for R in R_vals]

    plt.figure()
    plt.plot(R_vals, dVdR_vals, label='dV/dR')
    plt.axhline(0, linestyle=':', color='black')
    plt.xlabel('R')
    plt.ylabel('dV/dR')
    plt.title('derivative of the potential')
    plt.grid(False)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_refined_solution(sol, R_target, label_R0=None):
    """
    defined to plot the "Ricci-scalar" solution "sol.y[2]" vs "sol.t"
    on a log scale for the independent variable,
    with a dotted horizontal line at "R_target"
    (which shows how we approach the De Sitter condition)

    :param sol: the output of "solve_ivp", once we've found a refined initial condition
    :param R_target: the "R" value we want our solution to approach (considering the De Sitter condition)
    :param label_R0: it represents the "R0" value we want our solution to approach.
                     if the parameter "label_R0" is provided, it’s used in the legend
                     (we will use "label_R0 = optimal_R0")
    """

    plt.figure()
    label = f'R(x), R0={label_R0:.3f}' if label_R0 is not None else 'R(x)'  # this is to get the legend indicating the function being plotted, as well as the corresponding component of the initial condition used in the numerical solution
    plt.plot(sol.t, sol.y[2], label=label)  # to access what's going to be plotted
    plt.axhline(R_target, linestyle=':', color='black',
                label=f'R_target={R_target:.3f}')  # this is what we'd like our solution to approach (considering the De Sitter condition)
    plt.xscale('log')  # to better understand/visualize the behaviour of the solution
    plt.xlabel('x (distance)')
    plt.ylabel('R(x)')
    plt.title('refined solution for "R(x)"')
    plt.grid(False)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # and to print the final integration point we write
    final_x = sol.t[-1]
    final_R = sol.y[2, -1]

    print(f'the integration reached the point "(x={final_x:.3f}, R={final_R:.3f})"')
