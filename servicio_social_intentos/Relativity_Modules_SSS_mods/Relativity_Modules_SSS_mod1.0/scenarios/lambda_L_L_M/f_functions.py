from .variables import *


def f(R):
    return R - (lambda_staro * R_star) * (1 - (1 + (R / R_star) ** 2) ** (-beta))


def f1(R):

    R_tilde = R / R_star

    return 1 - 2 * lambda_staro * beta * R_tilde * (1 + R_tilde ** 2) ** (-beta - 1)


def f2(R):

    R_tilde = R / R_star

    return -2 * lambda_staro * beta / R_star * ((1 + R_tilde ** 2) ** (-beta - 2) * ((1 + R_tilde ** 2) + 2 * (-beta - 1) * R * R_tilde / R_star))


def f3(R):

    R_tilde = R / R_star

    return -(2 * lambda_staro * beta / R_star) * (-2 * (beta + 2) * R_tilde / R_star * (1 + R_tilde ** 2) ** (-beta - 3) * ((1 + R_tilde ** 2) + 2 * (-beta - 1) * R * R_tilde / R_star) + (1 + R_tilde ** 2) ** (-beta - 2) * -2 * (2 * beta + 1) * R / (R_star ** 2))


def f32(R):
    return f3(R) / f2(R)
