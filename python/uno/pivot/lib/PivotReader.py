import pandas as pd

from pandas import DataFrame
from typing import Dict, List

# Local Library
from lib.helper import open_document

class PivotReader:
  def __init__(self,
      document: 'com.sun.star.sheet.SpreadsheetDocument',
      sheetName: str,
      columns: Dict[str, str],
      categories: List[str]) -> None:

    # save initial parameter
    self.document = document
    self.sheet = self.document. \
      Sheets[sheetName]

    # Unpack the dictionary keys and values
    # into class attributes
    for key, value in columns.items():
      setattr(self, f"col_{key}", value)

    self.categories = categories

    # initialize dataframe
    self.df_source = pd.DataFrame({
      "Number": [], "Date": [], "Category": [] })

  def get_last_used_row(self) -> None:
    cursor = self.sheet.createCursor()
    cursor.gotoEndOfUsedArea(False)
    cursor.gotoStartOfUsedArea(True)
    rows = cursor.getRows()
    
    return len(rows)

  def load_data(self) -> None:
    # range to be proceed
    # omit header and plus one for the last
    max_row = self.get_last_used_row()
    range_rows = range(2, max_row+1)

    print(f'Range  : {range_rows}')

    for row in range_rows:
      # Convert the new data to a DataFrame
      new_row = pd.DataFrame({
        "Number"   : int(self.sheet[
            f'{self.col_index}{row}'].Value),
        "Date"     : int(self.sheet[
            f'{self.col_date}{row}'].Value),
        "Category" : self.sheet[
            f'{self.col_cat}{row}'].String
      }, index=[0])

      # Append the new row to the existing DataFrame
      self.df_source = pd.concat(
        [self.df_source, new_row], ignore_index=True)

  def build_pivot(self) -> None:
    try:
      # Perform pivot operations
      self.pivot_table = self.df_source.pivot_table(
        index='Date', columns='Category',
        aggfunc='count', fill_value=0)

      # Ensure all specified columns are present
      for cat in self.categories:
        if ('Number', cat) not in self.pivot_table.columns:
          self.pivot_table[('Number', cat)] = 0

      # Sort the columns (fruits) in alphabetical order
      self.pivot_table = self.pivot_table.sort_index(axis=1)

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

  def get_pivot(self) -> DataFrame:
    self.load_data()
    self.build_pivot()
    self.add_total_column()
    self.add_total_row()

    return self.pivot_table
