import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set the style of seaborn
sns.set_style("whitegrid")

# Read data from CSV file directly
# into a pandas DataFrame,
# strip leading spaces from column names
df = pd.read_csv("series.csv") \
  .rename(columns=lambda x: x.strip())

# Select columns ys1, ys2, and ys3
cols_selected = ['ys1', 'ys2', 'ys3']

# Create a figure and axis objects
plt.figure(figsize=(8, 6))

# Plot displot for selected columns
sns.histplot(data=df[cols_selected],
  kde=True, element='step',
  multiple='layer', palette='husl')

# Add title and labels
plt.title('Distribution Plot for ys1, ys2, and ys3')
plt.xlabel('Value')
plt.ylabel('Density')

# Show plot
plt.show()
