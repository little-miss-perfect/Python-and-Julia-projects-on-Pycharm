from plotting_allowed_initial_values import *

threshold = 1e23  # this is ridiculously high, right? why not use something like "1e3"?




def divergence_event(x, r):
    drdx = F(x, r)
    # Check if any component is NaN or Inf
    if np.any(np.isnan(drdx)) or np.any(np.isinf(drdx)):  # this checks if there are any "NaNs" in the derivative array or if there are any "Infs" (infinite values) in the derivative array.
        return 0.0  # Trigger event immediately if invalid values appear.

    # Consider divergence if the largest absolute derivative exceeds the threshold.
    max_derivative = np.max(np.abs(drdx))
    return max_derivative - threshold

divergence_event.terminal = True  # which stops the integration when our criteria is met
divergence_event.direction = 0  # this is related to the "zero-crossing"




nan_inf_evt  = make_nan_inf_event(F)
first_evt    = make_first_crossing_event(F, threshold=threshold)
second_evt   = make_second_crossing_event(F, threshold=threshold)




# this is just so that we can maybe select a specific set of "x" values
x_end = 13
step_size = 1e-4
spacing = [np.arange(0, x_end, step_size), None]
space = spacing[1]  # use index "1" for Scipy to decide the integration step sizes
# we'd like to modify "r0[2]".
r0[2] = 999  # and this is how we'll modify this value.

int_R_div = ODEIntegrator(F, r0, x_start=0, x_end=x_end, events=[divergence_event], t_eval=space)
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
