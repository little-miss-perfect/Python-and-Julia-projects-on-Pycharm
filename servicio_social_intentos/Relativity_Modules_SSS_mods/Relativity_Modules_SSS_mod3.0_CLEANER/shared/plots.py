import numpy as np
import matplotlib.pyplot as plt

def plot_reg_func(g, ind_var='ind_var', min_val=-1e2, max_val=1e2, num_points=200):
    # Create a range of values where we'll evaluate "g"
    values = np.linspace(min_val, max_val, num_points)

    # Evaluate "g" for all chosen "values"
    g_values = [g(i) for i in values]

    # Plot "g({ind_var})" vs "{ind_var}"
    plt.figure(figsize=(8, 5))
    plt.plot(values, g_values, label=f'{g.__name__}({ind_var})')
    plt.xlabel(f'{ind_var}')
    plt.ylabel(f'{g.__name__}({ind_var})')
    plt.title(f'Plot of: {g.__name__}({ind_var})')
    plt.grid(True)
    plt.legend()
    plt.show()


class MultiSolutionRPlotter:
    def __init__(self, solutions):
        """
        Initialize with a list of solution dictionaries.
        Each dictionary should have:
          - "x": 1D array of the independent variable (e.g., distance)
          - "r": 2D array of the solution, with shape (num_components, num_points)
          - "R0": the value used for the r0[2] initial condition
        """
        self.solutions = solutions

    def plot_R(self, component=2, x_log_scale=True, cmap='viridis'):
        """
        Plot the R component (default index 2) from each solution on the same figure.

        The color of each curve is determined by its r0[2] value via the specified colormap.
        The x-axis is set to logarithmic scale if x_log_scale=True.

        :param component: integer, the index of the solution component to plot (default 2 for R)
        :param x_log_scale: bool, if True sets the x-axis to logarithmic scale
        :param cmap: string or matplotlib colormap instance; default is 'viridis'
        """
        # Sort solutions by R0 value (so colors vary smoothly)
        solutions_sorted = sorted(self.solutions, key=lambda sol: sol["R0"])
        R0_values = np.array([sol["R0"] for sol in solutions_sorted])

        # Normalize R0 values for colormap
        norm = plt.Normalize(R0_values.min(), R0_values.max())
        colormap = plt.get_cmap(cmap)

        fig, ax = plt.subplots(figsize=(10, 6))

        for sol in solutions_sorted:
            x_vals = sol["x"]
            r_vals = sol["r"]
            R0_val = sol["R0"]

            # Check that the solution has the desired component
            if component < 0 or component >= r_vals.shape[0]:
                print(f"Warning: component index {component} out of range for solution with R0={R0_val}")
                continue

            y_vals = r_vals[component, :]

            # Map the R0 value to a color
            color = colormap(norm(R0_val))

            # Plot the solution curve
            ax.plot(x_vals, y_vals, color=color, label=f"R0={R0_val:.2f}")

        ax.set_xlabel("Distance x")
        ax.set_ylabel("R(x)")
        ax.set_title("Solutions for R with varying r0[2]")
        if x_log_scale:
            ax.set_xscale("log")

        # Add a colorbar to indicate the mapping of r0[2] values
        sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label("r0[2] value")

        # Only add legend if the number of curves is small
        if len(solutions_sorted) <= 10:
            ax.legend(loc="best")

        plt.tight_layout()
        plt.show()
