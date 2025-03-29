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

# Create histogram
plt.hist(y_observed, bins=10,
  density=True, alpha=0.6, color='cyan')

# Define skewness and kurtosis values
y_skewness = 0.61
y_kurtosis = -0.91

# Create range for x values
x_range = np.linspace(
  min(y_observed), max(y_observed), 100)

# Calculate the corresponding y-values
# for the standard normal distribution
y_standard = norm.pdf(x_range, y_mean, y_std)

# Adjust the shape parameter manually
# to achieve the desired kurtosis
# You may need to experiment with different values
# to get closer to the desired kurtosis
shape_param = 4

# Calculate the corresponding y-values
# for skewnorm distribution with given skewness
# and adjusted shape parameter
y_ks = skewnorm.pdf(x_range, a=y_skewness,
  loc=y_mean, scale=y_std / shape_param)

# Plot normal distribution curve
plt.plot(x_range, y_standard,
  label='Standard Normal')

# Plot skewnorm distribution
# with given skewness and kurtosis
plt.plot(x_range, y_ks, ls='-.',
  label='With Kurtosis and Skewness')

# Add labels and title
plt.xlabel('x')
plt.ylabel('Density')
plt.title('Normal Distribution '
  + 'with Kurtosis and Skewness')

# Add legend
plt.legend()

# Show grid
plt.grid(True)

# Show plot
plt.show()
