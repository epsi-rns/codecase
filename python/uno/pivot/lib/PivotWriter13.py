import uno
import pandas as pd

from datetime import datetime, timedelta
from typing import Dict, List
from pandas import DataFrame

class PivotWriter:
  def __init__(self,
      document    : 'com.sun.star.sheet.SpreadsheetDocument',
      sheetName   : str,
      pivot_table : pd.DataFrame,
      categories  : List[str],
      start_cell  : str) -> None:

    # save initial parameter
    self.document = document
    self.sheetName   = sheetName
    self.pivot_table = pivot_table
    self.categories  = categories
    self.start_cell  = start_cell

    # Get the 'Total' row as a separate variable
    self.total_row = self.pivot_table.loc['Total']

    # Exclude the 'Total' row from the DataFrame
    self.pivot_table = self.pivot_table.drop('Total')

  def prepare_sheet(self):
    sheets = self.document.Sheets

    if not sheets.hasByName(self.sheetName):
      sheets.insertNewByName(self.sheetName, 1)
    self.sheet = sheets[self.sheetName]

    # activate sheet
    spreadsheetView = self.document.getCurrentController()
    spreadsheetView.setActiveSheet(self.sheet)

    self.numberfmt = self.document.NumberFormats
    self.locale    = self.document.CharLocale

    self.dateFormat = self.numberfmt. \
      getStandardFormat(2, self.locale)

  def write(self) -> None:
    # Start filling cell horizontally
    addr = self.sheet[self.start_cell].CellAddress

    # Fill the cells horizontally
    for col, cat in enumerate(self.categories, start=1):
      col_pos = addr.Column + col

      cell = self.sheet. \
        getCellByPosition(col_pos, addr.Row)
      cell.String = cat

    # Iterate over both index and row data
    row_index = 0
    for date, row in self.pivot_table.iterrows():
      row_index += 1
      row_pos = addr.Row + row_index

      cell = self.sheet. \
        getCellByPosition(addr.Column, row_pos)

      cell.Value = date
      cell.NumberFormat = self.dateFormat

      for col, cat in enumerate(
          self.categories, start=1):

        col_pos = addr.Column + col

        cell = self.sheet. \
          getCellByPosition(col_pos, row_pos)
        cell.Value = int(row[('Number', cat)])

  def process(self) -> None:
    self.prepare_sheet()
    self.write()

