import pandas as pd

from datetime import datetime
from typing import List
from pandas import DataFrame

class PivotSample:
  def __init__(self,
      df_table: DataFrame,
      categories: List[str]) -> None:

    # save initial parameter
    self.df_table = df_table
    self.categories = categories

  def build_pivot(self) -> None:
    try:
      # Perform pivot operations
      df_pivot = self.df_table.pivot_table(
        index='Date', columns='Fruit',
        aggfunc='count', fill_value=0)

      # Sort the index by both month and day
      df_pivot.index = df_pivot. \
        index.to_series().apply(lambda x:
          datetime.strptime(x, "%d/%m/%Y").date())
      df_pivot = df_pivot.sort_index()

      # Ensure all specified columns are present
      for cat in self.categories:
        if ('Number', cat) not in df_pivot.columns:
          df_pivot[('Number', cat)] = 0

      # Sort the columns (fruits) in alphabetical order
      self.df_pivot = df_pivot.sort_index(axis=1)

    except Exception as e:
      print("An error occurred " \
        + f"while processing data: {e}")

  def add_total_column(self):
    # Calculate the row sums and add a total column
    row_sums = self.df_pivot.sum(axis=1)
    self.df_pivot[('Total', 'Total')] = row_sums

  def add_total_row(self):
    # Calculate the sum for each column
    # and add a total row
    total_row = self.df_pivot.sum().to_frame().T
    total_row.index = ['Total']
    self.df_pivot = pd.concat(
      [self.df_pivot, total_row])

  def access_headers_and_column(self):
    # Access and print column headers (keys)
    column_headers = self.df_pivot.columns
    print("Column Headers:", column_headers)

    # Access and print a specific column,
    # for example, "Orange"
    orange_column = self.df_pivot[('Number', 'Orange')]
    print("Orange Column:")
    print(orange_column)

  def get_df_pivot(self) -> DataFrame:
    return self.df_pivot

  def process(self) -> None:
    self.build_pivot()
    self.add_total_column()
    self.add_total_row()

  def display(self) -> None:
    # Display the pivot table
    print("Pivot Table:")
    print(self.df_pivot)
