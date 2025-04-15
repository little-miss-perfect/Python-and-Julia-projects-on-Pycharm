# TODO 1: import/install modules
from plotting_allowed_initial_values import *

# some of these modules already include other modules used like "numpy" and "pandas";
# so it would be redundant to import them again.

# TODO 2: import the data from the ".dat" files, and define the variables in the files
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
#         (such that you can choose from multiple "integrators"? maybe after just one of them works out)
#         preferably, choose one that handles a variable "step size".
r0[2] = 170  # this renames entry "2" of the array "r0". and "170" is also the first suggested unmodified value of "R0" that we know works
integrator = ODEIntegrator(F, r0)
integrator.integrate()
x, r = integrator.get_solution()


# TODO 8: measure the time taken to integrate.
execution_time = integrator.get_execution_time()


# TODO 9: plot the data as a function of position.
#         scale the position values logarithmically (plot "R(x) vs x").

plotter = ODESolutionPlotter(x, r, execution_time, R0=r0[2])
# # hay "6" índices para elegir del vector "r(n, m, R, DR, P, Ms, Mb)"
# plotter.plot(component=[0], x_log_scale=True)
# plotter.plot(component=[1], x_log_scale=True)
# plotter.plot(component=[2], x_log_scale=True)  # this is the graph we're interested in
# plotter.plot(component=[3], x_log_scale=False)
# plotter.plot(component=[4], x_log_scale=True)
# plotter.plot(component=[5], x_log_scale=True)
# plotter.plot(component=[6], x_log_scale=True)
# plotter.plot(component=[0,1,2,3, 4, 5, 6], x_log_scale=True)

plotter.plot(component=2, x_log_scale=True)


# TODO 10: create a function/class that checks for valid initial values of "R0"
# we've already done this in the module "finding_allowed_initial_values"
