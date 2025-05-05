import numpy as np
import pandas as pd
import os

# parameters for this "f(R)" function
alpha_mir = 1.2
R_star = 1


# the absolute path to the directory containing this file is
this_dir = os.path.dirname(__file__)

# the path to the data files will be defined by
data_cond_path = os.path.join(this_dir, "data", "init_cond.dat")
data_gas_path  = os.path.join(this_dir, "data", "init_gas.dat")

data_cond = pd.read_csv(data_cond_path, sep=",")
data_gas  = pd.read_csv(data_gas_path,  sep=",")


# print(data_cond)
# print(data_gas)
# print(type(data_gas.values[1][0]))
# print(data_gas.values[1][0])

# it works, now lets assign variables from "data_cond"

x0 = data_cond.values[0][0]

n0 = data_cond.values[1][0]

n10 = data_cond.values[2][0]

m0 = data_cond.values[3][0]

m10 = data_cond.values[4][0]

R0 = data_cond.values[5][0]  # this is the value we want to adjust as the program runs (when it runs correctly)

DR0 = data_cond.values[6][0]

Ms0 = data_cond.values[7][0]

delta = data_cond.values[8][0]

# assign variables from "data_gas"

rho = data_gas.values[0][0]

nHS = data_gas.values[1][0]

mHS = data_gas.values[2][0]  # the article says that after the square of this value, "R" values input into what we'll define as "f2(R)", are positive.

f1hoy = data_gas.values[3][0]

# TODO 3: define the other ("non-imported") variables used throughout the program
c2 = np.divide(np.multiply(-1, nHS * 19 * np.power(41, -1 * nHS - 1)), f1hoy)

c1 = np.multiply(19, c2)

P0 = np.multiply(0.1, rho)

Mb0 = 1.66e-27  # is this the initial baryonic mass?

G = 1

c = 1

M_sol = 1  # en el archivo original sale como "M_sol  ==> 1.0"

rho_nuc = 1.66e17

rho_c = np.divide(np.power(c, 8), np.multiply(np.power(M_sol, 2), np.power(G, 3)))

xrho = np.divide(np.multiply(rho_nuc, np.power(c, 2)), rho_c)

Po = np.multiply(0.1, rho)

T = np.add(np.multiply(-1, rho), np.multiply(3, Po))

# TODO 3.1:  the initial conditions will be stored in
r0 = np.array([n0, m0, R0, DR0, P0, Ms0, Mb0], float)

# other variables defined to compare the numerical method with an analytic solution for "R"

f0 = R0 - (c1 * mHS ** 2 * (R0 / mHS ** 2) ** nHS) / (1 + c2 * (R0 / mHS ** 2) ** nHS)

f10 = 1 - (c1 * nHS * (R0 / mHS ** 2) ** (-1 + nHS)) / ((1 + c2 * (R0 / mHS ** 2) ** nHS) ** 2)

f20 = (c1 * mHS ** 2 * nHS * (R0 / mHS ** 2) ** nHS * (
            1 + c2 * (R0 / mHS ** 2) ** nHS + nHS * (-1 + c2 * (R0 / mHS ** 2) ** nHS))) / (
                  R0 ** 2 * (1 + c2 * (R0 / mHS ** 2) ** nHS) ** 3)

f30 = -(c1 * mHS ** 2 * nHS * (R0 / mHS ** 2) ** nHS * (2 * (1 + c2 * (R0 / mHS ** 2) ** nHS) ** 2 + 3 * nHS * (
            -1 + c2 ** 2 * (R0 / mHS ** 2) ** (2 * nHS)) + nHS ** 2 * (1 - 4 * c2 * (
            R0 / mHS ** 2) ** nHS + c2 ** 2 * (R0 / mHS ** 2) ** (2 * nHS)))) / (
                  R0 ** 3 * (1 + c2 * (R0 / mHS ** 2) ** nHS) ** 4)
