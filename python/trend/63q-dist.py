import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Generate data points for x-axis
x = np.linspace(-5, 5, 1000)

# Calculate the corresponding y-values
# for a standard normal distribution
y = norm.pdf(x)

# Calculate the percentiles
percentiles = [25, 50, 75, 100]
quantiles = np.percentile(x, percentiles)

# Plot the normal distribution
plt.plot(x, y, color='black')

# Shade regions corresponding to percentiles
for i, q in enumerate(quantiles):
  plt.fill_between(
    x[x <= q], y[x <= q],
    color=f'C{i}', alpha=0.3)

# Add labels and title
plt.xlabel('x')
plt.ylabel('Density')
plt.title('Standard Normal Distribution '
  + 'with Quantiles')

# Show grid
plt.grid(True)

# Show plot
plt.show()
