import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skewnorm, norm, kurtosis

# Generate data points for x-axis
x = np.linspace(-5, 5, 1000)

# Calculate the corresponding y-values
# for the standard normal distribution
y_standard = norm.pdf(x)

# Examples of distributions
# with different levels of kurtosis

# Standard normal distribution (Kurtosis = 0)
y_kurtosis_1 = skewnorm.pdf(x, a=0, loc=1, scale=1)

# Lower kurtosis
y_kurtosis_2 = skewnorm.pdf(x, a=0, loc=1, scale=0.5)

# Higher kurtosis
y_kurtosis_3 = skewnorm.pdf(x, a=0, loc=1, scale=2)

# Plot the normal distribution
plt.plot(x, y_standard, label='Standard Normal')

# Plot distributions with
# different levels of kurtosis
plt.plot(x, y_kurtosis_1, ls='-.',
  label='Standard Kurtosis = 0')
plt.plot(x, y_kurtosis_2, ls='-.',
  label='Lower Kurtosis')
plt.plot(x, y_kurtosis_3, ls='-.',
  label='Higher Kurtosis')

# Add labels and title
plt.xlabel('x')
plt.ylabel('Density')
plt.title('Normal Distribution with Different Kurtosis')

# Add legend
plt.legend(loc='upper left')

# Show grid
plt.grid(True)

# Show plot
plt.show()
