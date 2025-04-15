from finding_roots import *
from class_definitions.plots import *


# todo "ALSO CONSIDER"... that negative values give valid solutions; but do they give "stable" solutions?
# another note is that: once you've found stable solutions, try plotting them with a solution that used "LSODA",
# just to get a few more points to visualize and a "longer" solution.


# TODO p.4: some parameters
# this is just so that we can maybe select a specific set of "x" values
step_size = 1e-5
spacing = [np.arange(0, x_end, step_size), None]
space = spacing[1]  # we'll use index "1" for Scipy to decide the integration step sizes.


# TODO p.5: choose "R0" and integrate
# we'd like to modify "r0[2]". also, note that the interval "(0, 1.4]" has a sort of "inverse/mirrored" logistic behaviour (to our target behaviour)
# that sort of moves to an exponential behaviour after the endpoint of this interval, to finally "converge" to the logistic behaviour we expect from the solution given by "R0=170" (the one we knew worked).
r0[2] = 170  # and this is how we'll modify this value. "5" gives a divergence.
# the wierd behaviour happens up to about "1.2"
print(f"the current 'R0' value is: \n"
          f"{r0[2]} \n")

int_R = solve_int

start_int_timed = timeit.default_timer()
int_R.integrate()
stop_int_timed = timeit.default_timer()

print(int_R.get_solver_message())
print(int_R.get_solver_final_time())

execution_time_timed = stop_int_timed - start_int_timed
print(f"\n done 1/2: \n"
      f"integrated for '{execution_time_timed} s'")


# TODO p.6: plot
r_R_execution_time = int_R.get_execution_time()
x_R, r_R = int_R.get_solution()
x_R_events, r_R_events = int_R.get_events()  # here are the "events"
print("\n done 2/2: \n"
      "plotted \n \n \n \n")
r_R_plotter = ODESolutionPlotter(x_R, r_R, r_R_execution_time, R0=r0[2])
# r_R_plotter.plot(component=2, x_log_scale=False)
r_R_plotter.plot(component=2, x_log_scale=True, y_log_scale=False)




# TODO p.7: this gives us the events
# print(type(x_R_events))
# print(x_R_events)
print(f"\n the current events are \n"  # [nan_inf_evt, div_evt, concave_evt]
          f"\n NaN/Inf: {x_R_events[0]} \n"
          f"\n div: {x_R_events[1]} \n"
          f"\n concave_evt: {x_R_events[2]} \n")

# the following is to see where the integration really stopped
# (why isn't it stopping at "x_end" is no other event is being triggered?
# is this something inherent from "solve_ivp" that we haven't figured out yet?)
print(f"we've integrated up to:"
      f"\n {x_R[-1]}")
print(f"whose image is:"
      f"\n {r_R[2][-1]}")
