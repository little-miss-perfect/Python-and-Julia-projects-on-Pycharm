from variables import *
import matplotlib.pyplot as plt


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




# Create a range of R values where you want to evaluate G
R_min, R_max = -0.05e2, 0.05e2   # For example, from -5 to 5
num_points = 200       # Number of points in this interval
R_values = np.linspace(R_min, R_max, num_points)

# Evaluate G(R) over the entire range of R_values
f_values = [f(R) for R in R_values]

# Plot G(R) vs R
plt.figure(figsize=(8, 5))
plt.plot(R_values, f_values, label='f(R)')
plt.xlabel('R')
plt.ylabel('f(R)')
plt.title('Plot of f(R)')
plt.grid(True)
plt.legend()
plt.show()




# Create a range of R values where you want to evaluate G
R_min, R_max = mHS, 0.10e2   # For example, from -5 to 5
num_points = 200       # Number of points in this interval
R_values = np.linspace(R_min, R_max, num_points)

# Evaluate G(R) over the entire range of R_values
f2_values = [f2(R) for R in R_values]

# Plot G(R) vs R
plt.figure(figsize=(8, 5))
plt.plot(R_values, f2_values, label='f2(R)')
# and to plot the single point at "mHS" we write
plt.scatter([mHS], [f2(mHS)],
            color='red', marker='.', s=200, label=f'(mHS, f2(mHS)) = ({mHS:.2f}, {f2(mHS):.2f})')
plt.xlabel('R')
plt.ylabel('f2(R)')
plt.title('Plot of f2(R)')
plt.grid(True)
plt.legend()
plt.show()
