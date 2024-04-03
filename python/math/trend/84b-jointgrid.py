import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read data from CSV file directly
# into a pandas DataFrame,
# strip leading spaces from column names
df = pd.read_csv("series.csv") \
  .rename(columns=lambda x: x.strip())

# Create a JointGrid object
g = sns.JointGrid(data=df, x='xs', y='ys3')

# Plot the scatter plot in the center
g.plot_joint(sns.regplot)

# Plot the histograms on the marginal axes
g.plot_marginals(sns.boxplot)

# Show the plot
plt.show()
