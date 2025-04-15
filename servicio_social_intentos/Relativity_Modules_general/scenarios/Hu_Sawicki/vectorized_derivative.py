from .derivative_functions import *


def F(x, r):  # the independent variable is "x", the dependent variable is the vector "r"

    n = r[0]
    m = r[1]
    R = r[2]
    R1 = r[3]
    P = r[4]
    Ms = r[5]
    Mb = r[6]

    F = np.zeros(len(r))

    F[0] = n1(x, n, m, R, R1, P, Ms, Mb)
    F[1] = m1(x, n, m, R, R1, P, Ms, Mb)
    F[2] = DR(x, n, m, R, R1, P, Ms, Mb)
    F[3] = R2(x, n, m, R, R1, P, Ms, Mb)
    F[4] = DP(x, n, m, R, R1, P, Ms, Mb)
    F[5] = DMs(x, n, m, R, R1, P, Ms, Mb)
    F[6] = DMb(x, n, m, R, R1, P, Ms, Mb)

    return F  # because of how we defined "F", this will return an array
