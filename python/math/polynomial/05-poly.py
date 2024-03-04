import numpy as np
import matplotlib.pyplot as plt

# Initial Matrix Value
order = 3
np.set_printoptions(precision=2, suppress=True)

# Getting Matrix Values
mCSV = np.genfromtxt("poly.csv",
  skip_header=1, delimiter=",", dtype=float)

mCSVt   = np.transpose(mCSV)
x_values = mx = mCSVt[0]
y_values = mB = mCSVt[1]

# Perform cubic regression using polyfit
mC = np.polyfit(x_values, y_values, deg=order)
print('Using polyfit')
print(f'Coefficients (a, b, c, d):\n\t{np.flip(mC)}\n')

# Calculated Matrix Variable
mA    = np.flip(np.vander(mx, order+1), axis=1)
mAt   = np.transpose(mA)
mAt_A = mAt @ mA
mAt_B = mAt @ mB
mC    = np.linalg.solve(mAt_A, mAt_B)

[a, b, c, d] = mC
print('Calculate manually')
print(f'Coefficients (a, b, c, d):\n\t{mC}\n')

for x in mx:
  y = a + b*x + c*x**2 + d*x**3
  print(f'x = {x:5}  =>  y = {y:10,.2f} ')

# Draw Plot
x_plot = np.linspace(min(mx), max(mx), 100)
y_plot = a + b * x_plot + \
         c * x_plot**2 + d * x_plot**3

plt.scatter(mx, mB, label='Data points')
plt.plot(x_plot, y_plot, color='red',
  label='Fitted third-order polynomial')

plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.suptitle(
  'Third-order polynomial curve fitting')

subfmt = "a = %.2f, b = %.2f c = %.2f, d = %.2f"
plt.title(subfmt % (a, b, c, d), y=-0.01)

plt.show()

