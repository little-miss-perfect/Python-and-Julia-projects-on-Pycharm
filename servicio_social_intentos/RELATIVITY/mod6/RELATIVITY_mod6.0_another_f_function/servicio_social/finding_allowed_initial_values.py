from events import *


# TODO 11: first check the allowed positive initial conditions (then we'll do the negative)


# TODO 11.1: some constants
print(f"The list we're looking through is:\n{allowed_R0}\n")

allowed_R0_len = len(allowed_R0)
R0_num_steps = 10  # print progress notification every "R0_num_steps" iterations

# TODO 11.5: the empty lists
successful_R0 = []
unsuccessful_R0 = []
terminal_error_list = []

# TODO 11.6: the loop
start_int_loop = timeit.default_timer()

for i, R0_value in enumerate(allowed_R0, start=1):
    r0[2] = R0_value  # update initial condition
    print(f"the current 'R0' value is: \n{R0_value}\n")

    integrator = solve_int


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
          f"concave down-up: {x_events[2]} \n"
          f"concave up-down: {x_events[3]} \n")

    if x_events is None:
        # no events => success
        successful_R0.append(R0_value)
    else:
        nan_inf_times = x_events[0]
        div_times = x_events[1]
        concave_DU_times = x_events[2]
        concave_UD_times = x_events[3]

        # check for undefined values
        if len(nan_inf_times) > 0:
            unsuccessful_R0.append(R0_value)
        # if the solution diverged
        elif len(div_times) > 0:
            unsuccessful_R0.append(R0_value)
            # if concavity was detected
        elif len(concave_DU_times) or len(concave_UD_times) > 0:
            successful_R0.append(R0_value)
        else:
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
      f"terminal_errors  = {terminal_error_list} \n")
