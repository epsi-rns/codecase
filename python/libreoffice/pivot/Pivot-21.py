import pandas as pd

from pprint import pprint
from typing import Dict

class PivotSample:
  def __init__(self,
      sheetSourceName: str,
      columns: Dict[str, str]) -> None:

    # Getting tthe source sheet
    document = XSCRIPTCONTEXT.getDocument()
    self.sheet_src = document.Sheets[sheetSourceName]

    # Unpack the dictionary keys and values
    # into class attributes
    for key, value in columns.items():
      setattr(self, f"col_{key}", value)

    self.df_source = pd.DataFrame({
      "Number": [], "Date": [], "Category": [] })

  def get_last_used_row(self) -> None:
    cursor = self.sheet_src.createCursor()
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
        "Number"   : int(self.sheet_src[
            f'{self.col_index}{row}'].Value),
        "Date"     : int(self.sheet_src[
            f'{self.col_date}{row}'].Value),
        "Category" : self.sheet_src[
            f'{self.col_cat}{row}'].String
      }, index=[0])

      # Append the new row to the existing DataFrame
      self.df_source = pd.concat(
        [self.df_source, new_row], ignore_index=True)

    # Set the "Number" column as the index
    self.df_source.set_index("Number", inplace=True)


  def run(self) -> None:
    self.load_data()

    # Print the updated DataFrame
    print(self.df_source)
    print()

def main() -> None:
  columns = {
    'index' : 'A',
    'date'  : 'B',
    'cat'   : 'C'
  }

  sample = PivotSample('Example', columns)
  sample.run()
