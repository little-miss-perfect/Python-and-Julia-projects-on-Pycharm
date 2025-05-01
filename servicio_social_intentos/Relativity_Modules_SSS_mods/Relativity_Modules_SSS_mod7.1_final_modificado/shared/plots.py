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
    print(f"Integration reached (x={final_x:.3f}, R={final_R:.3f})")

def plot_potential(p, start, stop, num_points=500, R_ref=None):
    """
    Plot the potential V(R) - V(R0) vs R over [start, stop].

    Parameters:
    - p: an instance of PotentialDerivative
    - start: lower bound of R interval (also default R0 if R0=None)
    - stop: upper bound of R interval
    - num_points: number of points in grid
    - R0: reference R value for V(R0); if None, uses start
    """
    # Reference point
    R0_ref = start if R_ref is None else R_ref

    # Generate grid
    R_vals = np.linspace(start, stop, num_points)
    V_vals = [p.V(R, R0_ref) for R in R_vals]

    # Plot
    plt.figure()
    label = 'V(R) - V(R0)' if R_ref is not None else 'V(R) - V(start)'
    plt.plot(R_vals, V_vals, label=label)
    plt.axhline(0, linestyle=':', color='black')
    plt.xlabel('R')
    plt.ylabel('V(R)')
    plt.title('Potential V(R)')
    plt.grid(False)
    plt.legend()
    plt.tight_layout()
    plt.show()
