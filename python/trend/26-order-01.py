import matplotlib.pyplot as plt
import numpy as np

# Define the two points
p0 = (11, 49)
p1 = (12, 53)

pr1 = (0, 5)
pr2 = (5, 25)
pr3 = (12, 53)

# Define the linear function y = 4x + 5
def linear_func(x):
    return 4 * x + 5

# Generate x values for plotting the line
x_vals = np.linspace(0, 20, 400)
y_vals = linear_func(x_vals)

# Plot the line with a soft blue color and transparency
plt.plot(x_vals, y_vals, color='skyblue', alpha=0.7)

# Plot the points
plt.scatter(*p0, color='red', zorder=5)
plt.scatter(*p1, color='red', zorder=5)

plt.scatter(*pr1, color='blue', zorder=5)
plt.scatter(*pr2, color='blue', zorder=5)

# Show coordinates next to each point
plt.text(p0[0], p0[1]+2, f'p₀ = {p0}', ha='right')
plt.text(p1[0], p1[1]+2, f'p₁ = {p1}', ha='left')

plt.text(pr1[0], pr1[1]+2, f'pred₁ = {pr1}', ha='center')
plt.text(pr2[0], pr2[1]+2, f'pred₂ = {pr2}', ha='center')

# Customize the plot
plt.title('Example Case: Two Points')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0, 20)
plt.ylim(0, 100)
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.tight_layout()

# Show the plot
plt.show()
