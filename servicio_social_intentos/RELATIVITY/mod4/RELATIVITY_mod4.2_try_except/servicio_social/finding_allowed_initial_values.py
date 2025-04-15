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
        method='LSODA',
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