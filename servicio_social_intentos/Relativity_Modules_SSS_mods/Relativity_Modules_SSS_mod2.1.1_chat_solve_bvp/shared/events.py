import numpy as np


# TODO e.1: some constants
threshold_big = 1e6  # used for 'big divergence' event ("1e3" generally works pretty good). but there's a problem:
# when trying "R0= 9", if we keep the threshold at "1e3", the integrator won't work.
# but if we keep it at "1e7", then it'll plot without a problem.


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
# # maybe use this next block of code in the "main.py" file
# nan_inf_evt = nan_inf_event(F)
# div_evt = divergence_event(F, big_threshold=threshold_big)
# concave_evt_DU = concave_event_DU(F)
# concave_evt_UD = concave_event_UD(F)

# all_events = [nan_inf_evt, div_evt, concave_evt_DU, concave_evt_UD]

all_events = [nan_inf_event, divergence_event, concave_event_DU, concave_event_UD]

