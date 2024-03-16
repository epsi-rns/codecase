import matplotlib.pyplot as plt

# Local Library
from Properties import get_properties, display

# Load properties from Properties.py helper
# and unpack them into local variables
properties = get_properties("50-samples.csv")
display(properties)
locals().update(properties)

# Plot the data and regression line
plt.figure(figsize=(10, 6))

plt.scatter(x_observed, y_observed,
  color='blue', label='Data Points')

plt.axvline(x=x_mean, color='green',
  linestyle='--', label='Mean of x')
plt.axhline(y=y_mean, color='orange',
  linestyle='--', label='Mean of y')

# Plot variance as error bars
plt.errorbar(x_mean, y_mean,
  xerr=x_std_dev, yerr=y_std_dev,
  fmt='o', color='purple', label='Variance')

# Chart Decoration
plt.title('Linear Regression')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()

