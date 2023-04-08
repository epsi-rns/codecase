import numpy as np
import matplotlib.pyplot as plt

# Initial Matrix Value

order = 3
mx  = np.array([
        0, 1, 2, 3,
        4, 5, 6, 7,
        8, 9, 10, 11, 12])
mB  = np.array([
         5,   10,  410,   90,
       190,  350,  460,  960,
      1050, 1740, 1340, 3270, 3540])

# Calculated Matrix Variable
mA    = np.flip(np.vander(mx, 4), axis=1)
mAt   = np.transpose(mA)
mAt_A = mAt @ mA
mAt_B = mAt @ mB
mC    = np.linalg.solve(mAt_A, mAt_B)
[a, b, c, d] = mC
print("Coefficients (a, b, c, d):", mC)

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

