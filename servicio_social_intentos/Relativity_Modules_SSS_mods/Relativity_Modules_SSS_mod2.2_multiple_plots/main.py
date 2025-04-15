import importlib
import timeit
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from shared.plots import MultiSolutionRPlotter

# ---------------------------------------------------------------------
# Import your scenario and derivative functions.
# Adjust these paths to match your project structure.
# ---------------------------------------------------------------------
from shared.derivative_functions import DerivativeFunctions
from shared.scenario_data import Scenario

# Map your scenarios and choose one:
scenarios_map = {
    "Hu_Sawicki": "scenarios.Hu_Sawicki.f_functions",
    "alpha_L_L_M": "scenarios.alpha_L_L_M.f_functions",
    "lambda_L_L_M": "scenarios.lambda_L_L_M.f_functions",
}
chosen_scenario = "lambda_L_L_M"
scenario_mod = importlib.import_module(scenarios_map[chosen_scenario])
scene = Scenario(
    r0=scenario_mod.r0,
    R0=scenario_mod.R0,
    mHS=scenario_mod.mHS,
    rho=scenario_mod.rho,
    xrho=scenario_mod.xrho,
    T=scenario_mod.T,
    f=scenario_mod.f,
    f1=scenario_mod.f1,
    f2=scenario_mod.f2,
    f3=scenario_mod.f3,
    f32=scenario_mod.f32
)

# Set up the derivative functions and get F (the ODE system function)
d_f = DerivativeFunctions(scene.f, scene.f1, scene.f2, scene.f3, scene.f32, scene.rho, scene.xrho, scene.T)
F = d_f.F

# ---------------------------------------------------------------------
# Define a set of allowed R₀ values to iterate (these update r0[2])
# ---------------------------------------------------------------------

start_lin = 0
end_lin = 1e5
num_values = 1000

allowed_R0 = np.linspace(start_lin, end_lin, num_values)

# Prepare to store solutions from solve_ivp
solutions_list = []

# Loop over each allowed R₀ value, update r0[2], and integrate
for R0_val in allowed_R0:
    # Copy the base initial condition so the original remains unchanged
    r0_local = np.copy(scene.r0)
    r0_local[2] = R0_val  # Update only the R₀ component (index 2)

    # Integrate using solve_ivp
    start_time = timeit.default_timer()
    sol = solve_ivp(
        fun=F,
        t_span=(0, 1e3),  # Adjust the integration range as needed
        y0=r0_local,
        method='DOP853',
    )
    end_time = timeit.default_timer()
    execution_time = end_time - start_time
    print(f"Integrated with r0[2]={R0_val:.2f} in {execution_time:.3f} s")

    # Store the solution dictionary
    solutions_list.append({
        "R0": R0_val,
        "x": sol.t,  # independent variable array
        "r": sol.y,  # solution array; expected shape: (num_components, num_points)
        "execution_time": execution_time
    })



# ---------------------------------------------------------------------
# Instantiate the plotter and plot all curves on one figure
# ---------------------------------------------------------------------
plotter = MultiSolutionRPlotter(solutions_list)
plotter.plot_R(component=2, x_log_scale=True, cmap='viridis')
