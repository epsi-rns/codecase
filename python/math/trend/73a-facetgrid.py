import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Getting Matrix Values
pairCSV = np.genfromtxt("series.csv",
  skip_header=1, delimiter=",", dtype=float)

cols_all = ['xs', 'ys1', 'ys2', 'ys3']
cols_sel = ['ys1', 'ys2', 'ys3']

# Convert to pandas DataFrame
df = pd.DataFrame(pairCSV, columns=cols_all)

# Melt the DataFrame to long format for FacetGrid
df_melted = pd.melt(df,
  id_vars='xs', var_name='y', value_name='value')

# Create a FacetGrid with one row and three columns
g = sns.FacetGrid(df_melted,
  col='y', col_wrap=3, height=4, sharey=False)

# Map regplot to each facet
# with different color for each ys
g.map_dataframe(sns.regplot,
  x='xs', y='value', color='b')

# Add different colors for each ys category
for ax, ys_name in zip(g.axes.flat, cols_sel):
  df_subset = df_melted[
    df_melted['y'] == ys_name]

  color  = sns.color_palette("husl", 3)[
    cols_sel.index(ys_name)]

  sns.regplot(x='xs', y='value',
    data=df_subset, ax=ax,
    color=color)

# Set titles for each facet
g.set_titles('{col_name}')

# Set common labels for x-axis and y-axis
g.set_axis_labels('x', 'y')

# Show plot
plt.show()
