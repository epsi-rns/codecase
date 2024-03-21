import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Getting Matrix Values
pairCSV = np.genfromtxt("50-samples.csv",
  skip_header=1, delimiter=",", dtype=int)

# Extract x and y values from CSV data
x_observed = pairCSV[:, 0]
y_observed = pairCSV[:, 1]

# Calculate mean and standard deviation of y
y_mean = np.mean(y_observed)
y_std  = np.std(y_observed)

# Calculate skewness and kurtosis of y
y_skewness = np.mean(
  ((y_observed - y_mean) / y_std) ** 3)
y_kurtosis = np.mean(
  ((y_observed - y_mean) / y_std) ** 4)

# Create histogram
plt.hist(y_observed, bins=10,
  density=True, alpha=0.6, color='cyan')

# Create range for x values
x_range = np.linspace(
  min(y_observed), max(y_observed), 100)

y_dist = norm.pdf(x_range, y_mean, y_std)

# Plot normal distribution curve
plt.plot(x_range, y_dist, color='blue',
  label='Normal Distribution')

plt.xlabel('y')
plt.ylabel('Density')
plt.title('Normal Distribution Plot of '
  + 'Observed y with Skewness and Kurtosis')
plt.legend()
plt.grid(True)
plt.show()

