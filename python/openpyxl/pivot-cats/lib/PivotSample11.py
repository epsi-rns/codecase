import pandas as pd

from datetime import datetime
from pandas import DataFrame

class PivotSample:
  def __init__(self, df_table: DataFrame) -> None:
    # save initial parameter
    self.df_table = df_table

  def process(self) -> None:
    # Perform pivot operations, for example:
    pivot_table = self.df_table.pivot_table(
      index='Date', columns='Fruit',
      aggfunc='count', fill_value=0)

    # Sort the index by both month and day
    pivot_table.index = pivot_table. \
      index.to_series().apply(lambda x:
        datetime.strptime(str(x), "%d/%m/%Y"))
    self.pivot_table = pivot_table.sort_index()

    print("Pivot Table:")
    print(self.pivot_table)
