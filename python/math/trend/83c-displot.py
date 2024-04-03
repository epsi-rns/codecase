import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read data from CSV file directly
# into a pandas DataFrame,
# strip leading spaces from column names
df = pd.read_csv("series.csv") \
  .rename(columns=lambda x: x.strip())

# Select only columns ys1, ys2, and ys3
cols_selected = ['ys1', 'ys2', 'ys3']
df_selected = df[cols_selected]

# Define a color palette for the displot
palette = sns.color_palette(
  "husl", len(cols_selected))

# Create displot for selected columns
plt.figure(figsize=(8, 6))
sns.displot(data=df_selected,
  kind='hist', rug=True, kde=True,
  palette=palette, alpha=0.7, multiple='layer')

# Add title and labels
plt.title('Distribution Plot for ys1, ys2, and ys3')
plt.xlabel('Value')
plt.ylabel('Density')

# Show plot
plt.show()
