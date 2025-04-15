import numpy as np
import matplotlib.pyplot as plt

def plot_reg_func(g, ind_var='ind_var', min_val=-1e2, max_val=1e2, num_points=200):
    # Create a range of values where we'll evaluate "g"
    values = np.linspace(min_val, max_val, num_points)

    # Evaluate "g" for all chosen "values"
    g_values = [g(i) for i in values]

    # Plot "g({ind_var})" vs "{ind_var}"
    plt.figure(figsize=(8, 5))
    plt.plot(values, g_values, label=f'{g.__name__}({ind_var})')
    plt.xlabel(f'{ind_var}')
    plt.ylabel(f'{g.__name__}({ind_var})')
    plt.title(f'Plot of: {g.__name__}({ind_var})')
    plt.grid(True)
    plt.legend()
    plt.show()
