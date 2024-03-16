import numpy as np
import matplotlib.pyplot as plt

# Given data
x_values = np.array([
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
y_values = np.array([
  5, 14, 41, 98, 197, 350, 569, 866, 
  1253, 1742, 2345, 3074, 3941])

# Curve Fitting Order
order = 3

# Perform cubic regression using polyfit
mC = np.polyfit(x_values, y_values, deg=order)
print('Using polyfit')
print(f'Coefficients (a, b, c, d):\n\t{np.flip(mC)}\n')

# Draw Plot
[a, b, c, d] = np.flip(mC)
x_plot = np.linspace(min(x_values), max(x_values), 100)
y_plot = a + b * x_plot + \
         c * x_plot**2 + d * x_plot**3

plt.scatter(x_values, y_values, label='Data points')
plt.plot(x_plot, y_plot, color='red',
  label='Fitted third-order polynomial')

plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.suptitle(
  'Third-order polynomial curve fitting')

subfmt = "a = %.2f, b = %.2f, c = %.2f, d = %.2f"
plt.title(subfmt % (a, b, c, d), y=-0.01)

plt.show()

