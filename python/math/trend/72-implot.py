import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read data from CSV file directly
# into a pandas DataFrame,
# strip leading spaces from column names
df = pd.read_csv("series.csv") \
  .rename(columns=lambda x: x.strip())

# Melt the DataFrame to long format
# for linear model plot
df_melted = pd.melt(df,
  id_vars='xs', var_name='y', value_name='value')

# Scatter plot with regression line
plt.figure(figsize=(8, 6))
sns.lmplot(x='xs', y='value',
  data=df_melted, hue='y')

# Adjust the position of the title
plt.subplots_adjust(top=0.9)

# Plot formatting
plt.title('Scatter Plot with Regression Line')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()

