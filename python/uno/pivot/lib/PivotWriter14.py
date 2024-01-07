import uno
import pandas as pd

from datetime import datetime, timedelta
from typing import Dict, List
from pandas import DataFrame

from com.sun.star.\
  awt.FontWeight import BOLD
from com.sun.star.\
  table.CellHoriJustify import CENTER
from com.sun.star.\
  table import BorderLine2, BorderLineStyle

tealScale = {
  0: 0xE0F2F1, 1: 0xB2DFDB, 2: 0x80CBC4,
  3: 0x4DB6AC, 4: 0x26A69A, 5: 0x009688,
  6: 0x00897B, 7: 0x00796B, 8: 0x00695C,
  9: 0x004D40
}

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

  def get_number_format(self, format_string):
    nf = self.numberfmt.queryKey(  \
              format_string, self.locale, True)
    if nf == -1:
       nf = self.numberfmt.addNew( \
              format_string, self.locale)
    return nf

  def prepare_sheet(self):
    sheets = self.document.Sheets

    if not sheets.hasByName(self.sheetName):
      sheets.insertNewByName(self.sheetName, 1)
    self.sheet = sheets[self.sheetName]

    # activate sheet
    spreadsheetView = self.document.getCurrentController()
    spreadsheetView.setActiveSheet(self.sheet)

    # Initial Position
    self.addr = self.sheet[self.start_cell].CellAddress

    # number and date format
    self.numberfmt = self.document.NumberFormats
    self.locale    = self.document.CharLocale

    date_format = 'DD-MMM-YY;@'
    self.dateFormat = \
      self.get_number_format(date_format)

    # table border
    lineFormat = BorderLine2()
    lineFormat.LineStyle = BorderLineStyle.SOLID
    lineFormat.LineWidth = 20
    lineFormat.Color = tealScale[9]
    self.lineFormat = lineFormat

  def get_formatted_date(self, excel_date) -> None:
    # Convert the number to a datetime object
    # Excel's epoch is two days off from the standard epoch
    excel_epoch = datetime(1899, 12, 30)
    date_obj = excel_epoch + timedelta(days=excel_date)

    # Format the datetime object as 'dd/mm/yyyy'
    return date_obj.strftime('%d/%m/%Y')

  def write_column_headers(self):
    # Get the list of catssify values
    lookup_cats = ['Date'] + self.categories

    # Fill the cells horizontally
    for col, cat in enumerate(lookup_cats, start=0):
      col_pos = self.addr.Column + col
      col_row = self.addr.Row

      cell = self.sheet. \
        getCellByPosition(col_pos, col_row)

      cell.String = cat
      cell.CharWeight = BOLD
      cell.BottomBorder = self.lineFormat

      if col_pos % 2:
        cell.CellBackColor = tealScale[1]
      else:
        cell.CellBackColor = tealScale[0]

      column = self.sheet. \
        getColumns().getByIndex(col_pos)
      column.Width = 3000

  def write_row_header(self,
      row_index: int, date: int) -> None:

    # Cell Address
    col_pos = self.addr.Column
    row_pos = self.addr.Row + row_index

    formatted_date = self.get_formatted_date(date)
    print(f"  Date : {formatted_date}")

    cell = self.sheet. \
      getCellByPosition(col_pos, row_pos)
    cell.Value = date

    cell.NumberFormat = self.dateFormat
    cell.HoriJustify = CENTER # or just 2
    cell.RightBorder = self.lineFormat
    cell.CellBackColor = tealScale[0]

  def write_row_content(self,
      row_index: int, row) -> None:

    # Fill the each row
    row_pos = self.addr.Row + row_index
    for col, cat in enumerate(self.categories, start=1):
      col_pos = self.addr.Column + col

      cell = self.sheet. \
        getCellByPosition(col_pos, row_pos)

      if count := int(row[('Number', cat)]):
        cell.Value = count
        cell.HoriJustify = CENTER # or just 2

  def write_rows(self) -> None:
    # Fill the rows
    row_index = 0
    for date, row in self.pivot_table.iterrows():
      row_index += 1
      self.write_row_header(row_index, date)
      self.write_row_content(row_index, row)

  def process(self) -> None:
    self.prepare_sheet()

    self.write_column_headers()
    self.write_rows()

