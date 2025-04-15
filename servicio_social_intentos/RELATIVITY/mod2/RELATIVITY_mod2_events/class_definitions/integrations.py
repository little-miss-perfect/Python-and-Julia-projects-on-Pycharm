from scipy.integrate import solve_ivp
import timeit

class ODEIntegrator:
    """
    By default, we integrate with "LSODA", because in principle, our problem might be stiff.
    the only non-default parameters are "F, r0".
    """
    def __init__(self, F, r0, x_start=0, x_end=8, rtol=1e-9, atol=1e-12, method='LSODA', events=None, t_eval=None):
        """
        Initialize the integrator with the ODE system function, initial values, and parameters for the solver.

        :param F: ODE system function, should have signature F(t, y) -> array_like
        :param r0: Initial values for the dependent variables (array_like)
        :param x_start: Starting point of the independent variable (float)
        :param x_end: Endpoint of the independent variable (float)
        :param rtol: Relative tolerance for the solver (float)
        :param atol: Absolute tolerance for the solver (float or array_like)
        :param method: Integration method (e.g., 'LSODA', 'RK45', etc.)
        :param events: A function or list of functions that defines event conditions.
                       Each event function has signature event(t, y), returns float.
                       An event is detected when this float crosses zero.
        :param t_eval: Times at which to store the computed solution. If None (default), the solver
                       chooses steps automatically. If an array, solver reports the solution at those times.
        """
        self.F = F
        self.r0 = r0
        self.t_start = x_start
        self.t_end = x_end
        self.rtol = rtol
        self.atol = atol
        self.method = method
        self.events = events
        self.t_eval = t_eval  # this is put in case we'd specifically want to get an evenly spaced interval or any subset of the set defined by the interval of allowed "x" values

        self.x = None  # Placeholder for independent variable array
        self.r = None  # Placeholder for dependent variable array
        self.execution_time = None  # Placeholder for execution time

        # If we have events, we'll store the times and states at event occurrences
        self.t_events = None
        self.y_events = None

    def integrate(self):
        """
        Perform the integration and store the result in the object.
        """
        start_int = timeit.default_timer()

        sol = solve_ivp(
            fun=self.F,
            t_span=(self.t_start, self.t_end),
            y0=self.r0,
            method=self.method,
            rtol=self.rtol,
            atol=self.atol,
            events=self.events,
            t_eval=self.t_eval
        )

        # Extract solution
        self.x = sol.t
        self.r = sol.y

        # If events occurred, store the event times and states
        if self.events is not None:
            self.t_events = sol.t_events
            self.y_events = sol.y_events

        stop_int = timeit.default_timer()
        self.execution_time = stop_int - start_int

    def get_solution(self):
        """
        Return the independent and dependent variables after integration.
        :return: (x, r) tuple where x is the independent variable array and r is the dependent variable array
        """
        return self.x, self.r

    def get_execution_time(self):
        """
        Return the execution time for the integration.
        :return: Execution time in seconds
        """
        return self.execution_time

    def get_events(self):
        """
        Return the event times and states if events were used.
        :return: (t_events, y_events) if events exist, else (None, None)

        self.t_events is a list (or array) of arrays, one for each event function you passed in. Each array in t_events contains the time values at which that particular event triggered.
        self.y_events is similarly structured and provides the state of the solution at those event times.
        """
        return self.t_events, self.y_events
