import numpy as np
from scipy.special import factorial, genlaguerre
from scipy.integrate import quad
import matplotlib.pyplot as plt

def R_nl(rho, n, l):

    x = 2 * rho / n
    factor = np.sqrt((2.0 / n)**3 * factorial(n - l - 1) / (2.0 * n * factorial(n + l)))
    L = genlaguerre(n - l - 1, 2*l + 1)(x)
    Rnl = factor * np.exp(-x / 2) * (x**l) * L

    return Rnl

# los parámetros de este problema ahora son: n=1, l=0, Z=1 (así lo definió en clase)
n = 1
l = 0

# en clase tomó "Z = 1" y en su código también toma "a0 = 1", así que tendríamos que aquí "rho = r"
rho = np.linspace(0, 10, 1000)  # en unidades de "a0"

# los valores para poder graficar
R10_vals = R_nl(rho, n, l)

# la densidad de probabilidad radial: |R_{1,0}(r)|^2 * r^2
densidad_de_probabilidad_radial = np.abs(R10_vals) ** 2 * rho ** 2

# y a graficar como en el problema anterior
plt.figure(dpi=150)
plt.plot(rho, densidad_de_probabilidad_radial, label=r"$|R_{1,0}(r)|^2\,r^2$")
plt.title("densidad de probabilidad radial para: $n=1, l=0$")
plt.xlabel(r"$r/a_0$")
plt.ylabel(r"$r^2\,|R_{1,0}(r)|^2$")
plt.legend()
plt.grid(True)
plt.show()

# para checar la normalización (como en el problema anterior)
def integrando_norm(r):

    R_val = R_nl(np.array([r]), n, l)[0]

    return (np.abs(R_val)**2) * (r**2)

normalization, error_norm = quad(integrando_norm, 0, np.inf)
print(f"lo que el profe tiene como 'verificar la normalización': {normalization:.12f} \n (error: {error_norm:.2e})")

# el valor esperado de "r" lo obtenemos mediante la función de densidad que ya tenemos:
# al integrar "r * [|R|^2 r^2]"
def integrand_r(r):

    R_val = R_nl(np.array([r]), n, l)[0]

    return (np.abs(R_val)**2) * (r**3)

esperanza_r, error_r = quad(integrand_r, 0, np.inf)
print(f"esperanza = {esperanza_r:.12f}  (error: {error_r:.2e})")

# para conocer el valor en metros, basta con multiplicar
# por "a0 = 5.29177210544e-11 m", como nos dijo asaf al final de la clase
a0_m = 5.29177210544e-11  # este valor lo agarré de la primera búsqueda en internet. pero lo pueden cambiar si gustan
esperanza_r_metros = esperanza_r * a0_m
print(f"<r> = {esperanza_r_metros:.3e} m")

# el radio con mayor densidad de probabilidad lo podemos encontrar tomando
idx_max = np.argmax(densidad_de_probabilidad_radial)  # que nos dará el índice donde hay un valor máximo en este array
r_mas_prob = rho[idx_max]  # y así obtenemos dicho valor
print(f"radio más probable: {r_mas_prob:.3f}")
print(f"radio más probable (en metros): {r_mas_prob * a0_m:.3e} m")  # análogo a como le hicimos antes
