# TODO 1: import/install modules
import timeit
import matplotlib.pyplot as plt
from vectorized_derivative import *
from integrators import *

# some of these modules already include other modules used like "numpy" and "pandas";
# so it would be redundant to import them again.

# TODO 2:  import the data from the ".dat" files, and define the variables in the files
# they've been imported from our module "variables"


# TODO 3: define the other ("non-imported") variables used throughout the program
# they've been imported from our module "variables"


# TODO 4: define the "f(R)" functions
# they've been imported from our module "f_functions"


# TODO 5: define the "derivative" functions
# they've been imported from our module "derivative_functions"


# TODO 6: define the "vectorized derivative" of the system of equations ("F")
# they've been imported from our module "vectorized_derivative"


# TODO 7: define an "integrator" class for the a "vectorized" problem,
#                 (such that you can choose from multiple "integrators"? maybe after just one of them works out)
#                 preferably, make one that handles a variable "step size".
# it's been imported from our module "integrators"


print("this is a test.")

a = 0 #desde un radio igual a cero (el centro de la estrella)? o casi cero como "1e-9"
b = 1 #tomaremos valores hasta este radio; como lo tiene en su código original?
N = 1e6 #number of steps #el código no sirve si el paso es de "1e5" y se tarda si es mayor que "1e6"
h = (b-a) / N #the step size

print('el paso es de un tamaño constante de', h)

x_points = np.arange(a, b, h) #la variable independiente "x" es "el radio" que se toma

#las variables que necesitamos saber son dadas por sus primeras derivadas como: n1, m1, DR, R2, DP, DMs, DMb. son estas las que usa el método

n_points = []

m_points = []

R_points = []

R1_points = []

P_points = []

Ms_points = []

Mb_points = []

r = r0

start = timeit.default_timer() #vamos a comenzar a tomar el tiempo que tarda en correr este RK_4



for x in x_points:


  n_points.append(r[0])

  m_points.append(r[1])

  R_points.append(r[2])

  R1_points.append(r[3])

  P_points.append(r[4])

  Ms_points.append(r[5])

  Mb_points.append(r[6])


  # all values of "k" are a vector quantity (because "f" is itself a vector quantity)

  k1 = h * F(x, r)

  k2 = h * F(x + 0.5 * h, r + 0.5 * k1)

  k3 = h * F(x + 0.5 * h, r + 0.5 * k2)

  k4 = h * F(x + h, r + k3)



  r += (1/6) * (k1 + 2 * k2 + 2 * k3 + k4)



stop = timeit.default_timer() #terminamos de tomar/medir el tiempo

execution_time = stop - start #vemos cuánto tardó el programa

print('el programa tarda', execution_time, 'segundos en compilar')
print('tarda', execution_time/60, 'minutos)')

plt.plot(x_points, R_points, 'c.', )
plt.xscale("log")
plt.show()

# con "N=1e6" tarda como "26 min."
# y las funciones que definimos usando numpy sí dan el mismo resultado que cuando sólo usamos los símbolos de siempre
