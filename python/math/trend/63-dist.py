import numpy as np
import matplotlib.pyplot as plt

# Generate data points for x-axis
x = np.linspace(-5, 5, 1000)

# Calculate the corresponding y-values
# for a standard normal distribution
y = 1 / np.sqrt(2 * np.pi) * np.exp(-0.5 * x**2)

# Plot the normal distribution
plt.plot(x, y, color='blue')

# Add labels and title
plt.xlabel('x')
plt.ylabel('Density')
plt.title('Standard Normal Distribution')

# Show grid
plt.grid(True)

# Show plot
plt.show()
