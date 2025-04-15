from events import *
import matplotlib.pyplot as plt


# Create a range of R values where you want to evaluate G
R_min, R_max = -1e1, 1e1   # For example, from -5 to 5
num_points = 200       # Number of points in this interval
R_values = np.linspace(R_min, R_max, num_points)

# Evaluate G(R) over the entire range of R_values
G_values = [G(R) for R in R_values]

# Plot G(R) vs R
plt.figure(figsize=(8, 5))
plt.plot(R_values, G_values, label='G(R)')
plt.xlabel('R')
plt.ylabel('G(R)')
plt.title('Plot of G(R)')
plt.grid(True)
plt.legend()
plt.show()

root = fsolve(G, np.array([8]))

z1 = 0
z2 = 3.54091717
z3 = 8.9026342
# but all of these zeroes give solutions that diverge.

print(root)
