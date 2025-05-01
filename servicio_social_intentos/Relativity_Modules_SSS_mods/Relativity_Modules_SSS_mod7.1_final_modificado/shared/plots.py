import numpy as np
import matplotlib.pyplot as plt

def plot_potential_derivative(dVdR, start, stop, num_points=500):
    """
    Plot dV/dR vs R over [start, stop], with a dotted zero line.
    """
    R_vals    = np.linspace(start, stop, num_points)
    dVdR_vals = [dVdR(R) for R in R_vals]

    plt.figure()
    plt.plot(R_vals, dVdR_vals, label='dV/dR')
    plt.axhline(0, linestyle=':', color='black')
    plt.xlabel('R')
    plt.ylabel('dV/dR')
    plt.title('Potential derivative dV/dR')
    plt.grid(False)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_refined_solution(sol, R_target, label_R0=None):
    """
    Plot the Ricci-scalar solution sol.y[2] vs sol.t on a log-x scale,
    with a dotted horizontal line at R_target.

    If label_R0 is provided, it’s used in the legend.
    """
    plt.figure()
    label = f'R(x), R0={label_R0:.3f}' if label_R0 is not None else 'R(x)'
    plt.plot(sol.t, sol.y[2], label=label)
    plt.axhline(R_target, linestyle=':', color='black',
                label=f'R_target={R_target:.3f}')
    plt.xscale('log')
    plt.xlabel('Distance x')
    plt.ylabel('R(x)')
    plt.title('Refined solution for R')
    plt.grid(False)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Print final integration point
    final_x = sol.t[-1]
    final_R = sol.y[2, -1]
    print(f"Integration reached (x={final_x:.3e}, R={final_R:.3e})")
