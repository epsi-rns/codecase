import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, skewnorm

pairCSV = np.genfromtxt("50-samples.csv",
  skip_header=1, delimiter=",", dtype=int)

# Extract x and y values from CSV data
x_observed = pairCSV[:, 0]
y_observed = pairCSV[:, 1]

# Calculate mean and standard deviation of y
y_mean = np.mean(y_observed)
y_std  = np.std(y_observed)

# Calculate skewness and kurtosis of y
y_skewness = 0.61
y_kurtosis = -0.91

# Create histogram
plt.hist(y_observed, bins=10,
  density=True, alpha=0.6, color='cyan')

# Plot normal distribution curve
x_range = np.linspace(
  min(y_observed), max(y_observed), 1000)
y_standard = norm.pdf(x_range, y_mean, y_std)
plt.plot(x_range, y_standard,
  label='Standard Normal')

# Plot vertical lines
# or add annotations for properties
y_median = np.median(y_observed)
y_mean   = np.mean(y_observed)
y_min    = min(y_observed)
y_max    = max(y_observed)

# Calculate mode using numpy
y_mode = np.argmax(np.bincount(y_observed))

# Add vertical lines for properties
plt.axvline(y_median, c='r', ls='--',
  label=f'Median: {y_median}')
plt.axvline(y_mean,   c='g', ls='--',
  label=f'Mean: {y_mean:.2f}')
plt.axvline(y_mode,   c='m', ls='--',
  label=f'Mode: {y_mode}')
plt.axvline(y_min,    c='c', ls='--',
  label=f'Min: {y_min}')
plt.axvline(y_max,    c='y', ls='--',
  label=f'Max: {y_max}')

# Add labels and title
plt.xlabel('x')
plt.ylabel('Density')
plt.title('Normal Distribution '
  + 'with Y-axis Properties')
plt.legend()

# Show grid
plt.grid(True)

# Show plot
plt.show()
