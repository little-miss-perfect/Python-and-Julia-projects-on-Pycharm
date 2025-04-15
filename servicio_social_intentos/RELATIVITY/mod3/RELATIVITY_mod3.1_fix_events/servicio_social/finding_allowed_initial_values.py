from vectorized_derivative import *
from class_definitions.integrations import *

# TODO 11: first check the allowed positive initial conditions (then we'll do the negative)
# this is where we've been stuck for a while


# TODO 11.1 : events functions
def make_nan_inf_event(F):
    """
    this stops the solver immediately if any derivative component is NaN or Inf.
    this is the "extreme" case of the function "make_divergence_event".
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
    a single 'divergence' event that stops as soon as 'max(abs(drdt))' exceeds 'big_threshold'.
    if this event triggers, we'll consider the solution 'unsuccessful' due to a 'blow-up'.
    """

    def event(t, y):
        drdt = F(t, y)
        return np.max(np.abs(drdt)) - big_threshold

    event.terminal = True
    event.direction = 1  # detect going from below threshold to above threshold (our derivative gets too big -in absolute value. that is, the function blows up/down; it diverges)
    return event


def make_small_divergence_event(F, big_threshold):
    """
    a single 'divergence' event that stops as soon as 'max(abs(drdt))' exceeds 'big_threshold'.
    if this event triggers, we'll consider the solution 'unsuccessful' due to a 'blow-up'.
    """

    def event(t, y):
        drdt = F(t, y)
        return np.min(np.abs(drdt)) - big_threshold

    event.terminal = True
    event.direction = 1  # detect going from below threshold to above threshold (our derivative gets too big -in absolute value. that is, the function blows up/down; it diverges)
    return event


def make_first_crossing_event(F, small_threshold):
    """
    a non-terminal upward crossing from below the threshold to above the threshold is detected.
    we won't stop the integration here, but we'll record that we crossed the threshold once.
    """

    def event(t, y):
        drdt = F(t, y)

        return np.max(np.abs(drdt)) - small_threshold

    event.terminal = False
    event.direction = 1  # upward crossing: the derivative has exceeded the threshold, something is starting to blow up/down.

    return event


# do we really need this next condition?
def make_second_crossing_event(F, small_threshold):
    """
    a terminal downward crossing from above the threshold back to below the threshold is detected.
    if this event is triggered, we consider it 'successful' because it returned the derivative's value below the threshold.
    """

    def event(t, y):
        drdt = F(t, y)

        return np.max(np.abs(drdt)) - small_threshold

    event.terminal = True
    event.direction = -1  # downward crossing: the derivative has gone below the threshold, this is good, this means we've come back to some kind of "stability". in our case, we're back to having a "constamt-like" behaviour

    return event


# TODO 11.2 : "parameters" to be used

# the integration range
x_end = 1e1
# and we pick an arbitrary "threshold = 1e3" for the 'dip'.
# this is chosen so that "normal derivative spikes" are recognized, but "crazy blow-ups" or no "dips" are distinguished.
threshold_small = 1e2  # used for first/second crossing (the first "dip" in the solution)
threshold_big = 1e5  # used for 'big divergence' event

# TODO 11.3 : setting the events
nan_inf_evt = make_nan_inf_event(F)
max_div_evt = make_divergence_event(F, big_threshold=threshold_big)
min_div_evt = make_small_divergence_event(F, big_threshold=threshold_big)
first_evt = make_first_crossing_event(F, small_threshold=threshold_small)
second_evt = make_second_crossing_event(F, small_threshold=threshold_small)

# we'll just use these events:
all_events = [nan_inf_evt, max_div_evt, min_div_evt, first_evt, second_evt]
# all_events = [nan_inf_evt, big_div_evt, first_evt]
# all_events = [nan_inf_evt, big_div_evt]
# all_events = [big_div_evt]

# TODO 11.4 : "R0" range (to be modified manually) and parameters for the loop
start = 0

R0_start = start
R0_increment = 1
quantity = 13  # amount of points ("R0" values) in the list to check
R0_end = start + quantity * R0_increment

R0_a = np.arange(start=R0_start, stop=R0_end, step=R0_increment)
R0_b = np.array([0])  # "annoying" values to skip
allowed_R0 = np.setdiff1d(R0_a, R0_b)
print(f"the list we're looking through is:"
      f"\n {allowed_R0} \n")

allowed_R0_len = len(allowed_R0)
R0_num_steps = 10  # print progress notification every 10 iterations

# the empty lists
successful_R0 = []
unsuccessful_R0 = []




# TODO 11.5 : the loop
start_int_loop = timeit.default_timer()

# for i, R0_value in enumerate(allowed_R0, start=1):
#     r0[2] = R0_value  # update initial condition
#
#     integrator = ODEIntegrator(
#         F=F,
#         r0=r0,
#         x_start=0,
#         x_end=x_end,
#         events=all_events,  # Only the NaN/Inf & divergence events
#         method='BDF'
#     )
#     integrator.integrate()
#
#     t_events, y_events = integrator.get_events()
#
#     if t_events is None:
#         # No events => solution never triggered NaN/Inf or big divergence => success
#         successful_R0.append(R0_value)
#     else:
#         big_div_times = t_events[0]
#
#         # If any event triggered => unsuccessful
#         if len(big_div_times) > 0:
#             unsuccessful_R0.append(R0_value)
#         else:
#             # If both arrays are empty => no event => success
#             successful_R0.append(R0_value)
#
#     # Print progress every R0_num_steps
#     if R0_num_steps != 0 and (i % R0_num_steps == 0):
#         percent_done = (i / allowed_R0_len) * 100
#         print(f"Processed {i} / {allowed_R0_len} R0 values ({percent_done:.2f}% done)")

# for i, R0_value in enumerate(allowed_R0, start=1):
#     r0[2] = R0_value  # update initial condition
#
#     integrator = ODEIntegrator(
#         F=F,
#         r0=r0,
#         x_start=0,
#         x_end=x_end,
#         events=all_events,
#         method='BDF'  # or whichever method works best for your problem
#     )
#     integrator.integrate()
#
#     t_events, y_events = integrator.get_events()
#
#     if t_events is None:
#         # No events => never crossed threshold => stable entire time => success
#         successful_R0.append(R0_value)
#     else:
#         # We have 3 event arrays: [nan_inf_times, first_times, second_times]
#         nan_inf_times = t_events[0]
#         first_cross_times = t_events[1]
#         second_cross_times = t_events[2]
#
#         if len(nan_inf_times) > 0:
#             # NaN/Inf => unsuccessful
#             unsuccessful_R0.append(R0_value)
#
#         elif len(second_cross_times) > 0:
#             # 2nd crossing => success (the dip returned to stable)
#             successful_R0.append(R0_value)
#
#         elif len(first_cross_times) > 0:
#             # Only the first crossing => unsuccessful
#             # (we 'dipped' but never came back => doesn't match your negative logistic pattern)
#             unsuccessful_R0.append(R0_value)
#
#         else:
#             # t_events isn't None but arrays are empty => no crossing => success
#             successful_R0.append(R0_value)
#
#     # Print progress every so often
#     if R0_num_steps != 0 and (i % R0_num_steps == 0):
#         percent_done = (i / allowed_R0_len) * 100
#         print(f"Processed {i} / {allowed_R0_len} R0 values ({percent_done:.2f}% done)")

for i, R0_value in enumerate(allowed_R0, start=1):
    r0[2] = R0_value  # update initial condition
    print(f"the current 'R0' value is: \n"
          f"{R0_value} \n")

    integrator = ODEIntegrator(
        F=F,
        r0=r0,
        x_start=0,
        x_end=x_end,
        events=all_events,  # "[nan_inf_evt, big_div_evt, first_evt, second_evt]" presumably
        method='BDF',
        max_step=1
    )
    integrator.integrate()

    x_events, r_events = integrator.get_events()
    print(f"the current events are \n"
          f"NaN/Inf: {x_events[0]} \n"
          f"max_div: {x_events[1]} \n"
          f"min_div: {x_events[2]} \n"
          f"first_evt: {x_events[3]} \n"
          f"second_evt: {x_events[4]} \n")

    if x_events is None:
        # does "no events" imply the integration terminated successfully?
        successful_R0.append(R0_value)
    else:
        # all_events = [nan_inf_evt, big_div_evt, first_evt, second_evt]
        nan_inf_times   = x_events[0]
        max_div_times = x_events[1]
        min_div_times = x_events[2]
        first_cross_times  = x_events[3]
        second_cross_times = x_events[4]

        # 1) If we ever had NaN/Inf => unsuccessful
        if len(nan_inf_times) > 0:
            unsuccessful_R0.append(R0_value)

        # 2) otherwise, we want a "stable->dip->stable" behaviour, that is, both first and second crossing.
        #    if the second crossing times list is non-empty, that means the solver triggered
        #    a "return to stable" behaviour and stopped. but let's also ensure we "had" a dip.
        elif (len(first_cross_times) > 0) and (len(second_cross_times) > 0):
            # if this behaviour occurs, then it's what we considered to be successful
            successful_R0.append(R0_value)

        elif len(max_div_times) > 0 or len(min_div_times) > 0:  # this goes here at the end because we want the loop to have checked for all those previous conditions before looking for a "divergence" (if we were thinking of putting this condition after the "NaN_Inf" condition, we might want to ask ourselves: what if it had the correct behaviour and then diverged, but we told our program to consider any divergence as unsuccessful? we wouldn't be considering the correct case, right? I think that's why the conditions should have the order they have currently)
            unsuccessful_R0.append(R0_value)

        else:
            # would any other scenario be successful?
            # e.g. no crossing, or only one crossing, or second crossing somehow
            # without first crossing (which sounds unlikely, but we might want to consider it just in case)
            successful_R0.append(R0_value)

    # Print progress
    if R0_num_steps != 0 and (i % R0_num_steps == 0):
        percent_done = (i / allowed_R0_len) * 100
        print(f"Processed {i} / {allowed_R0_len} R0 values ({percent_done:.2f}% done)")


stop_int_loop = timeit.default_timer()
execution_time_loop = stop_int_loop - start_int_loop




# TODO 11.6 : printing the results (of the loop)
print(f"It took '{execution_time_loop:.3f} s' to check valid values of 'R0'.")
print(f"the lists are: \n"
      f"unsuccessful_R0 = {unsuccessful_R0} \n"
      f"successful_R0   = {successful_R0} \n")
