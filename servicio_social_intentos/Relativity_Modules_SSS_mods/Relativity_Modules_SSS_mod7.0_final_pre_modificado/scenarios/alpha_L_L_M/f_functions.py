from .variables import *


# how can we modify these outputs in case "-R_star < R"?
def f(R):
    return R - alpha_mir * R_star * np.log(1 + (R / R_star))  # the problem with this function, is that we need to only consider values of "R" such that "-R_star < R" (assuming that "0 < R_star")

def f1(R):
    return 1 - alpha_mir * ((1 + (R / R_star)) ** (-1))

def f2(R):
    return (alpha_mir / R_star) * ((1 + (R / R_star)) ** (-2))

def f3(R):
    return -2 * (alpha_mir / (R_star ** 2)) * ((1 + (R / R_star)) ** (-3))

def f32(R):
    return f3(R) / f2(R)
