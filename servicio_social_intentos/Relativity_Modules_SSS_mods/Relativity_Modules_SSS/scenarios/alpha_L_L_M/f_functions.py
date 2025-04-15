from .variables import *


def f(R):
    return R - alpha * R_star * np.log(1 + (R / R_star))

def f1(R):
    return 1 - alpha * ((1 + (R / R_star))**(-1))

def f2(R):
    return (alpha / R_star) * ((1 + (R / R_star))**(-2))

def f3(R):
    return -2 * (alpha / (R_star ** 2)) * ((1 + (R / R_star))**(-3))
