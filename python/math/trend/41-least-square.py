import numpy as np
import statsmodels.api as sm

from scipy import stats

# Given data
x_values = np.array(
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
y_values = np.array(
  [5, 12, 25, 44, 69, 100, 137,
    180, 229, 284, 345, 412, 485])

# Perform least squares regression
# for a linear model (polynomial degree 1)
order = 1
mC    = np.polyfit(x_values, y_values, deg=order)
m     = mC[0]
b     = mC[1]

print('Using polyfit')
print(f'Coefficients (b = {b:2,.2f}, m = {m:2,.2f})\n')

# SciPy: scientific computing built on top of NumPy.
m, b, _, _, _ = stats.linregress(x_values, y_values)

print('Using linregress')
print(f'Coefficients (b = {b:2,.2f}, m = {m:2,.2f})\n')

# Statsmodels: statistical modeling and hypothesis testing.
x = sm.add_constant(x_values)
model = sm.OLS(y_values, x).fit()
b = model.params[0]
m = model.params[1]

print('Using Statsmodels')
print(f'Coefficients (b = {b:2,.2f}, m = {m:2,.2f})\n')
