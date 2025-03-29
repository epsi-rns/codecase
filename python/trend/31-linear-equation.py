import numpy as np
import matplotlib.pyplot as plt

# Initial Matrix Value
order = 1

# Setup numpy
np.set_printoptions(
  precision=2,
  formatter={
    'int':   '{:30,d}'.format,
    'float': '{:10,.8f}'.format
  },
  linewidth=np.inf,
  suppress=True)

# Getting Matrix Values
mCSV = np.genfromtxt("31-linear-equation.csv",
  skip_header=1, delimiter=",", dtype=float)

mCSVt   = np.transpose(mCSV)
x_values = mx = mCSVt[0]
y_values = mB = mCSVt[1]

# Perform linear regression using polyfit
mC = np.polyfit(x_values, y_values, deg=order)
print('Using polyfit')
print(f'Coefficients (a, b):\n\t{np.flip(mC)}\n')

# Calculated Matrix Variable
mA    = np.flip(np.vander(mx, order+1), axis=1)
mAt   = np.transpose(mA)
mAt_A = mAt @ mA
mAt_B = mAt @ mB
mC    = np.linalg.solve(mAt_A, mAt_B)

[a, b] = mC
print('Calculate manually')
print(f'Coefficients (a, b):\n\t{mC}\n')


# Draw Plot
x_plot = np.linspace(min(mx), max(mx), 100)
y_plot = a + b * x_plot

plt.scatter(mx, mB, label='Data points')
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

