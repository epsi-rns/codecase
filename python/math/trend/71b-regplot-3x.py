import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Getting Matrix Values
pairCSV = np.genfromtxt("series.csv",
  skip_header=1, delimiter=",", dtype=float)

# Extract x and y values from CSV data
xs, ys1, ys2, ys3 = pairCSV.T

# Creating subplots
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

# Defining a Seaborn color palette
# You can specify the number of colors here
palette = sns.color_palette("husl", 3)

# Plotting each scatter plot with regression line
pairs = zip([ys1, ys2, ys3], ['ys1', 'ys2', 'ys3'])

for i, (ys, title) in enumerate(pairs):
  sns.regplot(x=xs, y=ys,
    ax=axs[i], color=palette[i])

  axs[i].set_title(title)
  axs[i].set_xlabel('x')
  axs[i].set_ylabel('y')

# Plot formatting
plt.tight_layout()
plt.show()
