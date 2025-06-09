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

rho = np.linspace(0, 60, 1000)

n = 4

plt.figure(dpi=150)

for l in range(n):  # justo agarra los valores: 0, 1, 2, 3

    Rnl_vals = R_nl(rho, n, l)  # la función de onda

    densidad_de_probabilidad_radial = np.abs(Rnl_vals) ** 2 * rho ** 2  # la densidad de probabilidad radial es: |R_{n,l}(rho)|^2 * rho^2

    plt.plot(rho, densidad_de_probabilidad_radial, label=f"l = {l}")  # y grafiquemos cada una


    # para checar que la normalización esté bien, mejor definamos esta función
    def integrand(r):
        R_val = R_nl(np.array([r]), n, l)[0]
        return (np.abs(R_val) ** 2) * (r ** 2)

    # para después integrarla
    integral_quad, error_estimate = quad(integrand, 0, np.inf)

    print(f"lo que el profe tiene como 'verificar la normalización' de la integral de '|R|^2 rho^2 drho' dado '(n={n}, l={l})':"
          f"\n {integral_quad:.16f}"
          f"\n con un error aproximado de: {error_estimate:.2e}")


plt.title(f"densidad de probabilidad radial '|Rₙ,ₗ(ρ)|² ρ²' para 'n = {n}'")
plt.xlabel(r"$\rho$")
plt.ylabel(r"$|R_{n,l}(\rho)|^2\,\rho^2$")
plt.legend()
plt.grid(True)
plt.show()
