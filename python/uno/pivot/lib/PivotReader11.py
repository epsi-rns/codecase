import pandas as pd

from pprint import pprint
from typing import Dict

class PivotReader:
  def __init__(self,
      document  : 'com.sun.star.sheet.SpreadsheetDocument',
      sheetName : str,
      columns   : Dict[str, str]) -> None:

    # save initial parameter
    self.document = document
    self.sheet = self.document. \
      Sheets[sheetName]

    # Unpack the dictionary keys and values
    # into class attributes
    for key, value in columns.items():
      setattr(self, f"col_{key}", value)

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

  def process(self) -> None:
    self.load_data()

    # Print the updated DataFrame
    print(self.df_source)
    print()
