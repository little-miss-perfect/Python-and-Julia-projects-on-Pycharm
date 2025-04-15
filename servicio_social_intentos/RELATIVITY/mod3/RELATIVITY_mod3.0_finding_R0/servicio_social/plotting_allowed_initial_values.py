from vectorized_derivative import *
from class_definitions.integrations import *
from class_definitions.plots import *

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
# everything works fine before reaching values of order greater than "1e3". I think I ran the code with this value and it worked, the terminal had the value "x=9.107562951266592".
# but how long did it take? we'll have to run it again to find out

# orders of magnitude of "1e3" take too long. what happens here?

# after "1.01e3" we're okay
# orders of magnitude between "1e4" and "1.4e4" don't show a solution (sometimes it gives one point, sometimes it doesn't give anything).
# though "1.2e4" gives us exactly what we're looking for.
# after "1e5" we get graphs that begin to diverge.
# after "9.1e20" we don't get solutions aside from the initial value.

# todo "MAYBE"... look for values between "3.75" up to "9.1e20"

# after "1e400" we're asked to give "finite" values of our initial condition.
r0[2] = 170  # but we usually start here at "170"

# todo "ALSO CONSIDER"... that negative values give valid solutions; but do they give "stable" solutions?

threshold = 1e23  # this is ridiculously high, right? why not use something like "1e3"?




# def divergence_event(x, r):
#     drdx = F(x, r)
#     # Check if any component is NaN or Inf
#     if np.any(np.isnan(drdx)) or np.any(np.isinf(drdx)):  # this checks if there are any "NaNs" in the derivative array or if there are any "Infs" (infinite values) in the derivative array.
#         return 0.0  # Trigger event immediately if invalid values appear.
#
#     # Consider divergence if the largest absolute derivative exceeds the threshold.
#     max_derivative = np.max(np.abs(drdx))
#     return max_derivative - threshold
#
# divergence_event.terminal = True  # which stops the integration when our criteria is met
# divergence_event.direction = 0  # this is related to the "zero-crossing"




# def make_nan_inf_event(F):
#     """
#     Returns an event function that detects if any derivative component
#     becomes NaN or Inf. If so, it returns 0.0, triggering an event.
#     This event is marked terminal, so the solver stops immediately.
#     """
#     def event(t, y):
#         drdt = F(t, y)
#         if np.any(np.isnan(drdt)) or np.any(np.isinf(drdt)):
#             # Return 0.0 => zero crossing => event triggers
#             return 0.0
#         # Return a negative value so it doesn't detect an event otherwise
#         return -1.0
#
#     event.terminal = True   # Stop the solver immediately if NaN/Inf is found
#     event.direction = 0     # Detect crossing in both directions
#     return event
#
#
# def make_first_crossing_event(F, threshold):
#     """
#     Returns an event function that detects when the maximum absolute derivative
#     crosses the given threshold for the FIRST time, but does NOT stop the solver
#     (terminal=False).
#     """
#     def event(t, y):
#         drdt = F(t, y)
#         # Compare max(abs(drdt)) to threshold
#         val = np.max(np.abs(drdt)) - threshold
#         return val
#
#     event.terminal = False  # Do not stop on first crossing
#     event.direction = 0
#     return event
#
#
# def make_second_crossing_event(F, threshold):
#     """
#     Returns an event function that detects when the maximum absolute derivative
#     crosses the same threshold a SECOND time (or any subsequent time),
#     and STOPS the solver (terminal=True).
#     """
#     def event(t, y):
#         drdt = F(t, y)
#         val = np.max(np.abs(drdt)) - threshold
#         return val
#
#     event.terminal = True   # Stop on second crossing
#     event.direction = 0
#     return event
#
#
#
#
# nan_inf_evt  = make_nan_inf_event(F)
# first_evt    = make_first_crossing_event(F, threshold=threshold)
# second_evt   = make_second_crossing_event(F, threshold=threshold)
#
#
#
#
# # # this is just so that we can maybe select a specific set of "x" values
# # x_end = 20
# # step_size = 1e-4
# # spacing = [np.arange(0, x_end, step_size), None]
# # space = spacing[1]  # use index "1" for Scipy to decide the integration step sizes
# # # we'd like to modify "r0[2]".
# # r0[2] = 1.89  # and this is how we'll modify this value.
# #
# # int_R_div = ODEIntegrator(F, r0, x_start=0, x_end=x_end, events=[divergence_event], t_eval=space)
# # start_int_timed = timeit.default_timer()
# # int_R_div.integrate()
# # stop_int_timed = timeit.default_timer()
# #
# # execution_time_timed = stop_int_timed - start_int_timed
# # print(f"done 1/2: integrated for '{execution_time_timed}' s")
# #
# # r_R_div_execution_time = int_R_div.get_execution_time()
# # x_R_div, r_R_div = int_R_div.get_solution()
# # x_R_div_events, r_R_div_events = int_R_div.get_events()
# # print("done 2/2: plotted")
# # r_R_div_plotter = ODESolutionPlotter(x_R_div, r_R_div, r_R_div_execution_time, R0=r0[2])
# # r_R_div_plotter.plot(component=2, x_log_scale=True)
# #
# # if x_R_div_events is not None and len(x_R_div_events[0]) > 0:
# #     divergence_x = x_R_div_events[0][0]
# #     print(f"Event triggered at 'x={divergence_x}'")
#
# # this is just so that we can maybe select a specific set of "x" values
# x_end = 20
# step_size = 1e-4
# spacing = [np.arange(0, x_end, step_size), None]
# space = spacing[1]  # use index "1" for Scipy to decide the integration step sizes
# # we'd like to modify "r0[2]".
# r0[2] = 170  # and this is how we'll modify this value.
#
# int_R_div = ODEIntegrator(F, r0, x_start=0, x_end=x_end, events=[nan_inf_evt, first_evt, second_evt], t_eval=space)
# start_int_timed = timeit.default_timer()
# int_R_div.integrate()
# stop_int_timed = timeit.default_timer()
#
# execution_time_timed = stop_int_timed - start_int_timed
# print(f"done 1/2: integrated for '{execution_time_timed}' s")
#
# r_R_div_execution_time = int_R_div.get_execution_time()
# x_R_div, r_R_div = int_R_div.get_solution()
# x_R_div_events, r_R_div_events = int_R_div.get_events()
# print("done 2/2: plotted")
# r_R_div_plotter = ODESolutionPlotter(x_R_div, r_R_div, r_R_div_execution_time, R0=r0[2])
# r_R_div_plotter.plot(component=2, x_log_scale=True)
#
# if x_R_div_events is not None and len(x_R_div_events[0]) > 0:
#     divergence_x = x_R_div_events[0][0]
#     print(f"Event triggered at 'x={divergence_x}'")





def make_nan_inf_event(F):
    """
    Stops the solver immediately if any derivative component is NaN or Inf.
    """

    def event(t, y):
        drdt = F(t, y)
        if np.any(np.isnan(drdt)) or np.any(np.isinf(drdt)):
            return 0.0  # triggers the event
        return -1.0  # no event otherwise

    event.terminal = True
    event.direction = 0
    return event


def make_divergence_event(F, big_threshold):
    """
    A single 'divergence' event that stops as soon as max(abs(drdt)) exceeds 'big_threshold'.
    If this event triggers, we'll consider the solution 'unsuccessful' due to blow-up.
    """

    def event(t, y):
        drdt = F(t, y)
        val = np.max(np.abs(drdt)) - big_threshold
        return val

    event.terminal = True
    event.direction = 1  # detect going from below threshold to above threshold
    return event


def make_first_crossing_event(F, threshold):
    """
    Non-terminal upward crossing from below threshold to above threshold.
    We won't stop here, but we'll record that we crossed once.
    """

    def event(t, y):
        drdt = F(t, y)
        return np.max(np.abs(drdt)) - threshold

    event.terminal = False
    event.direction = 1  # upward crossing
    return event


def make_second_crossing_event(F, threshold):
    """
    Terminal downward crossing from above threshold back to below threshold.
    If triggered, we consider it 'successful' because it returned below threshold.
    """

    def event(t, y):
        drdt = F(t, y)
        return np.max(np.abs(drdt)) - threshold

    event.terminal = True
    event.direction = -1  # downward crossing
    return event




# Example thresholds:
threshold_small = 1e3  # used for first/second crossing
threshold_big = 1e17  # used for 'big divergence' event

# Instantiate event functions:
nan_inf_evt = make_nan_inf_event(F)
big_div_evt = make_divergence_event(F, big_threshold=threshold_big)
first_evt = make_first_crossing_event(F, threshold_small)
second_evt = make_second_crossing_event(F, threshold_small)

# You can reorder them if you like; the solver will monitor all:
# The index in t_events will match the order here.
# t_events[0] -> nan_inf_evt
# t_events[1] -> big_div_evt
# t_events[2] -> first_evt
# t_events[3] -> second_evt
all_events = [nan_inf_evt, big_div_evt, first_evt, second_evt]




# # this is just so that we can maybe select a specific set of "x" values
# x_end = 20
# step_size = 1e-4
# spacing = [np.arange(0, x_end, step_size), None]
# space = spacing[1]  # use index "1" for Scipy to decide the integration step sizes
# # we'd like to modify "r0[2]".
# r0[2] = 1.89  # and this is how we'll modify this value.
#
# int_R_div = ODEIntegrator(F, r0, x_start=0, x_end=x_end, events=[divergence_event], t_eval=space)
# start_int_timed = timeit.default_timer()
# int_R_div.integrate()
# stop_int_timed = timeit.default_timer()
#
# execution_time_timed = stop_int_timed - start_int_timed
# print(f"done 1/2: integrated for '{execution_time_timed}' s")
#
# r_R_div_execution_time = int_R_div.get_execution_time()
# x_R_div, r_R_div = int_R_div.get_solution()
# x_R_div_events, r_R_div_events = int_R_div.get_events()
# print("done 2/2: plotted")
# r_R_div_plotter = ODESolutionPlotter(x_R_div, r_R_div, r_R_div_execution_time, R0=r0[2])
# r_R_div_plotter.plot(component=2, x_log_scale=True)
#
# if x_R_div_events is not None and len(x_R_div_events[0]) > 0:
#     divergence_x = x_R_div_events[0][0]
#     print(f"Event triggered at 'x={divergence_x}'")

# this is just so that we can maybe select a specific set of "x" values
x_end = 20
step_size = 1e-4
spacing = [np.arange(0, x_end, step_size), None]
space = spacing[1]  # use index "1" for Scipy to decide the integration step sizes
# we'd like to modify "r0[2]".
r0[2] = 953.5  # and this is how we'll modify this value.

int_R_div = ODEIntegrator(F, r0, x_start=0, x_end=x_end, events=all_events, t_eval=space, method='BDF')
start_int_timed = timeit.default_timer()
int_R_div.integrate()
stop_int_timed = timeit.default_timer()

execution_time_timed = stop_int_timed - start_int_timed
print(f"done 1/2: integrated for '{execution_time_timed}' s")

r_R_div_execution_time = int_R_div.get_execution_time()
x_R_div, r_R_div = int_R_div.get_solution()
x_R_div_events, r_R_div_events = int_R_div.get_events()
print("done 2/2: plotted")
r_R_div_plotter = ODESolutionPlotter(x_R_div, r_R_div, r_R_div_execution_time, R0=r0[2])
r_R_div_plotter.plot(component=2, x_log_scale=True)

if x_R_div_events is not None and len(x_R_div_events[0]) > 0:
    divergence_x = x_R_div_events[0][0]
    print(f"Event triggered at 'x={divergence_x}'")
