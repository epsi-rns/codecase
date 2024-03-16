import matplotlib.pyplot as plt

# Local Library
from Properties import get_properties, display

# Load properties from Properties.py helper
# and unpack them into local variables
properties = get_properties("50-samples.csv")
display(properties)
locals().update(properties)

# Plot the data series
plt.figure(figsize=(10, 6))
plt.scatter(x_observed, y_observed, color='blue',
  s=100, label='Data Points')

# Plot deviation from mean
plt.axhline(y=y_mean, color='orange',
  linestyle='--',  label='Mean of y')
plt.vlines(x_observed, y_observed, y_mean,
  linestyle='--', color='teal',
  label='Deviation from Mean (y)')

# Chart Decoration
plt.title('Mean and Deviation')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()

