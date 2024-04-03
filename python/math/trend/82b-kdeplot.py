import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read data from CSV file directly
# into a pandas DataFrame
df = pd.read_csv("series.csv")

# Melt the DataFrame to long format for kdeplot
df_melted = pd.melt(df, id_vars='xs',
  var_name='Category', value_name='Value')

# Set the style of seaborn
sns.set_style("darkgrid")

# Create KDE plot for all categories
plt.figure(figsize=(8, 6))

sns.kdeplot(data=df_melted,
  x='Value', hue='Category', palette='deep',
  alpha=0.7, multiple='stack', linewidth=2)

# Add title and labels
plt.title('KDE Plot for ys1, ys2, and ys3')
plt.xlabel('Value')
plt.ylabel('Density')

# Add legend
plt.legend(title='Category', loc='upper left')

# Show plot
plt.show()

