import pandas as pd

from pprint import pprint
from typing import Dict, List

class PivotSample:
  def __init__(self,
      sheetSourceName: str,
      columns: Dict[str, str],
      categories: List[str]) -> None:

    # Getting tthe source sheet
    document = XSCRIPTCONTEXT.getDocument()
    self.sheet_src = document.Sheets[sheetSourceName]

    # Unpack the dictionary keys and values
    # into class attributes
    for key, value in columns.items():
      setattr(self, f"col_{key}", value)

    self.categories = categories

    # initialize dataframe
    self.df_source = pd.DataFrame({
      "Number": [], "Date": [], "Category": [] })

  def get_lookup_cats(self) -> None:
    return ["Apple", "Banana", "Orange", "Grape",
      "Strawberry", "Durian", "Mango", "Dragon Fruit"]

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
    self.df_source.set_index("Date", inplace=True)

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
    self.pivot_table[('Total', 'Total')] = row_sums

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

    # Print the newly created pivot table
    print(self.pivot_table)
    print()

def main() -> None:
  columns = {
    'index' : 'A',
    'date'  : 'B',
    'cat'   : 'C'
  }

  categories = [
    "Apple", "Banana", "Dragon Fruit",
    "Durian", "Grape", "Mango",
    "Orange", "Strawberry"]

  sample = PivotSample('Example', columns, categories)
  sample.process()

