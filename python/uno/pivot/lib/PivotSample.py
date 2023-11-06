import pandas as pd

from datetime import datetime, timedelta
from typing import List
from pandas import DataFrame

class PivotSample:
  def __init__(self, source_csv: str,
      categories: List[str]) -> None:

    # save initial parameter
    self.filename = source_csv
    self.categories = categories

  def date_ordinal(self, value, format_source):
    # Offset of the date value
    # for the date of 1900-01-00
    offset = 693594

    date_value = datetime.strptime(
                   value, format_source)
    return date_value.toordinal() - offset

  def load_data(self) -> None:
    try:
      # Load data into a DataFrame
      self.dataframe = pd.read_csv(self.filename)

      # Define the format of the original date in CSV
      format_source = '%d/%m/%Y'

      # Apply the date_ordinal function
      # to the "Date" column
      self.dataframe['Date'] = self.dataframe['Date'].\
        apply(lambda date: self.date_ordinal(
          date, format_source))

    except FileNotFoundError:
      print("Error: The file "\
        + f"'{self.filename}' was not found.")
    except Exception as e:
      print("An error occurred "
         + f"while loading data: {e}")

  def build_pivot(self) -> None:
    try:
      # Perform pivot operations
      self.pivot_table = self.dataframe.pivot_table(
        index='Date', columns='Fruit',
        aggfunc='count', fill_value=0)

      # Ensure all specified columns are present
      for cat in self.categories:
        if ('Number', cat) not in \
            self.pivot_table.columns:
          self.pivot_table[('Number', cat)] = 0

      # Sort the columns (fruits) in alphabetical order
      self.pivot_table = \
        self.pivot_table.sort_index(axis=1)

    except Exception as e:
      print("An error occurred " \
        + f"while processing data: {e}")

  def add_total_column(self):
    # Calculate the row sums and add a total column
    row_sums = self.pivot_table.sum(axis=1)
    self.pivot_table[('Total Date', 'Total')] = row_sums

  def add_total_row(self):
    # Calculate the sum for each column
    # and add a total row
    total_row = self.pivot_table.sum().to_frame().T
    total_row.index = ['Total']
    self.pivot_table = pd.concat(
      [self.pivot_table, total_row])

  def process(self) -> None:
    self.load_data()
    self.build_pivot()
    self.add_total_column()
    self.add_total_row()

  def get_dataframe(self) -> DataFrame:
    return self.dataframe

  def get_pivot(self) -> DataFrame:
    return self.pivot_table

