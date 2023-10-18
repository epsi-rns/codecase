import pandas as pd

from datetime import datetime
from pandas import DataFrame

class PivotSample:
  def __init__(self, df_table: DataFrame) -> None:
    # save initial parameter
    self.df_table = df_table

  def build_pivot(self) -> None:
    try:
      # Perform pivot operations
      df_pivot = self.df_table.pivot_table(
        index='Date', columns='Fruit',
        aggfunc='count', fill_value=0)

      # Sort the index by both month and day
      df_pivot.index = df_pivot. \
        index.to_series().apply(lambda x:
          datetime.strptime(x, "%d/%m/%Y"))
      self.df_pivot = df_pivot.sort_index()

    except Exception as e:
      print("An error occurred " \
        + f"while processing data: {e}")

  def get_df_pivot(self) -> DataFrame:
    return self.df_pivot

  def process(self) -> None:
    self.build_pivot()

  def display(self) -> None:
    # Display the pivot table
    print("Pivot Table:")
    print(self.df_pivot)
