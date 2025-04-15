import numpy as np
from numpy.ma.core import arange

from vectorized_derivative import *
from class_definitions.integrations import ODEIntegrator
from class_definitions.plots import ODESolutionPlotter

# TODO 10: create a function/class that checks for valid initial values of "R0"
# # we've already made sure to include the parameter "events" in SciPy's "solve_ivp". we now need to define that function
# r0[2] = 1000  # this renames entry "2" of the array "r0".
#
# threshold = 1e23  # this is an arbitrary number set by us. is this too big? we also need to be careful with this, what if now, it's too small of a threshold value?
# # I think a huge number corresponds better to the fact that there was a divergence (the first derivative "got too big").
# # just don't make it too huge so that Python considers it and "overflow".
#
# # the "return" of the following functions will tell the parameter "events" to look for its zeros. and that's the condition we need to adapt to our situation
# def R_div(x, r):
#     return abs(F(x, r)[2]) - threshold  # because the second component corresponds to "R". I think this should account for both positive and negative "huge" increases in the solution. with this definition... should we take into account the "direction" in which we get a "zero-crossing"? probably not. it should be positive (going from negative to positive) since we took the absolute value, right
# # this works for our specific set of functions. but we might want to be more careful with inflexion points. since they could have large first derivatives but still allow the solution to converge.
#
# # the whole idea of this "threshold" constant is the following: think about a line with an arbitrary slope such that
# # the larger/smaller the slope, the more "vertical" the line becomes.
# # and maybe think of the polynomial approximation of a function which to first order is a line.
# # so it's not so crazy to think about the divergence of our solution's component in terms of what we defined above.
#
# R_div.terminal = True  # this is what we wanted. for the solver to stop once a divergence was detected
# R_div.direction = 0  # just to be safe. this is so that we detect a "zero-crossing" going from negative to positive and vice versa.
#
#
# # we could also have generalized this for more events. we'd just need to define more conditions and in the parameter "events" we'd
# # set it equal to "[fun1, fun2, ...]" where in our case of just one function, we could simply just write "events=R_div"
#
# int_R_div = ODEIntegrator(F, r0, x_start=0, x_end=10, events=[R_div])
# int_R_div.integrate()
#
# r_R_div_execution_time = int_R_div.get_execution_time()
# x_R_div, r_R_div = int_R_div.get_solution()
# x_R_div_events, r_R_div_events = int_R_div.get_events()
# # and how do we see where our solution began to "diverge" according to our criteria?
# if x_R_div_events is not None:  # that is, if we actually get an event triggered.
#     if len(x_R_div_events[0]) > 0:  # if an event was detected, then we'd expect that the array "x_R_div_events[0]" was not empty
#         divergence_time = x_R_div_events[0][0]  # this would get the first element of the array "x_R_div_events[0]"; which would be when a divergence was detected. and since we told our code to stop integrating when a divergence was detected, then this is the value we're looking for here
#         print(f"divergence detected at 'x={divergence_time}'")
#
# # but maybe a divergence is caused by another component, and we can't detect it here. we need to check that out before generalizing the code.
# # but... we'll continue for now; just modifying values of the second component.
#
# r_R_div_plotter = ODESolutionPlotter(x_R_div, r_R_div, r_R_div_execution_time)
# r_R_div_plotter.plot(component=2, x_log_scale=True)

# todo "HERE"... we start guessing allowed values

# something happens to our plot between "1.4" and "1.89". it stops being stable and diverges (positively).
# but the way it's stable is kind of opposite to what we're expecting to be "stable" at "170".
# but the instabilities are just what we were told they would be: a positive/negative divergence after some integration steps.
# after "3.75", our solution has the expected behaviour; moreover,
# after this expected behaviour, we may just have the instabilities we were told before.
# it seems to handle numbers up to "9.9977e2" with not so much trouble.

# todo "CAREFULLY"
# everything works fine before reaching values of order greater than "1e3".

# orders of magnitude of "1e3" take too long. what happens here?

# after "1.01e3" we're okay
# orders of magnitude between "1e4" and "1.4e4" don't show a solution (sometimes it gives one point, sometimes it doesn't give anything).
# though "1.2e4" gives us exactly what we're looking for.
# after "1e5" we get graphs that begin to diverge.
# after "9.1e20" we don't get solutions aside from the initial value.

# todo "MAYBE"... look for values between "3.75" up to "9.1e20"

# after "1e400" we're asked to give "finite" values of our initial condition.
r0[2] = 170  # but we usually start here at "170"

threshold = 1e23

def divergence_event(x, r):
    drdx = F(x, r)
    # Check if any component is NaN or Inf
    if np.any(np.isnan(drdx)) or np.any(np.isinf(drdx)):  # this checks if there are any "NaNs" in the derivative array or if there are any "Infs" (infinite values) in the derivative array.
        return 0.0  # Trigger event immediately if invalid values appear.

    # Consider divergence if the largest absolute derivative exceeds the threshold.
    max_derivative = np.max(np.abs(drdx))
    return max_derivative - threshold

divergence_event.terminal = True
divergence_event.direction = 0

# this is just so that we can maybe select a specific set of "x" values
step_size = 1e-4
spacing = [np.arange(0, 20, step_size), None]
space = spacing[1]  # use index "1" for Scipy to decide the integration step sizes
r0[2] = 0.01

int_R_div = ODEIntegrator(F, r0, x_start=0, x_end=20, events=[divergence_event], t_eval=space)
int_R_div.integrate()
print("done 1/2: integrated")
r_R_div_execution_time = int_R_div.get_execution_time()
x_R_div, r_R_div = int_R_div.get_solution()
x_R_div_events, r_R_div_events = int_R_div.get_events()
print("done 2/2: plotted")
r_R_div_plotter = ODESolutionPlotter(x_R_div, r_R_div, r_R_div_execution_time, R0=r0[2])
r_R_div_plotter.plot(component=2, x_log_scale=True)

if x_R_div_events is not None and len(x_R_div_events[0]) > 0:
    divergence_time = x_R_div_events[0][0]
    print(f"Event triggered at 'x={divergence_time}'")
