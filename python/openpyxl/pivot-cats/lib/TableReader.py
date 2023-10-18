import pandas as pd

from typing import Dict
from pandas import DataFrame

# openPyXL
from openpyxl.worksheet.worksheet import Worksheet

class TableReader:
  def __init__(self,
      sheet: Worksheet,
      columns: Dict[str, str]) -> None:

    # save initial parameter
    self.sheet = sheet

    # Unpack the dictionary keys and values
    # into class attributes
    for key, value in columns.items():
      setattr(self, f"col_{key}", value)

    # initialize dataframe
    self.df_table = pd.DataFrame({
      "Number": [], "Date": [], "Category": [] })

  def load_data(self) -> None:
    # range to be proceed
    # omit header and plus one for the last
    max_row = self.sheet.max_row
    range_rows = range(2, max_row+1)

    print(f'Range  : {range_rows}')

    for row in range_rows:
      # Convert the new data to a DataFrame
      new_row = pd.DataFrame({
        "Number"   : self.sheet[
            f'{self.col_index}{row}'].value,
        "Date"     : self.sheet[
            f'{self.col_date}{row}'].value,
        "Category" : self.sheet[
            f'{self.col_cat}{row}'].value
      }, index=[0])

      # Append the new row to the existing DataFrame
      self.df_table = pd.concat(
        [self.df_table, new_row], ignore_index=True)

  def get_df_table(self) -> DataFrame:
    return self.df_table

  def process(self) -> None:
    self.load_data()

  def display(self) -> None:
    # Display the header
    print("Header:", self.df_table.columns)

    # Display the data
    print("Data:")
    print(self.df_table)
