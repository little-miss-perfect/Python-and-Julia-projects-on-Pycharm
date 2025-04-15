from vectorized_derivative import *
from class_definitions.integrations import *
from class_definitions.plots import *


r0[2] = 170  # but we usually start here at "170"


# todo "ALSO CONSIDER"... that negative values give valid solutions; but do they give "stable" solutions?




# TODO p.1: some constants
threshold_small = 1e2  # used for first/second crossing (the first "dip" in the solution)
threshold_big = 1e5  # used for 'big divergence' event




# TODO p.2: events functions
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




# TODO p.3:
nan_inf_evt = make_nan_inf_event(F)
big_div_evt = make_divergence_event(F, big_threshold=threshold_big)
first_evt = make_first_crossing_event(F, small_threshold=threshold_small)
second_evt = make_second_crossing_event(F, small_threshold=threshold_small)

all_events = [nan_inf_evt, big_div_evt, first_evt, second_evt]
# all_events = [nan_inf_evt, big_div_evt, first_evt]
# all_events = [nan_inf_evt, big_div_evt]
# all_events = [nan_inf_evt]
# all_events = [big_div_evt]
# all_events = []




# TODO p.4:
# this is just so that we can maybe select a specific set of "x" values
x_end = 4e1
step_size = 1e-5
spacing = [np.arange(0, x_end, step_size), None]
space = spacing[1]  # use index "1" for Scipy to decide the integration step sizes.




# TODO p.5: choose "R0" and integrate
# we'd like to modify "r0[2]". also, note that the interval "(0, 1.4]" has a sort of "inverse/mirrored" logistic behaviour (to our target behaviour)
# that sort of moves to an exponential behaviour after the endpoint of this interval, to finally "converge" to the logistic behaviour we expect from the solution given by "R0=170" (the one we knew worked).
r0[2] = 5  # and this is how we'll modify this value. "5" gives a divergence.
print(f"the current 'R0' value is: \n"
          f"{r0[2]} \n")

int_R = ODEIntegrator(
                    F=F,
                    r0=r0,
                    x_start=0,
                    x_end=x_end,
                    events=all_events,
                    t_eval=space,
                    method='BDF',  # or whichever method works best (remember that our problem is stiff at some parts of the integration)
                    max_step=1
                )

start_int_timed = timeit.default_timer()
int_R.integrate()
stop_int_timed = timeit.default_timer()

execution_time_timed = stop_int_timed - start_int_timed
print(f"\n done 1/2: \n"
      f"integrated for '{execution_time_timed} s'")




# TODO p.6:
r_R_execution_time = int_R.get_execution_time()
x_R, r_R = int_R.get_solution()
x_R_events, r_R_events = int_R.get_events()  # here are the "events"
print("\n done 2/2: \n"
      "plotted \n \n \n \n")
r_R_plotter = ODESolutionPlotter(x_R, r_R, r_R_execution_time, R0=r0[2])
r_R_plotter.plot(component=2, x_log_scale=True)




# TODO p.7: this gives us the events
# if x_R_events is not None and len(x_R_events[0]) > 0:
#     divergence_x = x_R_events[0][0]
#     print(f"Event triggered at 'x={divergence_x}'")




# print(type(x_R_events))
# print(x_R_events)
print(f"\n the current events are \n"
          f"\n NaN/Inf: {x_R_events[0]} \n"
          f"\n div: {x_R_events[1]} \n"
          f"\n first_evt: {x_R_events[2]} \n"
          f"\n second_evt: {x_R_events[3]} \n")

print(x_R[-1])
