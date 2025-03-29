import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set the style of seaborn
sns.set_style("ticks")

# Read data from CSV file directly
# into a pandas DataFrame
df = pd.read_csv("series.csv")

# Melt the DataFrame to long format for rugplot
df_melted = pd.melt(df, id_vars='xs',
  var_name='Category', value_name='Value')

# Define a color palette for the rug plots
# Use one less color for 'xs'
palette = sns.color_palette(
  "husl", len(df.columns) - 1)  

# Create rug plot for each category
plt.figure(figsize=(8, 6))

# Exclude 'xs' column
for i, col in enumerate(df.columns[1:]):
  df_subset = df_melted[df_melted['Category'] == col]
  sns.rugplot(data=df_subset, x='Value',
    color=palette[i], label=col, alpha=0.7)

# Add title and labels
plt.title('Rug Plot for ys1, ys2, and ys3')
plt.xlabel('Value')
plt.ylabel('Density')

# Add legend
plt.legend(title='Category', loc='upper left')

# Show plot
plt.show()
