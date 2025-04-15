from servicio_social.finding_allowed_initial_values import all_events
from vectorized_derivative import *
from class_definitions.integrations import *
from class_definitions.plots import *


# todo "ALSO CONSIDER"... that negative values give valid solutions; but do they give "stable" solutions?
# another note is that: once you've found stable solutions, try plotting them with a solution that used "LSODA",
# just to get a few more points to visualize and a "longer" solution.

# TODO p.1: some constants
# "1e3" generally works pretty good. but there's a problem:
# when trying "R0= 9", if we keep the threshold at "1e3", the integrator won't work.
# but if we keep it at "1e7", then it'll plot without a problem.
threshold1 = 1e3
threshold2 = 1e5
threshold3 = 1e7
threshold4 = 1e9
threshold5 = 1e12

num_thresholds = 5
thresh_list = []
all_events = []

for i in range(num_thresholds):

    threshold = 10**(3 + 2 * i)

    def divergence_event(F):

        def event(t, y):

            drdt = F(t, y)

            return np.max(np.abs(drdt)) - threshold

        event.terminal = True
        event.direction = 1

        return event

    thresh_list.append(divergence_event(F))


# TODO p.2: event functions
def nan_inf_event(F):
    """
    this stops the solver immediately if any derivative component is NaN or Inf.
    this is the "extreme" case of the function "make_divergence_event".
    """

    def event(t, y):

        drdt = F(t, y)

        if np.any(np.isnan(drdt)) or np.any(np.isinf(drdt)):
            return 0.0  # this triggers the event

        return -1.0  # this won't trigger the event (the event is only triggered when a zero is detected)

    event.terminal = True
    event.direction = 0

    return event


def concave_event(F):

    def event(t, y):

        drdt = F(t, y)
        R2 = drdt[3]

        return R2

    event.terminal = False  # we'd just like to detect this event, not terminate the solution. not yet.
    event.direction = 0  # in principle, we'd like to only consider "1" since we were told the correct behaviour was a change in "concavity" from "down to up"; which amounts to finding a "change in sign" in our event function from "negative to positive".
    # we set this direction because we've already seen that other solutions (at least ones given a non-negative "R0" value) have this "change in concavity" behaviour.
    # solutions given a negative "R0" value seem to always diverge. but we haven't tested this hypothesis out, yet. maybe we should consider the "concave" criteria as "universal".

    return event


# TODO p.3: the events used
nan_inf_evt = nan_inf_event(F)
all_events.append(nan_inf_evt)
for i in len(thresh_list):
    all_events.append(thresh_list[i])
concave_evt = concave_event(F)
all_events.append(concave_evt)

print(all_events)


# TODO p.4: some parameters
# this is just so that we can maybe select a specific set of "x" values
x_end = 4e1
step_size = 1e-5
spacing = [np.arange(0, x_end, step_size), None]
space = spacing[1]  # we'll use index "1" for Scipy to decide the integration step sizes.


# TODO p.5: choose "R0" and integrate
# we'd like to modify "r0[2]". also, note that the interval "(0, 1.4]" has a sort of "inverse/mirrored" logistic behaviour (to our target behaviour)
# that sort of moves to an exponential behaviour after the endpoint of this interval, to finally "converge" to the logistic behaviour we expect from the solution given by "R0=170" (the one we knew worked).
r0[2] = 9  # and this is how we'll modify this value. "5" gives a divergence.
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
                    max_step=np.inf
                )

start_int_timed = timeit.default_timer()
int_R.integrate()
stop_int_timed = timeit.default_timer()

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
r_R_plotter.plot(component=2, x_log_scale=False)




# TODO p.7: this gives us the events
# print(type(x_R_events))
# print(x_R_events)
print(f"\n the current events are \n"  # [nan_inf_evt, small_div_evt, big_div_evt, concave_evt]
          f"\n NaN/Inf: {x_R_events[0]} \n"
          f"\n small_div: {x_R_events[1]} \n"
          f"\n big_div: {x_R_events[2]} \n"
          f"\n concave_evt: {x_R_events[3]} \n")

# the following is to see where the integration really stopped
# (why isn't it stopping at "x_end" is no other event is being triggered?
# is this something inherent from "solve_ivp" that we haven't figured out yet?)
print(f"we've integrated up to:"
      f"\n {x_R[-1]}")
