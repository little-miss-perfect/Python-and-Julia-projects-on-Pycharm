# from vectorized_derivative import *
# from class_definitions.integrations import *
#
# # TODO 11: first check the allowed positive initial conditions (then we'll do the negative)
#
# threshold = 1e6
#
# # def divergence_event(x, r):
# #
# #     drdx = F(x, r)
# #
# #     if np.any(np.isnan(drdx)) or np.any(np.isinf(drdx)):
# #         return 0.0
# #
# #     max_derivative = np.max(np.abs(drdx))
# #     return max_derivative - threshold
# #
# # divergence_event.terminal = True
# # divergence_event.direction = 0
# #
# # def make_pattern_event(F, near_zero_threshold=1e-6):
# #     # Define initial phase
# #     phase = 'initial_stable'
# #
# #     def pattern_event(x, r):
# #         nonlocal phase
# #         val = F(x, r)[2]
# #         is_stable = (abs(val) < near_zero_threshold)
# #
# #         if phase == 'initial_stable':
# #             # Initially stable. Once we see a value that's not stable, transition to the next phase.
# #             if not is_stable:
# #                 phase = 'waiting_for_final_stability'
# #             # Return negative value so no event is triggered yet.
# #             return -1.0
# #
# #         elif phase == 'waiting_for_final_stability':
# #             # We have seen instability, now we're waiting to return to stable.
# #             if is_stable:
# #                 # Pattern complete: stable -> unstable -> stable again
# #                 return 0.0  # This triggers the event.
# #             else:
# #                 return -1.0
# #
# #     pattern_event.terminal = True
# #     pattern_event.direction = 0
# #     return pattern_event
# #
# # divergence_event.terminal = True
# # divergence_event.direction = 0
# #
# # pattern_event = make_pattern_event(F, near_zero_threshold=1e-6)
# #
# # def divergence_event_counter(x, r):
# #
# #     drdx = F(x, r)
# #
# #     if np.any(np.isnan(drdx)) or np.any(np.isinf(drdx)):  # "any" checks if there are 'any' nonzero values of the argument and returns a boolean variable
# #         return 0.0
# #
# #     max_derivative = np.max(np.abs(drdx))
# #     return max_derivative - threshold
# #
# # divergence_event.terminal = True
# # divergence_event.direction = 0
#
#
# # def make_nan_inf_event(F):
# #     """
# #     Stops the solver immediately if any derivative component is NaN or Inf.
# #     This is useful to catch numerical breakdowns or divisions by zero.
# #     """
# #
# #     def event(t, y):
# #         drdt = F(t, y)
# #         if np.any(np.isnan(drdt)) or np.any(np.isinf(drdt)):
# #             # Return 0.0 => zero crossing => event triggers
# #             return 0.0
# #         # Return a negative value so no event is detected otherwise
# #         return -1.0
# #
# #     event.terminal = True  # Stop the solver immediately if NaN/Inf is found
# #     event.direction = 0  # Detect crossing in both directions
# #     return event
# #
# #
# # def make_divergence_event(F, big_threshold):
# #     """
# #     A single divergence event:
# #     - Triggers (terminal) the first time max(abs(drdt)) exceeds 'big_threshold'.
# #     - Ideal if you want to stop as soon as the derivative is "too large".
# #     """
# #
# #     def event(t, y):
# #         drdt = F(t, y)
# #         val = np.max(np.abs(drdt)) - big_threshold
# #         return val
# #
# #     event.terminal = True  # Stop integration at the first crossing
# #     event.direction = 1  # Detect only upward crossing from below threshold to above
# #     return event
# #
# #
# # def make_first_crossing_event(F, threshold):
# #     """
# #     Returns an event function that detects when the maximum absolute derivative
# #     crosses 'threshold' for the FIRST time, but does NOT stop the solver.
# #     (non-terminal)
# #
# #     Typically used if you want a second event to handle the "second crossing".
# #     """
# #
# #     def event(t, y):
# #         drdt = F(t, y)
# #         return np.max(np.abs(drdt)) - threshold
# #
# #     event.terminal = False  # Do not stop on first crossing
# #     event.direction = 1  # Crossing from below threshold to above threshold
# #     return event
# #
# #
# # def make_second_crossing_event(F, threshold):
# #     """
# #     Returns an event function that detects when max(abs(drdt)) crosses
# #     the same 'threshold' again (in the opposite direction),
# #     and stops the solver (terminal=True).
# #
# #     Typically used in conjunction with 'make_first_crossing_event'.
# #     """
# #
# #     def event(t, y):
# #         drdt = F(t, y)
# #         return np.max(np.abs(drdt)) - threshold
# #
# #     event.terminal = True  # Stop on second crossing
# #     event.direction = -1  # Crossing from above threshold back down below threshold
# #     return event
# #
#
#
#
# # # end the integration at the following
# # x_end = 1e10
# #
# # # check these "R0" values
# # R0_start = 0
# # R0_end = 4
# # R0_increment = 1
# #
# #
# #
# #
# # # exclude the values we've found to be... "annoying" (time-consuming)
# # # a = np.arange(start=0, stop=1e9, step=1)
# # R0_a = np.arange(start=R0_start, stop=R0_end, step=R0_increment)  # "arange" doesn't consider the last element
# # R0_b = np.array([0, 1e3])  # these are values we've already found which either take too long to compute or don't give a solution
# # allowed_R0 = np.setdiff1d(R0_a, R0_b)
# #
# # allowed_R0_len = len(allowed_R0)
# # R0_num_steps = 10  # print progress every 10 iterations, for example
# # # or...
# # R0_num_steps = (R0_start - R0_end) / 8  # every "eighth of the way"
# #
# #
# #
# #
# # successful_R0 = []
# # unsuccessful_R0 = []
# #
# # # start the loop
# # start_int_loop = timeit.default_timer()
# #
# # for i, R0_value in enumerate(allowed_R0, start=1):  # "enumerate" will associate a tuple with the corresponding positioning index on every element of its input. you could see this by printing out "list(enumerate(allowed_R0, start=1))". and it starts indexing from "1" and not from "0", because that's what we specified.
# #     r0[2] = R0_value
# #
# #     int_R_div = ODEIntegrator(F, r0, x_start=0, x_end=x_end, events=[divergence_event, pattern_event])
# #     int_R_div.integrate()
# #
# #     x_events, r_events = int_R_div.get_events()
# #
# #     # Check event outcomes:
# #     if x_events is None:
# #         # No events were triggered, consider this a success
# #         successful_R0.append(R0_value)
# #     else:
# #         # x_events is [x_events_for_divergence, x_events_for_pattern]
# #         divergence_positions = x_events[0]
# #         pattern_positions = x_events[1]
# #
# #         if divergence_positions.size > 0:
# #             # Divergence event triggered: unsuccessful
# #             unsuccessful_R0.append(R0_value)
# #         elif pattern_positions.size > 0:
# #             # Pattern event triggered: successful
# #             successful_R0.append(R0_value)
# #         else:
# #             # Neither event triggered, solution ended normally
# #             successful_R0.append(R0_value)
# #
# #     # Print progress every R0_num_steps iterations
# #     if i % R0_num_steps == 0:  # this is why we started indexing at "1" and not at zero, right?
# #         percent_done = (i / allowed_R0_len) * 100
# #         print(f"Processed {i} out of {allowed_R0_len} R0 values ({percent_done:.2f}% done)")
# #
# # stop_int_loop = timeit.default_timer()
# #
# # execution_time_loop = stop_int_loop - start_int_loop
# #
# # print(f"it's took '{execution_time_loop} s' for us to check valid values of 'R0'")
# #
# # print(f" unsuccessful_R0 = {unsuccessful_R0}"
# #       f" \n successful_R0 ={successful_R0}")
#
#
#
#
# # nan_inf_evt  = make_nan_inf_event(F)
# # first_evt    = make_first_crossing_event(F, threshold=threshold)
# # second_evt   = make_second_crossing_event(F, threshold=threshold)
# #
# # # end the integration at the following
# # x_end = 13
# #
# # # check these "R0" values
# # R0_start = 1.89
# # R0_end = 1.90
# # R0_increment = 0.01
# #
# # R0_a = np.arange(start=R0_start, stop=R0_end, step=R0_increment)
# # R0_b = np.array([0, 13, 1e3])  # "annoying" values
# # allowed_R0 = np.setdiff1d(R0_a, R0_b)
# #
# # allowed_R0_len = len(allowed_R0)
# # R0_num_steps = 10  # or any logic you'd like for printing progress
# #
# # successful_R0 = []
# # unsuccessful_R0 = []
# #
# # start_int_loop = timeit.default_timer()
# #
# # for i, R0_value in enumerate(allowed_R0, start=1):
# #     r0[2] = R0_value
# #
# #     # Build your integrator with the three events:
# #     integrator = ODEIntegrator(
# #         F=F,
# #         r0=r0,
# #         x_start=0,
# #         x_end=x_end,
# #         events=[nan_inf_evt, first_evt, second_evt]  # THE KEY PART
# #     )
# #     integrator.integrate()
# #
# #     t_events, y_events = integrator.get_events()
# #
# #     # Check event outcomes according to your custom logic:
# #     if t_events is None:
# #         # No events triggered at all => "successful"
# #         successful_R0.append(R0_value)
# #     else:
# #         # We have 3 event arrays in t_events: [nan_inf_times, first_crossing_times, second_crossing_times]
# #         nan_inf_times = t_events[0]
# #         first_crossing_times = t_events[1]
# #         second_crossing_times = t_events[2]
# #
# #         if len(nan_inf_times) > 0:
# #             # NaN/Inf => unsuccessful
# #             unsuccessful_R0.append(R0_value)
# #         elif len(second_crossing_times) > 0:
# #             # Second crossing => successful
# #             successful_R0.append(R0_value)
# #         elif len(first_crossing_times) > 0:
# #             # Only the first crossing was detected => skip (do nothing)
# #             # (i.e., don't append to either list)
# #             pass
# #
# #         else:
# #             # t_events is not None, but all arrays are empty => effectively no event => successful
# #             successful_R0.append(R0_value)
# #
# #     # Print progress every R0_num_steps
# #     if R0_num_steps != 0 and (i % R0_num_steps == 0):
# #         percent_done = (i / allowed_R0_len) * 100
# #         print(f"Processed {i} out of {allowed_R0_len} R0 values ({percent_done:.2f}% done)")
# #
# #     print(f"R0 is {R0_value}"
# #           f"\n and the events triggered were:"
# #           f"\n nan_inf_evt: {t_events[0]}"
# #           f"\n first_evt: {t_events[1]}"
# #           f"\n second_evt: {t_events[2]}")
# #
# # stop_int_loop = timeit.default_timer()
# # execution_time_loop = stop_int_loop - start_int_loop
# #
# # print(f"It took {execution_time_loop:.3f}s to check valid values of 'R0'.")
# # print(f"unsuccessful_R0 = {unsuccessful_R0}")
# # print(f"successful_R0 = {successful_R0}")
#
# def make_nan_inf_event(F):
#     """
#     Stops the solver immediately if any derivative component is NaN or Inf.
#     """
#
#     def event(t, y):
#         drdt = F(t, y)
#         if np.any(np.isnan(drdt)) or np.any(np.isinf(drdt)):
#             return 0.0  # triggers the event
#         return -1.0  # no event otherwise
#
#     event.terminal = True
#     event.direction = 0
#     return event
#
#
# def make_divergence_event(F, big_threshold):
#     """
#     A single 'divergence' event that stops as soon as max(abs(drdt)) exceeds 'big_threshold'.
#     If this event triggers, we'll consider the solution 'unsuccessful' due to blow-up.
#     """
#
#     def event(t, y):
#         drdt = F(t, y)
#         val = np.max(np.abs(drdt)) - big_threshold
#         return val
#
#     event.terminal = True
#     event.direction = 1  # detect going from below threshold to above threshold
#     return event
#
#
# def make_first_crossing_event(F, threshold):
#     """
#     Non-terminal upward crossing from below threshold to above threshold.
#     We won't stop here, but we'll record that we crossed once.
#     """
#
#     def event(t, y):
#         drdt = F(t, y)
#         return np.max(np.abs(drdt)) - threshold
#
#     event.terminal = False
#     event.direction = 1  # upward crossing
#     return event
#
#
# def make_second_crossing_event(F, threshold):
#     """
#     Terminal downward crossing from above threshold back to below threshold.
#     If triggered, we consider it 'successful' because it returned below threshold.
#     """
#
#     def event(t, y):
#         drdt = F(t, y)
#         return np.max(np.abs(drdt)) - threshold
#
#     event.terminal = True
#     event.direction = -1  # downward crossing
#     return event
#
#
# ###################################
# # 2) USING ALL FOUR EVENTS IN A LOOP
# ###################################
#
# # Example thresholds:
# threshold_small = 1e3  # used for first/second crossing
# threshold_big = 1e17  # used for 'big divergence' event
#
# # Instantiate event functions:
# nan_inf_evt = make_nan_inf_event(F)
# big_div_evt = make_divergence_event(F, big_threshold=threshold_big)
# first_evt = make_first_crossing_event(F, threshold_small)
# second_evt = make_second_crossing_event(F, threshold_small)
#
# # You can reorder them if you like; the solver will monitor all:
# # The index in t_events will match the order here.
# # t_events[0] -> nan_inf_evt
# # t_events[1] -> big_div_evt
# # t_events[2] -> first_evt
# # t_events[3] -> second_evt
# all_events = [nan_inf_evt, big_div_evt, first_evt, second_evt]
#
# # Integration range:
# x_end = 13
#
#
# ###################################
# # 3) HERE'S WHERE WE SEARCH
# ###################################
#
# # Define the R0 range:
# R0_start = 999
# R0_end = 1e3 + 1
# R0_increment = 1
#
# R0_a = np.arange(start=R0_start, stop=R0_end, step=R0_increment)
# R0_b = np.array([0, 1e3])  # "annoying" values to skip
# allowed_R0 = np.setdiff1d(R0_a, R0_b)
#
# allowed_R0_len = len(allowed_R0)
# R0_num_steps = 10  # Print progress every 10 iterations
#
# successful_R0 = []
# unsuccessful_R0 = []
#
# start_int_loop = timeit.default_timer()
#
# for i, R0_value in enumerate(allowed_R0, start=1):
#     # Set the initial condition
#     r0[2] = R0_value
#
#     # Build integrator with all four events:
#     integrator = ODEIntegrator(
#         F=F,
#         r0=r0,
#         x_start=0,
#         x_end=x_end,
#         events=all_events,  # <--- important!
#         method= 'BDF'  # or any method you prefer
#     )
#     integrator.integrate()
#
#     t_events, y_events = integrator.get_events()
#
#     ##################################
#     # 3) CLASSIFY THE OUTCOME
#     ##################################
#     if t_events is None:
#         # No events => success
#         successful_R0.append(R0_value)
#     else:
#         # We have four arrays in t_events, one per event in the order above:
#         nan_inf_times = t_events[0]
#         big_div_times = t_events[1]
#         first_crossing_times = t_events[2]
#         second_crossing_times = t_events[3]
#
#         if len(nan_inf_times) > 0:
#             # NaN/Inf => unsuccessful
#             unsuccessful_R0.append(R0_value)
#
#         elif len(big_div_times) > 0:
#             # 'big divergence' => unsuccessful
#             unsuccessful_R0.append(R0_value)
#
#         elif len(second_crossing_times) > 0:
#             # second crossing => success
#             successful_R0.append(R0_value)
#
#         elif len(first_crossing_times) > 0:
#             # ONLY the first crossing => let's consider it unsuccessful
#             # (since it never returned below threshold_small)
#             unsuccessful_R0.append(R0_value)
#
#         else:
#             # all arrays empty => no event triggered => success
#             successful_R0.append(R0_value)
#
#     # Print progress
#     if R0_num_steps != 0 and (i % R0_num_steps == 0):
#         percent_done = (i / allowed_R0_len) * 100
#         print(f"Processed {i} out of {allowed_R0_len} R0 values ({percent_done:.2f}% done)")
#
#     # Debug: Print which events triggered
#     # print(f"R0 = {R0_value}")
#     # print(f" - nan_inf_evt times:        {t_events[0] if t_events else None}")
#     # print(f" - big_div_evt times:        {t_events[1] if t_events else None}")
#     # print(f" - first_crossing_evt times: {t_events[2] if t_events else None}")
#     # print(f" - second_crossing_evt times:{t_events[3] if t_events else None}")
#     # print()
#
# stop_int_loop = timeit.default_timer()
# execution_time_loop = stop_int_loop - start_int_loop
#
# print(f"It took {execution_time_loop:.3f}s to check valid values of R0.")
# print("unsuccessful_R0 =", unsuccessful_R0)
# print("successful_R0   =", successful_R0)

from vectorized_derivative import *
from class_definitions.integrations import *

# TODO 11: first check the allowed positive initial conditions (then we'll do the negative)

threshold = 1e6
#
# # def divergence_event(x, r):
# #
# #     drdx = F(x, r)
# #
# #     if np.any(np.isnan(drdx)) or np.any(np.isinf(drdx)):
# #         return 0.0
# #
# #     max_derivative = np.max(np.abs(drdx))
# #     return max_derivative - threshold
# #
# # divergence_event.terminal = True
# # divergence_event.direction = 0
# #
# # def make_pattern_event(F, near_zero_threshold=1e-6):
# #     # Define initial phase
# #     phase = 'initial_stable'
# #
# #     def pattern_event(x, r):
# #         nonlocal phase
# #         val = F(x, r)[2]
# #         is_stable = (abs(val) < near_zero_threshold)
# #
# #         if phase == 'initial_stable':
# #             # Initially stable. Once we see a value that's not stable, transition to the next phase.
# #             if not is_stable:
# #                 phase = 'waiting_for_final_stability'
# #             # Return negative value so no event is triggered yet.
# #             return -1.0
# #
# #         elif phase == 'waiting_for_final_stability':
# #             # We have seen instability, now we're waiting to return to stable.
# #             if is_stable:
# #                 # Pattern complete: stable -> unstable -> stable again
# #                 return 0.0  # This triggers the event.
# #             else:
# #                 return -1.0
# #
# #     pattern_event.terminal = True
# #     pattern_event.direction = 0
# #     return pattern_event
# #
# # divergence_event.terminal = True
# # divergence_event.direction = 0
# #
# # pattern_event = make_pattern_event(F, near_zero_threshold=1e-6)
# #
# # def divergence_event_counter(x, r):
# #
# #     drdx = F(x, r)
# #
# #     if np.any(np.isnan(drdx)) or np.any(np.isinf(drdx)):  # "any" checks if there are 'any' nonzero values of the argument and returns a boolean variable
# #         return 0.0
# #
# #     max_derivative = np.max(np.abs(drdx))
# #     return max_derivative - threshold
# #
# # divergence_event.terminal = True
# # divergence_event.direction = 0
#
#
# # def make_nan_inf_event(F):
# #     """
# #     Stops the solver immediately if any derivative component is NaN or Inf.
# #     This is useful to catch numerical breakdowns or divisions by zero.
# #     """
# #
# #     def event(t, y):
# #         drdt = F(t, y)
# #         if np.any(np.isnan(drdt)) or np.any(np.isinf(drdt)):
# #             # Return 0.0 => zero crossing => event triggers
# #             return 0.0
# #         # Return a negative value so no event is detected otherwise
# #         return -1.0
# #
# #     event.terminal = True  # Stop the solver immediately if NaN/Inf is found
# #     event.direction = 0  # Detect crossing in both directions
# #     return event
# #
# #
# # def make_divergence_event(F, big_threshold):
# #     """
# #     A single divergence event:
# #     - Triggers (terminal) the first time max(abs(drdt)) exceeds 'big_threshold'.
# #     - Ideal if you want to stop as soon as the derivative is "too large".
# #     """
# #
# #     def event(t, y):
# #         drdt = F(t, y)
# #         val = np.max(np.abs(drdt)) - big_threshold
# #         return val
# #
# #     event.terminal = True  # Stop integration at the first crossing
# #     event.direction = 1  # Detect only upward crossing from below threshold to above
# #     return event
# #
# #
# # def make_first_crossing_event(F, threshold):
# #     """
# #     Returns an event function that detects when the maximum absolute derivative
# #     crosses 'threshold' for the FIRST time, but does NOT stop the solver.
# #     (non-terminal)
# #
# #     Typically used if you want a second event to handle the "second crossing".
# #     """
# #
# #     def event(t, y):
# #         drdt = F(t, y)
# #         return np.max(np.abs(drdt)) - threshold
# #
# #     event.terminal = False  # Do not stop on first crossing
# #     event.direction = 1  # Crossing from below threshold to above threshold
# #     return event
# #
# #
# # def make_second_crossing_event(F, threshold):
# #     """
# #     Returns an event function that detects when max(abs(drdt)) crosses
# #     the same 'threshold' again (in the opposite direction),
# #     and stops the solver (terminal=True).
# #
# #     Typically used in conjunction with 'make_first_crossing_event'.
# #     """
# #
# #     def event(t, y):
# #         drdt = F(t, y)
# #         return np.max(np.abs(drdt)) - threshold
# #
# #     event.terminal = True  # Stop on second crossing
# #     event.direction = -1  # Crossing from above threshold back down below threshold
# #     return event
# #
#
#
#
# # # end the integration at the following
# # x_end = 1e10
# #
# # # check these "R0" values
# # R0_start = 0
# # R0_end = 4
# # R0_increment = 1
# #
# #
# #
# #
# # # exclude the values we've found to be... "annoying" (time-consuming)
# # # a = np.arange(start=0, stop=1e9, step=1)
# # R0_a = np.arange(start=R0_start, stop=R0_end, step=R0_increment)  # "arange" doesn't consider the last element
# # R0_b = np.array([0, 1e3])  # these are values we've already found which either take too long to compute or don't give a solution
# # allowed_R0 = np.setdiff1d(R0_a, R0_b)
# #
# # allowed_R0_len = len(allowed_R0)
# # R0_num_steps = 10  # print progress every 10 iterations, for example
# # # or...
# # R0_num_steps = (R0_start - R0_end) / 8  # every "eighth of the way"
# #
# #
# #
# #
# # successful_R0 = []
# # unsuccessful_R0 = []
# #
# # # start the loop
# # start_int_loop = timeit.default_timer()
# #
# # for i, R0_value in enumerate(allowed_R0, start=1):  # "enumerate" will associate a tuple with the corresponding positioning index on every element of its input. you could see this by printing out "list(enumerate(allowed_R0, start=1))". and it starts indexing from "1" and not from "0", because that's what we specified.
# #     r0[2] = R0_value
# #
# #     int_R_div = ODEIntegrator(F, r0, x_start=0, x_end=x_end, events=[divergence_event, pattern_event])
# #     int_R_div.integrate()
# #
# #     x_events, r_events = int_R_div.get_events()
# #
# #     # Check event outcomes:
# #     if x_events is None:
# #         # No events were triggered, consider this a success
# #         successful_R0.append(R0_value)
# #     else:
# #         # x_events is [x_events_for_divergence, x_events_for_pattern]
# #         divergence_positions = x_events[0]
# #         pattern_positions = x_events[1]
# #
# #         if divergence_positions.size > 0:
# #             # Divergence event triggered: unsuccessful
# #             unsuccessful_R0.append(R0_value)
# #         elif pattern_positions.size > 0:
# #             # Pattern event triggered: successful
# #             successful_R0.append(R0_value)
# #         else:
# #             # Neither event triggered, solution ended normally
# #             successful_R0.append(R0_value)
# #
# #     # Print progress every R0_num_steps iterations
# #     if i % R0_num_steps == 0:  # this is why we started indexing at "1" and not at zero, right?
# #         percent_done = (i / allowed_R0_len) * 100
# #         print(f"Processed {i} out of {allowed_R0_len} R0 values ({percent_done:.2f}% done)")
# #
# # stop_int_loop = timeit.default_timer()
# #
# # execution_time_loop = stop_int_loop - start_int_loop
# #
# # print(f"it's took '{execution_time_loop} s' for us to check valid values of 'R0'")
# #
# # print(f" unsuccessful_R0 = {unsuccessful_R0}"
# #       f" \n successful_R0 ={successful_R0}")
#
#
#
#
# # nan_inf_evt  = make_nan_inf_event(F)
# # first_evt    = make_first_crossing_event(F, threshold=threshold)
# # second_evt   = make_second_crossing_event(F, threshold=threshold)
# #
# # # end the integration at the following
# # x_end = 13
# #
# # # check these "R0" values
# # R0_start = 1.89
# # R0_end = 1.90
# # R0_increment = 0.01
# #
# # R0_a = np.arange(start=R0_start, stop=R0_end, step=R0_increment)
# # R0_b = np.array([0, 13, 1e3])  # "annoying" values
# # allowed_R0 = np.setdiff1d(R0_a, R0_b)
# #
# # allowed_R0_len = len(allowed_R0)
# # R0_num_steps = 10  # or any logic you'd like for printing progress
# #
# # successful_R0 = []
# # unsuccessful_R0 = []
# #
# # start_int_loop = timeit.default_timer()
# #
# # for i, R0_value in enumerate(allowed_R0, start=1):
# #     r0[2] = R0_value
# #
# #     # Build your integrator with the three events:
# #     integrator = ODEIntegrator(
# #         F=F,
# #         r0=r0,
# #         x_start=0,
# #         x_end=x_end,
# #         events=[nan_inf_evt, first_evt, second_evt]  # THE KEY PART
# #     )
# #     integrator.integrate()
# #
# #     t_events, y_events = integrator.get_events()
# #
# #     # Check event outcomes according to your custom logic:
# #     if t_events is None:
# #         # No events triggered at all => "successful"
# #         successful_R0.append(R0_value)
# #     else:
# #         # We have 3 event arrays in t_events: [nan_inf_times, first_crossing_times, second_crossing_times]
# #         nan_inf_times = t_events[0]
# #         first_crossing_times = t_events[1]
# #         second_crossing_times = t_events[2]
# #
# #         if len(nan_inf_times) > 0:
# #             # NaN/Inf => unsuccessful
# #             unsuccessful_R0.append(R0_value)
# #         elif len(second_crossing_times) > 0:
# #             # Second crossing => successful
# #             successful_R0.append(R0_value)
# #         elif len(first_crossing_times) > 0:
# #             # Only the first crossing was detected => skip (do nothing)
# #             # (i.e., don't append to either list)
# #             pass
# #
# #         else:
# #             # t_events is not None, but all arrays are empty => effectively no event => successful
# #             successful_R0.append(R0_value)
# #
# #     # Print progress every R0_num_steps
# #     if R0_num_steps != 0 and (i % R0_num_steps == 0):
# #         percent_done = (i / allowed_R0_len) * 100
# #         print(f"Processed {i} out of {allowed_R0_len} R0 values ({percent_done:.2f}% done)")
# #
# #     print(f"R0 is {R0_value}"
# #           f"\n and the events triggered were:"
# #           f"\n nan_inf_evt: {t_events[0]}"
# #           f"\n first_evt: {t_events[1]}"
# #           f"\n second_evt: {t_events[2]}")
# #
# # stop_int_loop = timeit.default_timer()
# # execution_time_loop = stop_int_loop - start_int_loop
# #
# # print(f"It took {execution_time_loop:.3f}s to check valid values of 'R0'.")
# # print(f"unsuccessful_R0 = {unsuccessful_R0}")
# # print(f"successful_R0 = {successful_R0}")
#
# def make_nan_inf_event(F):
#     """
#     Stops the solver immediately if any derivative component is NaN or Inf.
#     """
#
#     def event(t, y):
#         drdt = F(t, y)
#         if np.any(np.isnan(drdt)) or np.any(np.isinf(drdt)):
#             return 0.0  # triggers the event
#         return -1.0  # no event otherwise
#
#     event.terminal = True
#     event.direction = 0
#     return event
#
#
# def make_divergence_event(F, big_threshold):
#     """
#     A single 'divergence' event that stops as soon as max(abs(drdt)) exceeds 'big_threshold'.
#     If this event triggers, we'll consider the solution 'unsuccessful' due to blow-up.
#     """
#
#     def event(t, y):
#         drdt = F(t, y)
#         val = np.max(np.abs(drdt)) - big_threshold
#         return val
#
#     event.terminal = True
#     event.direction = 1  # detect going from below threshold to above threshold
#     return event
#
#
# def make_first_crossing_event(F, threshold):
#     """
#     Non-terminal upward crossing from below threshold to above threshold.
#     We won't stop here, but we'll record that we crossed once.
#     """
#
#     def event(t, y):
#         drdt = F(t, y)
#         return np.max(np.abs(drdt)) - threshold
#
#     event.terminal = False
#     event.direction = 1  # upward crossing
#     return event
#
#
# def make_second_crossing_event(F, threshold):
#     """
#     Terminal downward crossing from above threshold back to below threshold.
#     If triggered, we consider it 'successful' because it returned below threshold.
#     """
#
#     def event(t, y):
#         drdt = F(t, y)
#         return np.max(np.abs(drdt)) - threshold
#
#     event.terminal = True
#     event.direction = -1  # downward crossing
#     return event
#
#
# ###################################
# # 2) USING ALL FOUR EVENTS IN A LOOP
# ###################################
#
# # Example thresholds:
# threshold_small = 1e3  # used for first/second crossing
# threshold_big = 1e17  # used for 'big divergence' event
#
# # Instantiate event functions:
# nan_inf_evt = make_nan_inf_event(F)
# big_div_evt = make_divergence_event(F, big_threshold=threshold_big)
# first_evt = make_first_crossing_event(F, threshold_small)
# second_evt = make_second_crossing_event(F, threshold_small)
#
# # You can reorder them if you like; the solver will monitor all:
# # The index in t_events will match the order here.
# # t_events[0] -> nan_inf_evt
# # t_events[1] -> big_div_evt
# # t_events[2] -> first_evt
# # t_events[3] -> second_evt
# all_events = [nan_inf_evt, big_div_evt, first_evt, second_evt]
#
# # Integration range:
# x_end = 13
#
#
# ###################################
# # 3) HERE'S WHERE WE SEARCH
# ###################################
#
# # Define the R0 range:
# R0_start = 999
# R0_end = 1e3 + 1
# R0_increment = 1
#
# R0_a = np.arange(start=R0_start, stop=R0_end, step=R0_increment)
# R0_b = np.array([0, 1e3])  # "annoying" values to skip
# allowed_R0 = np.setdiff1d(R0_a, R0_b)
#
# allowed_R0_len = len(allowed_R0)
# R0_num_steps = 10  # Print progress every 10 iterations
#
# successful_R0 = []
# unsuccessful_R0 = []
#
# start_int_loop = timeit.default_timer()
#
# for i, R0_value in enumerate(allowed_R0, start=1):
#     # Set the initial condition
#     r0[2] = R0_value
#
#     # Build integrator with all four events:
#     integrator = ODEIntegrator(
#         F=F,
#         r0=r0,
#         x_start=0,
#         x_end=x_end,
#         events=all_events,  # <--- important!
#         method= 'BDF'  # or any method you prefer
#     )
#     integrator.integrate()
#
#     t_events, y_events = integrator.get_events()
#
#     ##################################
#     # 3) CLASSIFY THE OUTCOME
#     ##################################
#     if t_events is None:
#         # No events => success
#         successful_R0.append(R0_value)
#     else:
#         # We have four arrays in t_events, one per event in the order above:
#         nan_inf_times = t_events[0]
#         big_div_times = t_events[1]
#         first_crossing_times = t_events[2]
#         second_crossing_times = t_events[3]
#
#         if len(nan_inf_times) > 0:
#             # NaN/Inf => unsuccessful
#             unsuccessful_R0.append(R0_value)
#
#         elif len(big_div_times) > 0:
#             # 'big divergence' => unsuccessful
#             unsuccessful_R0.append(R0_value)
#
#         elif len(second_crossing_times) > 0:
#             # second crossing => success
#             successful_R0.append(R0_value)
#
#         elif len(first_crossing_times) > 0:
#             # ONLY the first crossing => let's consider it unsuccessful
#             # (since it never returned below threshold_small)
#             unsuccessful_R0.append(R0_value)
#
#         else:
#             # all arrays empty => no event triggered => success
#             successful_R0.append(R0_value)
#
#     # Print progress
#     if R0_num_steps != 0 and (i % R0_num_steps == 0):
#         percent_done = (i / allowed_R0_len) * 100
#         print(f"Processed {i} out of {allowed_R0_len} R0 values ({percent_done:.2f}% done)")
#
#     # Debug: Print which events triggered
#     # print(f"R0 = {R0_value}")
#     # print(f" - nan_inf_evt times:        {t_events[0] if t_events else None}")
#     # print(f" - big_div_evt times:        {t_events[1] if t_events else None}")
#     # print(f" - first_crossing_evt times: {t_events[2] if t_events else None}")
#     # print(f" - second_crossing_evt times:{t_events[3] if t_events else None}")
#     # print()
#
# stop_int_loop = timeit.default_timer()
# execution_time_loop = stop_int_loop - start_int_loop
#
# print(f"It took {execution_time_loop:.3f}s to check valid values of R0.")
# print("unsuccessful_R0 =", unsuccessful_R0)
# print("successful_R0   =", successful_R0)




######################################
# 1) EVENT FUNCTIONS
######################################

def make_nan_inf_event(F):
    """
    Stops the solver immediately if any derivative component is NaN or Inf.
    """

    def event(t, y):
        drdt = F(t, y)
        if np.any(np.isnan(drdt)) or np.any(np.isinf(drdt)):
            return 0.0
        return -1.0

    event.terminal = True
    event.direction = 0
    return event


def make_first_crossing_event(F, threshold):
    """
    Non-terminal upward crossing:
    - We detect when max(abs(drdt)) goes from below threshold to above threshold.
    - This does NOT stop the solver, but we record the crossing.
    """

    def event(t, y):
        drdt = F(t, y)
        return np.max(np.abs(drdt)) - threshold

    event.terminal = False
    event.direction = 1  # crossing upward
    return event


def make_second_crossing_event(F, threshold):
    """
    Terminal downward crossing:
    - We detect when max(abs(drdt)) goes from above threshold back below threshold
    - Once triggered, we consider that the 'stable -> dip -> stable' pattern is completed => success
    """

    def event(t, y):
        drdt = F(t, y)
        return np.max(np.abs(drdt)) - threshold

    event.terminal = True
    event.direction = -1  # crossing downward
    return event


######################################
# 2) BUILD & USE EVENTS IN A LOOP
######################################

# Suppose we pick a threshold = 1e3 for the 'dip'.
# Adjust as needed so that normal derivative spikes are recognized, but "crazy blow-ups" or no dip are distinguished.
threshold_small = 1e3

nan_inf_evt = make_nan_inf_event(F)
first_evt = make_first_crossing_event(F, threshold_small)
second_evt = make_second_crossing_event(F, threshold_small)

# We'll just use these three events:
all_events = [nan_inf_evt, first_evt, second_evt]

# Integration range
x_end = 13

# R0 range (adapt to your case)
start = 170

R0_start = start
R0_end = start + 1
R0_increment = 1

R0_a = np.arange(start=R0_start, stop=R0_end, step=R0_increment)
R0_b = np.array([0])  # "annoying" values to skip
allowed_R0 = np.setdiff1d(R0_a, R0_b)

allowed_R0_len = len(allowed_R0)
R0_num_steps = 10  # print progress every 10 iterations

successful_R0 = []
unsuccessful_R0 = []

start_int_loop = timeit.default_timer()

for i, R0_value in enumerate(allowed_R0, start=1):
    r0[2] = R0_value  # update initial condition

    integrator = ODEIntegrator(
        F=F,
        r0=r0,
        x_start=0,
        x_end=x_end,
        events=all_events,
        method='BDF'  # or whichever method works best for your problem
    )
    integrator.integrate()

    t_events, y_events = integrator.get_events()

    if t_events is None:
        # No events => never crossed threshold => stable entire time => success
        successful_R0.append(R0_value)
    else:
        # We have 3 event arrays: [nan_inf_times, first_times, second_times]
        nan_inf_times = t_events[0]
        first_cross_times = t_events[1]
        second_cross_times = t_events[2]

        if len(nan_inf_times) > 0:
            # NaN/Inf => unsuccessful
            unsuccessful_R0.append(R0_value)

        elif len(second_cross_times) > 0:
            # 2nd crossing => success (the dip returned to stable)
            successful_R0.append(R0_value)

        elif len(first_cross_times) > 0:
            # Only the first crossing => unsuccessful
            # (we 'dipped' but never came back => doesn't match your negative logistic pattern)
            unsuccessful_R0.append(R0_value)

        else:
            # t_events isn't None but arrays are empty => no crossing => success
            successful_R0.append(R0_value)

    # Print progress every so often
    if R0_num_steps != 0 and (i % R0_num_steps == 0):
        percent_done = (i / allowed_R0_len) * 100
        print(f"Processed {i} / {allowed_R0_len} R0 values ({percent_done:.2f}% done)")

stop_int_loop = timeit.default_timer()
execution_time_loop = stop_int_loop - start_int_loop

print(f"It took {execution_time_loop:.3f}s to check valid values of R0.")
print("unsuccessful_R0 =", unsuccessful_R0)
print("successful_R0   =", successful_R0)

