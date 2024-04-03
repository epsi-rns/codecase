import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Getting Matrix Values
pairCSV = np.genfromtxt("series.csv",
  skip_header=1, delimiter=",", dtype=float)

# Convert the data to a pandas DataFrame
cols_all = ['xs', 'ys1', 'ys2', 'ys3']
df = pd.DataFrame(pairCSV, columns=cols_all)

# Melt the DataFrame to long format for boxplot
df_melted = pd.melt(df,
  id_vars='xs', var_name='y', value_name='value')

# Create violinplot
plt.figure(figsize=(8, 6))
sns.violinplot(x='y', y='value', data=df_melted)

# Visualize the distribution of values
# across different categories.
plt.title('Violin Plot for ys1, ys2, and ys3')
plt.xlabel('Variable')
plt.ylabel('Value')
plt.show()
