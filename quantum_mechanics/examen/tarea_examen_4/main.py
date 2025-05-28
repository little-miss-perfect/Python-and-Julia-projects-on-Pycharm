import numpy as np
from scipy.integrate import quad

# las constantes que igualamos a "1" por simplicidad
h_bar, m, omega = 1, 1, 1

# define la región de integración
x_max = np.sqrt(h_bar / (m * omega))

# la función de onda en la representación de posición
def phi_0(x):
    factor = (m * omega / (np.pi * h_bar)) ** 0.25
    return factor * np.exp(-(m * omega * x ** 2) / (2 * h_bar))

# la función de densidad de probabilidad
def density(x):
    return np.abs(phi_0(x))**2  # como la función de onda es un real, tomamos el valor absoluto

# usamos "quad" porque... me topé está función en mi servicio social y aparte deja "integrar hasta infinito"
integral, error = quad(density, x_max, np.inf)  # la integración en la región "|x| > x_max"
P = 2 * integral  # pero la probabilidad era la suma de esta misma integral, por eso multiplicamos por "2"
print(P)
