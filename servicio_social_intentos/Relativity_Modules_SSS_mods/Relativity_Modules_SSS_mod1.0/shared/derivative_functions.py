import numpy as np


class DerivativeFunctions:

    # first, we initialize our variables/functions
    def __init__(self, f, f1, f2, f3, f32, rho, xrho, T):
        self.f    = f
        self.f1   = f1
        self.f2   = f2
        self.f3   = f3
        self.f32  = f32
        self.rho  = rho
        self.T    = T
        self.xrho = xrho

    # then we construct each component of the final vector we'll use
    def n1(self, x, n, m, R, R1, P, Ms, Mb):
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

    def m1(self, x, n, m, R, R1, P, Ms, Mb):
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

    def DR(self, x, n, m, R, R1, P, Ms, Mb):
        if x == 0:
            return 0
        elif P > 0:
            return R1
        elif x <= 0.1 and P <= 0:
            P = 0
            return R1
        else:
            P = 0
            return 0

    def R2(self, x, n, m, R, R1, P, Ms, Mb):
        if x == 0:
            return ((2*self.f(R) - self.f1(R)*R + 8*np.pi*self.T) / (9*self.f2(R)))
        elif P > 0:
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

    def DP(self, x, n, m, R, R1, P, Ms, Mb):
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

    def DMs(self, x, n, m, R, R1, P, Ms, Mb):
        if x == 0:
            return 0
        elif P > 0:
            return 4*np.pi*self.rho*(x**2)
        else:
            return 0

    def DMb(self, x, n, m, R, R1, P, Ms, Mb):
        if x == 0:
            return 0
        elif P > 0:
            return 4*np.pi*self.rho*(x**2)*self.xrho
        else:
            return 0

    # and we can finally construct the vectorized derivative
    def F(self, x, r):
        n = r[0]
        m = r[1]
        R = r[2]
        R1 = r[3]
        P = r[4]
        Ms = r[5]
        Mb = r[6]

        F = np.zeros(len(r))

        F[0] = self.n1(x, n, m, R, R1, P, Ms, Mb)
        F[1] = self.m1(x, n, m, R, R1, P, Ms, Mb)
        F[2] = self.DR(x, n, m, R, R1, P, Ms, Mb)
        F[3] = self.R2(x, n, m, R, R1, P, Ms, Mb)
        F[4] = self.DP(x, n, m, R, R1, P, Ms, Mb)
        F[5] = self.DMs(x, n, m, R, R1, P, Ms, Mb)
        F[6] = self.DMb(x, n, m, R, R1, P, Ms, Mb)

        return F

    # let's write a new method for solving over an infinite interval
    def G(self, u, r):
        """
        For solve_bvp, we solve dr/du = G(u, r)
        where x = u / (1 - u), and dx/du = 1 / (1-u)^2.
        So G(u, r) = (1 - u)^(-2) * F(x, r).
        """
        x = u / (1 - u)
        factor = (1 - u) ** (-2)
        return factor * self.F(x, r)
