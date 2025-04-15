import matplotlib.pyplot as plt

class ODESolutionPlotter:
    def __init__(self, x, r, execution_time, R0=None):
        """
        Initializes the ODESolutionPlotter class with the independent variable (x),
        dependent variable (r), and execution time of the integration.

        :param x: The independent variable (position).
        :param r: The dependent variable (results), shape: (num_components, num_points)
        :param execution_time: Time taken for the integration.
        :param R0: An optional parameter to include in the plot label.
        """
        self.x = x
        self.r = r
        self.execution_time = execution_time
        self.R0 = R0  # Store R0 for later use in labels

    def plot(self, component=2, x_log_scale=False, y_log_scale=False):
        """
        Plots specified component(s) of the solution r as a function of x (by default it chooses the component "R").
        Optionally uses a logarithmic scale for the axes.

        :param component: Index (or list of indices) of the component(s) to plot. Default is 2.
        :param x_log_scale: Boolean to indicate if x-axis should be logarithmic. Default is False.
        :param y_log_scale: Boolean to indicate if y-axis should be logarithmic. Default is False.
        """

        r_list = ["n", "m", "R", "DR", "P", "Ms", "Mb"]

        # Convert component to a list if it's a single integer
        if isinstance(component, int):
            component = [component]

        fig_plot, axis_plot = plt.subplots()

        if x_log_scale:
            axis_plot.set_xscale('log')
        if y_log_scale:
            axis_plot.set_yscale('log')

        # Plot each requested component
        for comp_idx in component:
            if comp_idx < 0 or comp_idx >= self.r.shape[0]:
                raise IndexError(f"Component index '{comp_idx}' is out of bounds. 'r' has '{self.r.shape[0]}' components.")

            plot_idx = self.r[comp_idx, :]
            label_str = f'"{r_list[comp_idx]}(x)" \n "{len(self.x)}" points'

            # if "R0" is provided, add it to the label
            if self.R0 is not None:
                label_str += f'\n "R0 = {self.R0}"'

            axis_plot.scatter(self.x, plot_idx, marker='.', label=label_str)

        axis_plot.set(xlabel='distance "x"', ylabel='component of "r(x)"')
        axis_plot.legend(loc='lower left')

        plt.title(f'Integration took "{round(self.execution_time, 3)} s"')

        plt.show()
