import numpy as np
import matplotlib.pyplot as plt

# Getting Matrix Values
pairCSV = np.genfromtxt("50-samples.csv",
  skip_header=1, delimiter=",", dtype=int)

# Extract x and y values from CSV data
x_observed = pairCSV[:, 0]
y_observed = pairCSV[:, 1]

# Calculate properties
y_median = np.median(y_observed)
y_mean   = np.mean(y_observed)
y_min    = np.min(y_observed)
y_max    = np.max(y_observed)

# Calculate mode using numpy
y_mode   = np.argmax(np.bincount(y_observed))

# Plot x,y scatter plot
plt.scatter(x_observed, y_observed,
  color='blue', label='Data')

# Add horizontal lines for properties
plt.axhline(y_median, c='r', ls='--',
  label=f'Median: {y_median}')
plt.axhline(y_mean,   c='g', ls='--',
  label=f'Mean: {y_mean:.2f}')
plt.axhline(y_mode,   c='m', ls='--',
  label=f'Mode: {y_mode}')
plt.axhline(y_min,    c='c', ls='--',
  label=f'Min: {y_min}')
plt.axhline(y_max,    c='y', ls='--',
  label=f'Max: {y_max}')

# Add labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Scatter Plot with Y-axis Properties')
plt.legend()

# Show plot
plt.grid(True)
plt.show()
