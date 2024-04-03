import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read data from CSV file directly
# into a pandas DataFrame,
# strip leading spaces from column names
df = pd.read_csv("series.csv") \
  .rename(columns=lambda x: x.strip())
  
# Define selected columns
cols_sel = ['ys1', 'ys2', 'ys3']

# Melt the DataFrame to long format for FacetGrid
df_melted = df.melt(
  id_vars='xs', value_vars=cols_sel)

# Create a FacetGrid with seaborn
g = sns.FacetGrid(df_melted,
  col='variable', col_wrap=3,
  sharex=False, sharey=True)

# Iterate over selected columns and
# map regplot to each column in the FacetGrid
for ax, col in zip(g.axes.flatten(), cols_sel):
  df_subset = df.melt(
    id_vars='xs', value_vars=col)

  color = sns.color_palette("husl", 3)[
    cols_sel.index(col)]

  sns.regplot(x='xs', y='value',
    data=df_subset, ax=ax, color=color)

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
