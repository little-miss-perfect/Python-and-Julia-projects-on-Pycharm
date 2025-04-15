from .f_functions import *


def n1(x, n, m, R, R1, P, Ms, Mb):
    fR = f(R)
    f1R = f1(R)
    f2R = f2(R)

    if x == 0:
        return 0  # as is written in the paper (for the general case; the same happens to "m1(x=0)")

    elif P > 0:
        return np.multiply(np.divide(n, np.multiply(x, np.add(np.multiply(2, f1R), np.multiply(x, np.multiply(R1, f2R))))),
                           np.add(np.multiply(np.multiply(np.power(x, 2), m), np.add(fR, np.add(np.negative(np.multiply(R, f1R)), np.multiply(2, np.multiply(8, np.multiply(np.pi, P)))))), np.add(np.multiply(np.multiply(2, np.add(m, -1)), f1R), np.negative(np.multiply(4, np.multiply(x, np.multiply(R1, f2R)))))))

    else:
        return np.multiply(np.divide(n, np.multiply(x, np.add(np.multiply(2, f1R), np.multiply(x, np.multiply(R1, f2R))))),
                           np.add(np.multiply(np.power(x, 2), np.multiply(m, np.add(fR, np.negative(np.multiply(R, f1R))))), np.add(np.multiply(2, np.multiply(np.add(m, -1), f1R)), np.negative(np.multiply(4, np.multiply(x, np.multiply(R1, f2R)))))))


def m1(x, n, m, R, R1, P, Ms, Mb):
    fR = f(R)
    f1R = f1(R)
    f2R = f2(R)

    if x == 0:
        return 0

    elif P > 0:
        return np.multiply(np.divide(m, np.multiply(x, np.add(np.multiply(2, f1R), np.multiply(x, np.multiply(R1, f2R))))),
                           np.add(np.multiply(np.multiply(2, f1R), np.add(1, np.negative(m))), np.add(np.multiply(
                               np.multiply(np.multiply(16, np.pi), m), np.multiply(np.power(x, 2), rho)), np.add(
                               np.multiply(np.divide(np.multiply(m, np.power(x, 2)), 3), np.add(np.add(
                                   np.multiply(R, f1R), fR), np.multiply(np.multiply(16, np.pi), T))), np.multiply(
                                   np.multiply(np.multiply(x, R1), np.divide(f2R, f1R)), np.add(np.divide(np.multiply(
                                       m, np.power(x, 2)), np.multiply(3, np.add(np.multiply(np.multiply(2, R),  f1R),
                                                                                 np.add(np.negative(fR), np.multiply(
                                                                                     np.multiply(8, np.pi), T))))),
                                       np.add(
                                       np.multiply(np.negative(np.multiply(np.multiply(np.multiply(8, np.pi), m),
                                                                           np.power(x, 2))), np.add(np.negative(rho), P)), np.add(np.multiply(
                                           np.multiply(2, np.add(1, np.negative(m))), f1R), np.multiply(np.multiply(2, x), np.multiply(R1, f2R))))))))))

    else:
        return np.multiply(np.divide(m, np.multiply(x, np.add(np.multiply(2, f1R), np.multiply(x, np.multiply(R1, f2R))))),
                           np.add(np.add(np.multiply(np.multiply(2, f1R), np.add(1, np.negative(m))), np.divide(np.multiply(
                               m, np.power(x, 2)), np.multiply(3, np.add(np.multiply(R, f1R), fR)))), np.multiply(np.multiply(
                               np.multiply(x, R1), np.divide(f2R, f1R)), np.add(np.divide(np.multiply(m, np.power(x, 2)), np.multiply(
                               3, np.add(np.multiply(np.multiply(2, R), f1R), np.negative(fR)))), np.add(np.multiply(np.multiply(
                               2, np.add(1, np.negative(m))), f1R), np.multiply(np.multiply(2, x), np.multiply(R1, f2R)))))))


def DR(x, n, m, R, R1, P, Ms, Mb):
    if x == 0:
        return 0

    elif P > 0:
        return R1

    elif x <= 0.1 and P <= 0:  # por qué aquí es "0.1" y no "0"?
        P = 0
        DR = R1
        return DR

    else:
        P = 0
        DR = 0
        return DR


def R2(x, n, m, R, R1, P, Ms, Mb):
    fR = f(R)
    f1R = f1(R)
    f2R = f2(R)
    f32R = f32(R)

    if x == 0:
        m1 = 0
        n1 = 0
        DR = 0
        R2 = np.divide(np.add(np.add(np.multiply(2, fR), np.negative(np.multiply(f1R, R))), np.multiply(np.multiply(8, np.pi), T)),
                       np.multiply(9, f2R))

        return R2

    elif P > 0:
        m1 = np.multiply(np.divide(m, np.multiply(x, (np.multiply(2, f1R) + np.multiply(x, np.multiply(R1, f2R))))),
                         np.add(np.add(np.multiply(np.multiply(2, f1R),  np.add(1, np.negative(m))),
                                       np.multiply(np.multiply(np.multiply(16, np.pi), m), np.power(np.power(x, 2), rho))),
                                np.add(np.multiply(np.multiply(m, np.divide(np.power(x, 2), 3)), np.add(np.add(
                                    np.multiply(R, f1R), fR), np.multiply(np.multiply(16, np.pi), T))), np.multiply(np.multiply(
                                    x, np.multiply(R1, np.divide(f2R, f1R))), np.add(np.add(np.add(np.divide(np.multiply(
                                    m, np.power(x, 2)), np.multiply(3, np.add(np.add(np.multiply(np.multiply(2, R), f1R), np.negative(fR)),
                                                                              np.multiply(np.multiply(8, np.pi), T)))), np.multiply(np.negative(np.multiply(np.multiply(np.multiply(
                                    8, np.pi), m), np.power(x, 2))), np.add(np.negative(rho), P))), np.multiply(np.multiply(2, np.add(1, np.negative(m))), f1R)),
                                    np.multiply(np.multiply(2, x), np.multiply(R1, f2R)))))))
        n1 = np.multiply(np.divide(n, np.multiply(x, np.add(np.multiply(2, f1R), np.multiply(x , np.multiply(R1, f2R))))),
                         np.add(np.multiply(np.multiply(np.power(x, 2), m), np.add(fR, np.add(np.negative(np.multiply(R, f1R)), np.multiply(
                             2, np.multiply(8, np.multiply(np.pi, P)))))), np.add(np.multiply(np.multiply(2, np.add(m, -1)), f1R),
                                                                                  np.negative(np.multiply(np.multiply(4, x), np.multiply(R1, f2R))))))
        DR = R1
        R2 = np.add(np.divide(np.multiply(m, np.add(np.multiply(np.multiply(8, np.pi), T), np.add(np.multiply(2, fR),
                                                                                                  np.negative(np.multiply(f1R, R))))), np.multiply(3, f2R)), np.add(np.negative(f32R * np.power(R1, 2)),
                                                                                                                                                                    np.divide(np.multiply(m1, R1), np.add(np.multiply(2, m),
                                                                                                                                                                                                          np.negative(np.multiply(np.add(np.divide(n1,
                                                                                                                                                                                                                                                   np.multiply(2, n)),
                                                                                                                                                                                                                                         np.divide(2, x)), R1))))))
        return R2

    elif x <= 0.1 and P <= 0:
        m1 = np.multiply(np.divide(m, np.multiply(x, np.add(np.multiply(2, f1R), np.multiply(x, np.multiply(R1, f2R))))),
                         np.add(np.add(np.multiply(np.multiply(2, f1R), np.add(1, np.negative(m))), np.divide(
                             np.multiply(m, np.power(x, 2)), np.multiply(3, np.add(np.multiply(R, f1R), fR)))),
                                                np.multiply(np.multiply(x, np.multiply(R1, np.divide(f2R, f1R))), np.add(np.divide(np.multiply(m, np.power(x, 2)), np.multiply(3, np.add(np.multiply(np.multiply(2, R), f1R), np.negative(fR)))), np.add(np.multiply(np.multiply(2, np.add(1, np.negative(m))), f1R), np.multiply(np.multiply(2, x), np.multiply(R1, f2R)))))))
        n1 = np.multiply(np.divide(n, np.multiply(x, np.add(np.multiply(2, f1R), np.multiply(x, np.multiply(R1, f2R))))),
                         np.add(np.multiply(np.multiply(np.power(x, 2), m), np.add(fR, np.negative(np.multiply(R, f1R)))),
                                np.add(np.multiply(np.multiply(2, np.add(m, -1)), f1R), np.negative(np.multiply(np.multiply(4, x), np.multiply(R1, f2R))))))
        DR = R1
        R2 = np.add(np.divide(np.multiply(m, np.add(np.multiply(2, fR), np.negative(np.multiply(f1R, R)))),
                              np.multiply(3, f2R)), np.add(np.negative(np.multiply(f32R, np.power(R1, 2))), np.add(np.multiply(m1,
                                                                                                                               np.divide(R1, np.multiply(2, m))), np.negative(np.multiply(np.add(
            np.divide(n1, np.multiply(2, n)), np.divide(2, x)), R1)))))
        return R2

    else:
        R2 = 0
        return R2


def DP(x, n, m, R, R1, P, Ms, Mb):
    fR = f(R)
    f1R = f1(R)
    f2R = f2(R)

    if x == 0:
        DP = 0
        return DP

    elif P > 0:
        n1 = np.multiply(np.divide(n, np.multiply(x, np.add(np.multiply(2, f1R), np.multiply(x, np.multiply(R1, f2R))))), np.add(np.multiply(np.multiply(np.power(x, 2), m), np.add(np.add(fR, np.negative(np.multiply(R, f1R))), np.multiply(2, np.multiply(8, np.multiply(np.pi, P))))), np.add(np.multiply(np.multiply(2, np.add(m, -1)), f1R), np.negative(np.multiply(4, np.multiply(x, np.multiply(R1, f2R)))))))
        DP = np.negative(np.multiply(np.add(rho, P), np.divide(n1, np.multiply(2, n))))
        return DP

    else:
        DP = 0
        return DP


def DMs(x, n, m, R, R1, P, Ms, Mb):
    if x == 0:
        DMs = 0
        return DMs

    elif P > 0:
        DMs = np.multiply(np.multiply(4, np.pi), np.multiply(rho, np.power(x, 2)))
        return DMs

    else:
        DMs = 0
        return DMs


def DMb(x, n, m, R, R1, P, Ms, Mb):
    if x == 0:
        DMb = 0
        return DMb

    elif P > 0:
        DMb = np.multiply(np.multiply(4, np.pi), np.multiply(rho, np.multiply(np.power(x, 2), xrho)))
        return DMb

    else:
        DMb = 0
        return DMb
