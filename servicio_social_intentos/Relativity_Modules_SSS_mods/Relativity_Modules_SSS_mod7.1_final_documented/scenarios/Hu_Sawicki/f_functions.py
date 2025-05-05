from .variables import *


def f(R):
    return np.add(R, np.negative(np.divide(np.multiply(c1, np.multiply(np.power(mHS, 2), np.power(np.divide(R, np.power(
        mHS, 2)), nHS))), np.add(1, np.multiply(c2, np.power(np.divide(R, np.power(mHS, 2)), nHS))))))


def f1(R):
    return np.add(1, np.negative(np.divide(np.multiply(c1, np.multiply(nHS, np.power(np.divide(R, np.power(mHS, 2)),
                                                                                     np.add(-1, nHS)))), np.power(np.add(1, np.multiply(c2, np.power(np.divide(R, np.power(mHS, 2)), nHS))), 2))))


def f2(R):
    return np.divide(np.multiply(np.multiply(np.multiply(c1, np.power(mHS,  2)), np.multiply(nHS, np.power(np.divide(R,
                                                                                                                     np.power(mHS, 2)), nHS))), np.add(np.add(1, np.multiply(c2, np.power(np.divide(R, np.power(mHS, 2)), nHS))), np.multiply(nHS, np.add(-1, np.multiply(c2, np.power(np.divide(R, np.power(mHS, 2)), nHS)))))), np.multiply(np.power(R, 2), np.power(np.add(1, np.multiply(c2, np.power(np.divide(R, np.power(mHS, 2)), nHS))), 3)))


def f3(R):
    return np.divide(np.negative(np.multiply(np.multiply(c1, np.multiply(np.power(mHS, 2), nHS)), np.multiply(np.power(
        np.divide(R, np.power(mHS, 2)), nHS), np.add(np.multiply(2, np.power(np.add(1, np.multiply(c2, np.power(
            np.divide(R, np.power(mHS, 2)), nHS))), 2)), np.add(np.multiply(np.multiply(3, nHS), np.add(-1, np.multiply(
                np.power(c2, 2), np.power(np.divide(R, np.power(mHS, 2)), np.multiply(2, nHS))))), np.multiply(np.power(
                    nHS, 2), np.add(1, np.add(np.negative(np.multiply(np.multiply(4, c2), np.power(np.divide(
                        R, np.power(mHS, 2)), nHS))), np.multiply(np.power(c2, 2), np.power(np.divide(R, np.power(
                            mHS, 2)), np.multiply(2, nHS))))))))))), np.multiply(np.power(R, 3), np.power(np.add(1, np.multiply(c2, np.power(np.divide(R, np.power(mHS, 2)), nHS))), 4)))


def f32(R):
    return np.divide(f3(R), f2(R))
