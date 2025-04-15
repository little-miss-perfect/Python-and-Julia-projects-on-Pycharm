# TODO 1: import/install modules
import timeit
import matplotlib.pyplot as plt
from vectorized_derivative import *
from SciPy_modified import solve_ivp

# some of these modules already include other modules used like "numpy" and "pandas";
# so it would be redundant to import them again.

# TODO 2:  import the data from the ".dat" files, and define the variables in the files
# they've been imported from our module "variables"


# TODO 3: define the other ("non-imported") variables used throughout the program
# they've been imported from our module "variables"


# TODO 4: define the "f(R)" functions
# they've been imported from our module "f_functions"


# TODO 5: define the "derivative" functions
# they've been imported from our module "derivative_functions"


# TODO 6: define the "vectorized derivative" of the system of equations ("F")
# they've been imported from our module "vectorized_derivative"


# TODO 7: define an "integrator" class for the "vectorized" problem,
#                 (such that you can choose from multiple "integrators"? maybe after just one of them works out)
#                 preferably, make one that handles a variable "step size".

class ODEIntegrator:
    """
    by default, we integrate with "LSODA", because in principle, our problem is stiff.
    """
    def __init__(self, F, r0, x_start=0, x_end=8, rtol=1e-9, atol=1e-12, method='LSODA'):
        """
        Initialize the integrator with the ODE system function, initial values, and parameters for the solver.

        :param F: ODE system function
        :param r0: Initial values for the dependent variables
        :param x_start: Starting point of the independent variable
        :param x_end: Endpoint of the independent variable
        :param rtol: Relative tolerance for the solver
        :param atol: Absolute tolerance for the solver
        :param method: Integration method (e.g., 'LSODA', 'RK45', etc.)
        """
        self.F = F
        self.r0 = r0
        self.t_start = x_start
        self.t_end = x_end
        self.rtol = rtol
        self.atol = atol
        self.method = method  # Solver method (e.g., 'LSODA', 'RK45')
        self.x = None  # Placeholder for independent variable array
        self.r = None  # Placeholder for dependent variable array
        self.execution_time = None  # Placeholder for execution time

    def integrate(self):
        """
        Perform the integration and store the result in the object.
        """
        start_int = timeit.default_timer()

        # Perform the integration using the chosen method
        sol = solve_ivp(self.F, (self.t_start, self.t_end), self.r0, method=self.method, rtol=self.rtol, atol=self.atol)

        self.x = sol.t  # Independent variable
        self.r = sol.y  # Dependent variable (a "vector")

        stop_int = timeit.default_timer()
        self.execution_time = stop_int - start_int  # Time taken for the integration

    def get_solution(self):
        """
        Return the independent and dependent variables after integration.
        :return: (x, r) tuple where x is the independent variable and r is the dependent variable
        """
        return self.x, self.r

    def get_execution_time(self):
        """
        Return the execution time for the integration.
        :return: Execution time in seconds
        """
        return self.execution_time


integrator = ODEIntegrator(F, r0)
integrator.integrate()
x, r = integrator.get_solution()

# TODO 8: measure the time taken to integrate.
execution_time = integrator.get_execution_time()

# TODO 9: create a function/class that checks the value


# TODO 10: plot the data as a function of position.
#         scale the position values logarithmically (plot "R(x) vs x").
class ODESolutionPlotter:
    def __init__(self, x, r, execution_time):
        """
        Initializes the ODESolutionPlotter class with the independent variable (x),
        dependent variable (r), and execution time of the integration.

        :param x: The independent variable (position).
        :param r: The dependent variable (results).
        :param execution_time: Time taken for the integration.
        """
        self.x = x
        self.r = r
        self.execution_time = execution_time

    def plot(self, log_scale=False):
        """
        Plots the R(x) vs x, with an option for logarithmic scaling of the x-axis.

        :param log_scale: Boolean to indicate if x-axis should be logarithmic. Default is False.
        """
        R = self.r[2, :]  # Access the R values from the solution

        figR, axisR = plt.subplots()

        if log_scale:
            axisR.set_xscale('log')  # Set the x-axis to logarithmic scale

        axisR.scatter(self.x, R, marker='.', color='b', label=f'{len(self.x)} points \n "135.009989998 < R0 < 199.99999899987"')
        axisR.set(xlabel='distance', ylabel='R(x)')
        axisR.legend(loc='lower left')

        plt.title(
            f'it took "{round(self.execution_time, 3)} s" '
            f'\n ("{round(self.execution_time / 60, 3)} min.") to solve the IVP, '
            f'given "R0={R0}"')

        plt.show()


plotter = ODESolutionPlotter(x, r, execution_time)
plotter.plot(log_scale=True)  # Set log_scale=True to enable the logarithmic x-axis
