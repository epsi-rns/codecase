import matplotlib.pyplot as plt
import numpy as np

# Define the four data points
p0 = (9, 1742)
p1 = (10, 2345)
p2 = (11, 3074)
p3 = (12, 3941)

# Define prediction points based on the formula y = 5 + 4x + 3x^2 + 2x^3
pr1 = (0, 5)
pr2 = (5, 350)

# Define the cubic function
def cubic_func(x):
    return 5 + 4 * x + 3 * x**2 + 2 * x**3

# Generate x values for plotting the curve
x_vals = np.linspace(0, 20, 400)
y_vals = cubic_func(x_vals)

# Plot the curve with a soft blue color and transparency
plt.plot(x_vals, y_vals, color='skyblue', alpha=0.7)

# Plot the data points
plt.scatter(*p0, color='red', zorder=5)
plt.scatter(*p1, color='red', zorder=5)
plt.scatter(*p2, color='red', zorder=5)
plt.scatter(*p3, color='red', zorder=5)

# Plot the prediction points
plt.scatter(*pr1, color='blue', zorder=5)
plt.scatter(*pr2, color='blue', zorder=5)

# Show coordinates next to each point
plt.text(p0[0], p0[1]+25, f'p₀ = {p0}', ha='right')
plt.text(p1[0], p1[1]+25, f'p₁ = {p1}', ha='right')
plt.text(p2[0], p2[1]+25, f'p₂ = {p2}', ha='left')
plt.text(p3[0], p3[1]+25, f'p₃ = {p3}', ha='left')

plt.text(pr1[0], pr1[1]+20, f'pred₁ = {pr1}', ha='center')
plt.text(pr2[0], pr2[1]+20, f'pred₂ = {pr2}', ha='center')

# Customize the plot
plt.title('Example Case: Four Points')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0, 20)
plt.ylim(0, 4500)
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.tight_layout()

# Show the plot
plt.show()
