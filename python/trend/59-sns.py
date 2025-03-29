import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Getting Matrix Values
pairCSV = np.genfromtxt("50-samples.csv",
  skip_header=1, delimiter=",", dtype=float)

# Extract x and y values from CSV data
x_observed = pairCSV[:, 0]
y_observed = pairCSV[:, 1]

# Scatter plot with regression line
plt.figure(figsize=(8, 6))
sns.regplot(x=x_observed, y=y_observed)
plt.title('Scatter Plot with Regression Line')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()

