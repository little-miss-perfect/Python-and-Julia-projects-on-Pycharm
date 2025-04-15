# from vectorized_derivative import *
# from class_definitions.integrations import *
#
# # TODO 11: first check the allowed positive initial conditions (then we'll do the negative)
# # this is where we've been stuck for a while
#
#
# # TODO 11.0: some constants
# threshold_big = 1e3  # used for 'big divergence' event
# start = 6  # this is where we start searching for values of "R0" (the left/lower bound of the interval we're searching in)
# R0_increment = 1  # the increment to the next value of "R0" in the interval we're searching in
# quantity = 4  # amount of points ("R0" values) in the list we'd be searching
# R0_end = start + quantity * R0_increment
#
#
# # TODO 11.1: event functions
# def nan_inf_event(F):
#     """
#     this stops the solver immediately if any derivative component is NaN or Inf.
#     this is the "extreme" case of the function "make_divergence_event".
#     """
#
#     def event(t, y):
#
#         drdt = F(t, y)
#
#         if np.any(np.isnan(drdt)) or np.any(np.isinf(drdt)):
#             return 0.0  # this triggers the event
#
#         return -1.0  # this won't trigger the event (the event is only triggered when a zero is detected)
#
#     event.terminal = True
#     event.direction = 0
#
#     return event
#
#
# def divergence_event(F, big_threshold):
#     """
#     a single 'divergence' event that stops as soon as 'max(abs(drdt))' exceeds 'big_threshold'.
#     if this event triggers, we'll consider the solution 'unsuccessful' due to a 'blow-up'.
#     """
#
#     def event(t, y):
#
#         drdt = F(t, y)
#
#         return np.max(np.abs(drdt)) - big_threshold
#
#     event.terminal = True
#     event.direction = 1  # detect going from below threshold to above threshold (our derivative gets too big -in absolute value. that is, the function blows up/down; it diverges)
#
#     return event
#
#
# def concave_event(F):
#
#     def event(t, y):
#
#         drdt = F(t, y)
#         R2 = drdt[3]
#
#         return R2
#
#     event.terminal = False  # we'd just like to detect this event, not terminate the solution. not yet.
#     event.direction = 0  # in principle, we'd like to only consider "1" since we were told the correct behaviour was a change in "concavity" from "down to up"; which amounts to finding a "change in sign" in our event function from "negative to positive".
#     # we set this direction because we've already seen that other solutions (at least ones given a non-negative "R0" value) have this "change in concavity" behaviour.
#     # solutions given a negative "R0" value seem to always diverge. but we haven't tested this hypothesis out, yet. maybe we should consider the "concave" criteria as "universal".
#
#     return event
#
#
# # TODO 11.2: the events used
# nan_inf_evt = nan_inf_event(F)
# div_evt = divergence_event(F, big_threshold=threshold_big)
# concave_evt = concave_event(F)
#
# all_events = [nan_inf_evt, div_evt, concave_evt]
#
#
# # TODO 11.3: some parameters
# x_end = 4e1
#
#
# # TODO 11.4: "R0" range (to be modified manually) and "parameters" for the loop
# R0_a = np.arange(start=start, stop=R0_end, step=R0_increment)
# R0_b = np.array([0])  # "annoying" values to skip
# allowed_R0 = np.setdiff1d(R0_a, R0_b)
#
# print(f"the list we're looking through is:"
#       f"\n {allowed_R0} \n")
#
# allowed_R0_len = len(allowed_R0)
# R0_num_steps = 10  # print progress notification every "R0_num_steps" iterations
#
#
# # TODO 11.5: the empty lists
# successful_R0 = []
# unsuccessful_R0 = []
#
#
# # TODO 11.6: the loop
# start_int_loop = timeit.default_timer()
#
# for i, R0_value in enumerate(allowed_R0, start=1):  # start enumerating by tuples from "1" instead of "0". this is done for the last print we have in the loop.
#     r0[2] = R0_value  # update initial condition
#     print(f"the current 'R0' value is: \n"
#           f"{R0_value} \n")
#
#     integrator = ODEIntegrator(
#         F=F,
#         r0=r0,
#         x_start=0,
#         x_end=x_end,
#         events=all_events,  # [nan_inf_evt, div_evt, concave_evt]
#         method='BDF',
#         max_step=np.inf  # we might want to change this to smaller values (like: allow the maximum step to be of "0.1" units; with no restriction on how small it can be)
#     )
#     integrator.integrate()
#
#     x_events, r_events = integrator.get_events()
#     print(f"the current events are \n"  # [nan_inf_evt, div_evt, concave_evt]
#           f"NaN/Inf: {x_events[0]} \n"
#           f"div: {x_events[1]} \n"
#           f"concave: {x_events[2]} \n")
#
#     if x_events is None:  # why not some explicit condition on the array being "empty"? what does "SciPy" return when asked for the "event" array? is it even an array?
#         # does "no events" imply the integration terminated successfully?
#         successful_R0.append(R0_value)
#     else:
#         # all_events = [nan_inf_evt, div_evt, concave_evt]
#         nan_inf_times = x_events[0]
#         div_times = x_events[1]
#         concave_times = x_events[2]
#
#         # first check for undefined values
#         if len(nan_inf_times) > 0:
#             unsuccessful_R0.append(R0_value)
#
#         # then check for the condition we're searching for
#         elif len(concave_times) > 0:
#             # if this behaviour occurs, then it's what we considered to be successful
#             successful_R0.append(R0_value)
#
#         # if no undefined value was detected, and our condition was not reached, then check if the solution diverged
#         elif len(div_times) > 0:
#             unsuccessful_R0.append(R0_value)
#
#         else:
#             # would any other scenario be successful?
#             unsuccessful_R0.append(R0_value)
#
#     # Print progress
#     if R0_num_steps != 0 and (i % R0_num_steps == 0):
#         percent_done = (i / allowed_R0_len) * 100
#         print(f"Processed {i} / {allowed_R0_len} R0 values ({percent_done:.2f}% done)")
#
# stop_int_loop = timeit.default_timer()
#
# execution_time_loop = stop_int_loop - start_int_loop
#
#
# # TODO 11.7: printing the results (of the loop)
# print(f"It took '{execution_time_loop:.3f} s' to check valid values of 'R0'.")
# print(f"the lists are: \n"
#       f"unsuccessful_R0 = {unsuccessful_R0} \n"
#       f"successful_R0   = {successful_R0} \n")




from vectorized_derivative import *
from class_definitions.integrations import *


# TODO 11: first check the allowed positive initial conditions (then we'll do the negative)

# TODO 11.0: some constants
threshold_big = 1e3  # used for 'big divergence' event
R0_start = 8  # this is where we start searching for values of "R0" (the left/lower bound of the interval we're searching in)
R0_increment = 1  # the increment to the next value of "R0" in the interval we're searching in
quantity = 4  # amount of points ("R0" values) in the list we'd be searching
R0_end = R0_start + quantity * R0_increment


# TODO 11.1: event functions
def nan_inf_event(F):
    """
    stops the solver if any derivative component is NaN or Inf.
    """
    def event(t, y):
        drdt = F(t, y)
        if np.any(np.isnan(drdt)) or np.any(np.isinf(drdt)):
            return 0.0  # triggers the event
        return -1.0
    event.terminal = True
    event.direction = 0
    return event


def divergence_event(F, big_threshold):
    """
    stops as soon as max(abs(drdt)) exceeds 'big_threshold'.
    """
    def event(t, y):
        drdt = F(t, y)
        return np.max(np.abs(drdt)) - big_threshold

    event.terminal = True
    event.direction = 1
    return event


def concave_event(F):
    def event(t, y):
        drdt = F(t, y)
        R2 = drdt[3]
        return R2
    event.terminal = False
    event.direction = 0
    return event


# TODO 11.2: the events used
nan_inf_evt = nan_inf_event(F)
div_evt = divergence_event(F, big_threshold=threshold_big)
concave_evt = concave_event(F)

all_events = [nan_inf_evt, div_evt, concave_evt]


# TODO 11.3: some parameters
x_end = 4e1

# TODO 11.4: "R0" range
R0_a = np.arange(start=R0_start, stop=R0_end, step=R0_increment)
R0_b = np.array([0])  # "annoying" values to skip
allowed_R0 = np.setdiff1d(R0_a, R0_b)

print(f"The list we're looking through is:\n{allowed_R0}\n")

allowed_R0_len = len(allowed_R0)
R0_num_steps = 10  # print progress notification every "R0_num_steps" iterations

# TODO 11.5: the empty lists
successful_R0 = []
unsuccessful_R0 = []
terminal_error_list = []   ##### NEW CODE #####

# TODO 11.6: the loop
start_int_loop = timeit.default_timer()

for i, R0_value in enumerate(allowed_R0, start=1):
    r0[2] = R0_value  # update initial condition
    print(f"the current 'R0' value is: \n{R0_value}\n")

    integrator = ODEIntegrator(
        F=F,
        r0=r0,
        x_start=0,
        x_end=x_end,
        events=all_events,
        method='BDF',
        max_step=np.inf
    )

    ##### NEW CODE #####
    try:
        integrator.integrate()
    except ValueError as e:
        # if the error message matches the "array must not contain infs or NaNs"
        if "array must not contain infs or NaNs" in str(e):
            print(f"Encountered ValueError for R0={R0_value}: {e}")
            terminal_error_list.append(R0_value)
            continue  # skip the rest of this loop iteration
        else:
            # if it's some other ValueError, you might want to re-raise
            raise

    # If we reach here, integrator.integrate() succeeded
    x_events, r_events = integrator.get_events()
    print(f"the current events are:\n"
          f"NaN/Inf: {x_events[0]} \n"
          f"div:     {x_events[1]} \n"
          f"concave: {x_events[2]} \n")

    if x_events is None:
        # no events => success
        successful_R0.append(R0_value)
    else:
        nan_inf_times = x_events[0]
        div_times = x_events[1]
        concave_times = x_events[2]

        # check for undefined values
        if len(nan_inf_times) > 0:
            unsuccessful_R0.append(R0_value)
        # if concavity was detected
        elif len(concave_times) > 0:
            successful_R0.append(R0_value)
        # if the solution diverged
        elif len(div_times) > 0:
            unsuccessful_R0.append(R0_value)
        else:
            # any other scenario => unsuccessful
            unsuccessful_R0.append(R0_value)

    # Print progress
    if R0_num_steps != 0 and (i % R0_num_steps == 0):
        percent_done = (i / allowed_R0_len) * 100
        print(f"Processed {i} / {allowed_R0_len} R0 values ({percent_done:.2f}% done)")

stop_int_loop = timeit.default_timer()
execution_time_loop = stop_int_loop - start_int_loop

# TODO 11.7: printing the results
print(f"It took '{execution_time_loop:.3f} s' to check valid values of 'R0'.")
print(f"the lists are: \n"
      f"unsuccessful_R0  = {unsuccessful_R0} \n"
      f"successful_R0    = {successful_R0} \n"
      f"terminal_errors  = {terminal_error_list} \n")    ##### NEW CODE #####