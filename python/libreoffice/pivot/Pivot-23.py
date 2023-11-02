import pandas as pd

from datetime import datetime, timedelta
from typing import Dict, List
from pandas import DataFrame

# Debugging purpose, just in case
from pprint import pprint

class PivotReader:
  def __init__(self,
      sheetSourceName: str,
      columns: Dict[str, str],
      categories: List[str]) -> None:

    # Getting the source sheet
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

class PivotWriter:
  def __init__(self,
      sheetDestName: str,
      pivot_table: pd.DataFrame,
      categories: List[str],
      start_cell: str) -> None:

    # save initial parameter
    self.sheetDestName = sheetDestName
    self.pivot_table = pivot_table
    self.categories = categories
    self.start_cell = start_cell

    # Get the 'Total' row as a separate variable
    self.total_row = self.pivot_table.loc['Total']

    # Exclude the 'Total' row from the DataFrame
    self.pivot_table = self.pivot_table.drop('Total')

  def prepare_sheet(self):
    document   = XSCRIPTCONTEXT.getDocument()
    sheets_dst = document.Sheets

    sheetName = self.sheetDestName
    if not sheets_dst.hasByName(sheetName):
      sheets_dst.insertNewByName(sheetName, 1)
    self.sheet_dst = sheets_dst[sheetName]

    desktop    = XSCRIPTCONTEXT.getDesktop()
    model      = desktop.getCurrentComponent()
    controller = model.getCurrentController()
    controller.setActiveSheet(self.sheet_dst)

    self.numberfmt = model.NumberFormats
    self.locale    = model.CharLocale

    self.dateFormat = self.numberfmt. \
      getStandardFormat(2, self.locale)

  def write(self) -> None:
    # Start filling cell horizontally
    addr = self.sheet_dst[self.start_cell].CellAddress

    # Fill the cells horizontally
    for col, cat in enumerate(self.categories, start=1):
      col_pos = addr.Column + col

      cell = self.sheet_dst. \
        getCellByPosition(col_pos, addr.Row)
      cell.String = cat

    # Iterate over both index and row data
    row_index = 0
    for date, row in self.pivot_table.iterrows():
      row_index += 1
      row_pos = addr.Row + row_index

      cell = self.sheet_dst. \
        getCellByPosition(addr.Column, row_pos)

      cell.Value = date
      cell.NumberFormat = self.dateFormat

      for col, cat in enumerate(
          self.categories, start=1):

        col_pos = addr.Column + col

        cell = self.sheet_dst. \
          getCellByPosition(col_pos, row_pos)
        cell.Value = int(row[('Number', cat)])

  def process(self) -> None:
    self.prepare_sheet()
    self.write()

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

  pd.set_option('display.max_rows', 10)

  reader = PivotReader(
    'Table', columns, categories)
  pivot_table = reader.get_pivot()

  # Print the newly created pivot table
  # on terminal console for debugging
  print(pivot_table)
  print()

  writer = PivotWriter(
    'Pivot', pivot_table, categories, 'B2')
  writer.process()

