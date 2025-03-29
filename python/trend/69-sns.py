import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis

pairCSV = np.genfromtxt("50-samples.csv",
  skip_header=1, delimiter=",", dtype=int)

# Extract x and y values from CSV data
x_observed = pairCSV[:, 0]
y_observed = pairCSV[:, 1]

# Calculate skewness and kurtosis of y
y_skew     = skew(y_observed)
y_kurtosis = kurtosis(y_observed)

# Plot distribution of y with annotations
sns.set(style="whitegrid")
sns.displot(y_observed,
  bins=10, kde=True, rug=True)

# Annotate skewness and kurtosis on the plot
plt.text(0.9, 0.9,
  f'Skewness = {y_skew:.2f}',
  ha='center', va='center',
  transform=plt.gca().transAxes)
plt.text(0.9, 0.8,
  f'Kurtosis = {y_kurtosis:.2f}',
  ha='center', va='center',
  transform=plt.gca().transAxes)

plt.xlabel('y')
plt.ylabel('Density')
plt.title('Distribution of Observed y '
  + 'with Skewness and Kurtosis')
plt.show()
