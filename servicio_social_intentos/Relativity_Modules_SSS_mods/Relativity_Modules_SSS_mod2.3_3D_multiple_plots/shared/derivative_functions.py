import numpy as np

class DerivativeFunctions:
    def __init__(self, f, f1, f2, f3, f32, rho, xrho, T):
        self.f    = f
        self.f1   = f1
        self.f2   = f2
        self.f3   = f3
        self.f32  = f32
        self.rho  = rho
        self.xrho = xrho
        self.T    = T

    # ----------------------------------------------------------------------
    # SCALAR VERSIONS: handle one x and one (n,m,R,R1,P,Ms,Mb) at a time.
    # These preserve your original "if x==0" etc. logic.
    # ----------------------------------------------------------------------

    def _scalar_n1(self, x, n, m, R, R1, P, Ms, Mb):
        if x == 0:
            return 0
        elif P > 0:
            return (
                n / (x * (2 * self.f1(R) + x * R1 * self.f2(R)))
            ) * (
                (x**2)*m*(self.f(R) - R*self.f1(R) + 2 * 8 * np.pi * P)
                + 2*(m - 1)*self.f1(R)
                - 4*x*R1*self.f2(R)
            )
        else:
            return (
                n / (x * (2 * self.f1(R) + x * R1 * self.f2(R)))
            ) * (
                (x**2)*m*(self.f(R) - R*self.f1(R))
                + 2*(m - 1)*self.f1(R)
                - 4*x*R1*self.f2(R)
            )

    def _scalar_m1(self, x, n, m, R, R1, P, Ms, Mb):
        if x == 0:
            return 0
        elif P > 0:
            return (
                m / (x * (2*self.f1(R) + x*R1*self.f2(R)))
            ) * (
                2*self.f1(R)*(1 - m)
                + 16*np.pi*m*(x**2)*self.rho
                + ((m*(x**2))/3)*(R*self.f1(R) + self.f(R) + 16*np.pi*self.T)
                + x*R1*(self.f2(R)/self.f1(R)) * (
                    ((m*(x**2))/3)*(2*R*self.f1(R) - self.f(R) + 8*np.pi*self.T)
                    - 8*np.pi*m*(x**2)*(-1*self.rho + P)
                    + 2*(1 - m)*self.f1(R)
                    + 2*x*R1*self.f2(R)
                )
            )
        else:
            return (
                m / (x * (2*self.f1(R) + x*R1*self.f2(R)))
            ) * (
                2*self.f1(R)*(1 - m)
                + ((m*(x**2))/3)*(R*self.f1(R) + self.f(R))
                + x*R1*(self.f2(R)/self.f1(R)) * (
                    ((m*(x**2))/3)*(2*R*self.f1(R) - self.f(R))
                    + 2*(1 - m)*self.f1(R)
                    + 2*x*R1*self.f2(R)
                )
            )

    def _scalar_DR(self, x, n, m, R, R1, P, Ms, Mb):
        if x == 0:
            return 0
        elif P > 0:
            return R1
        elif x <= 0.1 and P <= 0:
            # original logic: P=0, return R1
            return R1
        else:
            # original logic: P=0, return 0
            return 0

    def _scalar_R2(self, x, n, m, R, R1, P, Ms, Mb):
        if x == 0:
            return ((2*self.f(R) - self.f1(R)*R + 8*np.pi*self.T) / (9*self.f2(R)))
        elif P > 0:
            # same sub-logic as your code
            m1_val = (
                m / (x*(2*self.f1(R) + x*R1*self.f2(R)))
            ) * (
                2*self.f1(R)*(1 - m)
                + 16*np.pi*m*(x**2)*self.rho
                + ((m*(x**2))/3)*(R*self.f1(R) + self.f(R) + 16*np.pi*self.T)
                + x*R1*(self.f2(R)/self.f1(R)) * (
                    ((m*(x**2))/3)*(2*R*self.f1(R) - self.f(R) + 8*np.pi*self.T)
                    - 8*np.pi*m*(x**2)*(-1*self.rho + P)
                    + 2*(1 - m)*self.f1(R)
                    + 2*x*R1*self.f2(R)
                )
            )
            n1_val = (
                n / (x*(2*self.f1(R) + x*R1*self.f2(R)))
            ) * (
                (x**2)*m*(self.f(R) - R*self.f1(R) + 2*8*np.pi*P)
                + 2*(m - 1)*self.f1(R)
                - 4*x*R1*self.f2(R)
            )
            return (
                (m*(8*np.pi*self.T + 2*self.f(R) - self.f1(R)*R)) / (3*self.f2(R))
                - self.f32(R)*(R1**2)
                + m1_val*(R1/(2*m))
                - ((n1_val/(2*n)) + (2/x))*R1
            )
        elif x <= 0.1 and P <= 0:
            m1_val = (
                m / (x*(2*self.f1(R) + x*R1*self.f2(R)))
            ) * (
                2*self.f1(R)*(1 - m)
                + ((m*(x**2))/3)*(R*self.f1(R) + self.f(R))
                + x*R1*(self.f2(R)/self.f1(R)) * (
                    ((m*(x**2))/3)*(2*R*self.f1(R) - self.f(R))
                    + 2*(1 - m)*self.f1(R)
                    + 2*x*R1*self.f2(R)
                )
            )
            n1_val = (
                n / (x*(2*self.f1(R) + x*R1*self.f2(R)))
            ) * (
                (x**2)*m*(self.f(R) - R*self.f1(R))
                + 2*(m - 1)*self.f1(R)
                - 4*x*R1*self.f2(R)
            )
            return (
                (m*(2*self.f(R) - self.f1(R)*R)) / (3*self.f2(R))
                - self.f32(R)*(R1**2)
                + m1_val*(R1/(2*m))
                - ((n1_val/(2*n)) + (2/x))*R1
            )
        else:
            return 0

    def _scalar_DP(self, x, n, m, R, R1, P, Ms, Mb):
        if x == 0:
            return 0
        elif P > 0:
            n1_val = (
                n / (x*(2*self.f1(R) + x*R1*self.f2(R)))
            ) * (
                (x**2)*m*(self.f(R) - R*self.f1(R) + 2*8*np.pi*P)
                + 2*(m - 1)*self.f1(R)
                - 4*x*R1*self.f2(R)
            )
            return - (self.rho + P) * (n1_val/(2*n))
        else:
            return 0

    def _scalar_DMs(self, x, n, m, R, R1, P, Ms, Mb):
        if x == 0:
            return 0
        elif P > 0:
            return 4*np.pi*self.rho*(x**2)
        else:
            return 0

    def _scalar_DMb(self, x, n, m, R, R1, P, Ms, Mb):
        if x == 0:
            return 0
        elif P > 0:
            return 4*np.pi*self.rho*(x**2)*self.xrho
        else:
            return 0

    def _scalar_F(self, x, r):
        """
        Return the derivative for a single x, r.
        r = [n, m, R, R1, P, Ms, Mb].
        """
        n, m, R, R1, P, Ms, Mb = r
        out = np.zeros_like(r)
        out[0] = self._scalar_n1(x, n, m, R, R1, P, Ms, Mb)
        out[1] = self._scalar_m1(x, n, m, R, R1, P, Ms, Mb)
        out[2] = self._scalar_DR(x, n, m, R, R1, P, Ms, Mb)
        out[3] = self._scalar_R2(x, n, m, R, R1, P, Ms, Mb)
        out[4] = self._scalar_DP(x, n, m, R, R1, P, Ms, Mb)
        out[5] = self._scalar_DMs(x, n, m, R, R1, P, Ms, Mb)
        out[6] = self._scalar_DMb(x, n, m, R, R1, P, Ms, Mb)
        return out

    # ----------------------------------------------------------------------
    # WRAPPERS that handle scalar or array x.
    # These are the methods you pass to solve_ivp or solve_bvp.
    # ----------------------------------------------------------------------

    def F(self, x, r):
        """
        If solve_ivp calls F with a scalar x and a 1D array r, we evaluate _scalar_F directly.
        If solve_bvp calls F with an array x (shape (N,)) and 2D array r (shape (7, N)),
        we loop over each point in x.
        """
        # Check if x is scalar:
        if np.isscalar(x):
            # r should be shape (7,). Return shape (7,).
            return self._scalar_F(x, r)
        else:
            # x is array of shape (N,). r is (7, N).
            # We need to produce a (7, N) output.
            N = len(x)
            out = np.zeros_like(r)  # shape (7, N)
            for i in range(N):
                xi = x[i]
                ri = r[:, i]  # shape (7,)
                out[:, i] = self._scalar_F(xi, ri)
            return out

    def G(self, u, r):
        """
        For solve_bvp on [0,1], dr/du = G(u,r),
        where x = u/(1-u), dx/du = 1/(1-u)^2 => factor = (1-u)^(-2).

        We again handle scalar or array 'u'.
        """
        if np.isscalar(u):
            # scalar case
            x = u/(1-u)
            factor = 1./(1.-u)**2
            dF = self.F(x, r)      # shape (7,)
            return dF * factor     # shape (7,)
        else:
            # array case, shape (N,)
            N = len(u)
            out = np.zeros_like(r)  # shape (7, N)
            for i in range(N):
                ui = u[i]
                ri = r[:, i]        # shape (7,)
                xi = ui/(1-ui)
                factor_i = 1./(1.-ui)**2
                dF_i = self.F(xi, ri)   # shape (7,)
                out[:, i] = dF_i * factor_i
            return out


from scipy.optimize import brentq
from scipy.integrate import solve_ivp


class ShootingSolver:
    def __init__(self, F, base_r0, t_span, target,  # Add target parameter
                 method='DOP853', rtol=1e-6, atol=1e-9):
        self.F = F
        self.base_r0 = np.copy(base_r0)
        self.t_span = t_span
        self.method = method
        self.rtol = rtol
        self.atol = atol
        self.component = 2
        self.target = target  # Initialize target here

    def _residual(self, R0_guess):
        r0 = np.copy(self.base_r0)
        r0[self.component] = R0_guess
        sol = solve_ivp(
            fun=self.F,
            t_span=self.t_span,
            y0=r0,
            method=self.method,
            rtol=self.rtol,
            atol=self.atol
        )
        return sol.y[self.component, -1] - self.target  # Now safe

    def solve(self, bracket, maxiter=100):
        root, result = brentq(
            self._residual,
            bracket[0],
            bracket[1],
            maxiter=maxiter,
            full_output=True
        )
        if not result.converged:
            raise RuntimeError(f"Convergence failed: {result.flag}")
        return root


