import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Getting Matrix Values
pairCSV = np.genfromtxt("series.csv",
  skip_header=1, delimiter=",", dtype=float)

# Extract x and y values from CSV data
xs, ys1, ys2, ys3 = pairCSV.T

# Scatter plot with regression line
plt.figure(figsize=(8, 6))
sns.regplot(x=xs, y=ys1)
sns.regplot(x=xs, y=ys2)
sns.regplot(x=xs, y=ys3)

# Plot formatting
plt.title('Scatter Plot with Regression Line')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()

