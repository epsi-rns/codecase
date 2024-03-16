import numpy as np
import matplotlib.pyplot as plt

# Given data
x_values = np.array([
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
y_values = np.array([
  5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53])

# Curve Fitting Order
order = 1

# Perform linear regression using polyfit
mC = np.polyfit(x_values, y_values, deg=order)
print('Using polyfit')
print(f'Coefficients (a, b):\n\t{np.flip(mC)}\n')

# Draw Plot
[a, b] = np.flip(mC)
x_plot = np.linspace(min(x_values), max(x_values), 100)
y_plot = a + b * x_plot

plt.scatter(x_values, y_values, label='Data points')
plt.plot(x_plot, y_plot, color='red',
  label='Linear Equation')

plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.suptitle(
  'Straight line fitting')

subfmt = "a = %.2f, b = %.2f"
plt.title(subfmt % (a, b), y=-0.01)

plt.show()

