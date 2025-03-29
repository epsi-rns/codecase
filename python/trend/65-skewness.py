import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skewnorm, norm, kurtosis

# Generate data points for x-axis
x = np.linspace(-5, 5, 1000)

# Calculate the corresponding y-values
# for the standard normal distribution
y_standard = norm.pdf(x)

# Calculate the corresponding y-values 
# or distributions with different skewness parameters
# Examples of skewed distributions
# with different skewness parameters

# Negative skewness
y_skewed_1 = skewnorm.pdf(x, a=-4)

# Moderate positive skewness
y_skewed_2 = skewnorm.pdf(x, a=2)

# High positive skewness
y_skewed_3 = skewnorm.pdf(x, a=6)

# Plot the normal distribution
plt.plot(x, y_standard, label='Standard Normal')

# Plot skewed distributions
# with different skewness parameters
plt.plot(x, y_skewed_1, ls='--',
         label='Negative Skewness = -4')
plt.plot(x, y_skewed_2, ls='--',
         label='Moderate Positive Skewness = 2')
plt.plot(x, y_skewed_3, ls='--',
         label='High Positive Skewness = 6')

# Add labels and title
plt.xlabel('x')
plt.ylabel('Density')
plt.title('Normal Distribution '
 + 'with Different Skewness')

# Add legend on the top left
plt.legend(loc='upper left')

# Show grid
plt.grid(True)

# Show plot
plt.show()
