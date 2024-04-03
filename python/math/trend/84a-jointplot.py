import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read data from CSV file directly
# into a pandas DataFrame,
# strip leading spaces from column names
df = pd.read_csv("series.csv") \
  .rename(columns=lambda x: x.strip())

# Use seaborn's jointplot to create
# a scatter plot with KDE at the marginal
sns.jointplot(data=df, x='xs', y='ys3',
  kind='reg', marginal_kws={'fill': True})

# Show the plot
plt.show()
