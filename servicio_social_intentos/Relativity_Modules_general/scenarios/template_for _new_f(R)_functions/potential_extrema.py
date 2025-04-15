from .vectorized_derivative import *

def dVdR(R):
    '''
    there should be certain values we use to plot correctly "R vs x" ("the Ricci scalar vs the position from the center of the star")
    :param R: the Ricci scalar
    :return: a function whose
    '''
    g1 = (1 / 3) * (2 * f(R) - f1(R) * R)  # as is in the paper
    g2 = -(1 / 3) * (f(R) + R * f1(R))  # as we think it might be if there's a mistake
    return g1  # for now, we'll leave this general result as is (in the paper)
