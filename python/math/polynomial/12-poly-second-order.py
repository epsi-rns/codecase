import numpy as np
import matplotlib.pyplot as plt

# Initial Matrix Value
order = 2

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
mCSV = np.genfromtxt("12-data-second-order.csv",
  skip_header=1, delimiter=",", dtype=float)

mCSVt   = np.transpose(mCSV)
x_values = mx = mCSVt[0]
y_values = mB = mCSVt[1]

# Perform quadratic regression using polyfit
mC = np.polyfit(x_values, y_values, deg=order)
print('Using polyfit')
print(f'Coefficients (a, b, c):\n\t{np.flip(mC)}\n')

# Calculated Matrix Variable
mA    = np.flip(np.vander(mx, order+1), axis=1)
mAt   = np.transpose(mA)
mAt_A = mAt @ mA
mAt_B = mAt @ mB
mC    = np.linalg.solve(mAt_A, mAt_B)

[a, b, c] = mC
print('Calculate manually')
print(f'Coefficients (a, b, c):\n\t{mC}\n')


# Draw Plot
x_plot = np.linspace(min(mx), max(mx), 100)
y_plot = a + b * x_plot + c * x_plot**2

plt.scatter(mx, mB, label='Data points')
plt.plot(x_plot, y_plot, color='red',
  label='Fitted second-order polynomial')

plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.suptitle(
  'Second-order polynomial curve fitting')

subfmt = "a = %.2f, b = %.2f, c = %.2f"
plt.title(subfmt % (a, b, c), y=-0.01)

plt.show()

