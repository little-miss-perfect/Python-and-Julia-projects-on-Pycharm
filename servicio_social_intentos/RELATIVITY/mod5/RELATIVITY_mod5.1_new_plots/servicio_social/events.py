import numpy as np

from vectorized_derivative import *
from class_definitions.integrations import *
from scipy.optimize import fsolve


# TODO e.1: some constants
threshold_big = 1e6  # used for 'big divergence' event ("1e3" generally works pretty good). but there's a problem:
# when trying "R0= 9", if we keep the threshold at "1e3", the integrator won't work.
# but if we keep it at "1e7", then it'll plot without a problem.

# TODO e.2: constants (for the loop)
R0_start = 9  # this is where we start searching for values of "R0" (the left/lower bound of the interval we're searching in)
R0_increment = 1  # the increment to the next value of "R0" in the interval we're searching in
quantity = 2  # amount of points ("R0" values) in the list we'd be searching
R0_end = R0_start + quantity * R0_increment


# TODO e.3: "R0" range (for the loop)
R0_a = np.arange(start=R0_start, stop=R0_end, step=R0_increment)
R0_b = np.array([0])  # "annoying" values to skip
allowed_R0 = np.setdiff1d(R0_a, R0_b)


# TODO e.4: event functions
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


def concave_event_DU(F):
    def event(t, y):
        drdt = F(t, y)
        R2 = drdt[3]
        return R2 - 1e-12  # we're now looking for a value "close to" (but not) zero
    event.terminal = False
    event.direction = 1  # negative to positive crossing
    return event


def concave_event_UD(F):
    def event(t, y):
        drdt = F(t, y)
        R2 = drdt[3]
        return R2 - 1e-12  # we're now looking for a value "close to" (but not) zero
    event.terminal = False
    event.direction = -1  # positive to negative crossing
    return event


# TODO e.5: the events used
nan_inf_evt = nan_inf_event(F)
div_evt = divergence_event(F, big_threshold=threshold_big)
concave_evt_DU = concave_event_DU(F)
concave_evt_UD = concave_event_UD(F)

all_events = [nan_inf_evt, div_evt, concave_evt_DU, concave_evt_UD]


# TODO e.6: end of integration
x_end = 2e1


# TODO e.7: integration used
solve_int = ODEIntegrator(
    F=F,
    r0=r0,
    x_start=0,
    x_end=x_end,
    events=all_events,
    method='DOP853',  # DOP853, LSODA, BDF
    # or whichever method works best (remember that our problem is stiff at some parts of the integration)
    max_step=np.inf
)


# TODO e.8: root finding for the minimum of the potential

def G(R):  # we've defined this as is defined by the article. this is a generalization of minimizing the potential which is a function of the curvature given by "R"
    return np.add(np.multiply(2, f(R)), np.negative(np.multiply(f1(R), R)))
