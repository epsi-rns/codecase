import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read data from CSV file directly
# into a pandas DataFrame,
# strip leading spaces from column names
df = pd.read_csv("series.csv") \
  .rename(columns=lambda x: x.strip())

# Set the style of seaborn
sns.set_style("whitegrid")

# Define a color palette for the KDE plot
# Adjust the number of colors as needed
palette = sns.color_palette("husl", 3)

# Create a KDE plot for each ys category
plt.figure(figsize=(8, 6))
for i, col in enumerate(['ys1', 'ys2', 'ys3']):
  sns.kdeplot(data=df[col],
    color=palette[i], label=col)

# Add title and labels
plt.title('KDE Plot for ys1, ys2, and ys3')
plt.xlabel('Value')
plt.ylabel('Density')

# Add legend
plt.legend()

# Show plot
plt.show()
