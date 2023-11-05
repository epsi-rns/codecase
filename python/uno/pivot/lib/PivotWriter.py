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
      desktop     : 'com.sun.star.frame.XDesktop',
      document    : 'com.sun.star.frame.XModel',
      sheetName   : str,
      pivot_table : pd.DataFrame,
      categories  : List[str],
      start_cell  : str) -> None:

    # save initial parameter
    self.desktop  = desktop
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

    model      = self.desktop.getCurrentComponent()
    controller = model.getCurrentController()
    controller.setActiveSheet(self.sheet)

    # Initial Position
    self.addr = self.sheet[self.start_cell].CellAddress

    # number and date format
    self.numberfmt = model.NumberFormats
    self.locale    = model.CharLocale

    date_format = 'DD-MMM-YY;@'
    self.dateFormat = \
      self.get_number_format(date_format)

    # table border
    lineFormat = BorderLine2()
    lineFormat.LineStyle = BorderLineStyle.SOLID
    lineFormat.LineWidth = 20
    lineFormat.Color = tealScale[9]
    self.lineFormat = lineFormat

    # sheet wide
    controller.ShowGrid = False
    controller.freezeAtPosition(
      self.addr.Column + 1, self.addr.Row + 1)

  def get_formatted_date(self, excel_date) -> None:
    # Convert the number to a datetime object
    # Excel's epoch is two days off from the standard epoch
    excel_epoch = datetime(1899, 12, 30)
    date_obj = excel_epoch + timedelta(days=excel_date)

    # Format the datetime object as 'dd/mm/yyyy'
    return date_obj.strftime('%d/%m/%Y')


  def write_column_headers(self):
    # Get the list of catssify values
    lookup_cats = ['Date'] + self.categories + ['Total']

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

    column = self.sheet. \
      getColumns().getByIndex(0). \
      Width = 500
    column = self.sheet. \
      getColumns().getByIndex(len(lookup_cats) + 1). \
      Width = 500

  def write_row_header(self,
      row_index: int, date: int) -> None:

    # Cell Address
    col_pos = self.addr.Column
    row_pos = self.addr.Row + row_index

    formatted_date = self.get_formatted_date(date)

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

  def write_row_total(self,
      row_index: int, row) -> None:

    # Cell Address
    col_pos = self.addr.Column \
            + len(self.categories) + 1
    row_pos = self.addr.Row + row_index

    cell = self.sheet. \
      getCellByPosition(col_pos, row_pos)
    cell.Value = int(row['Total Date'])

    cell.HoriJustify = CENTER # or just 2
    cell.LeftBorder = self.lineFormat
    cell.CellBackColor = tealScale[0]

  def write_column_total_header(self):
    # calculate position, respect start cell
    col_pos = self.addr.Column
    row_pos = self.addr.Row \
            + len(self.pivot_table) + 1

    cell = self.sheet. \
      getCellByPosition(col_pos, row_pos)
    cell.String = 'Total'

    cell.CharWeight = BOLD
    cell.TopBorder = self.lineFormat
    cell.CellBackColor = tealScale[1]

  def write_column_total_content(self):
    # calculate position, respect start cell
    row_pos = self.addr.Row \
            + len(self.pivot_table) + 1

    # Fill the cells horizontally
    for col, cat in enumerate(self.categories, start=1):
      col_pos = self.addr.Column + col

      cell = self.sheet. \
        getCellByPosition(col_pos, row_pos)
      cell.Value = int(self.total_row[('Number', cat)])

      cell.CharWeight = BOLD
      cell.HoriJustify = CENTER # or just 2
      cell.TopBorder = self.lineFormat
      cell.CellBackColor = tealScale[0]

  def write_column_total_grand(self):
    # calculate position, respect start cell
    col_pos = self.addr.Column \
            + len(self.categories) + 1
    row_pos = self.addr.Row \
            + len(self.pivot_table) + 1

    cell = self.sheet. \
      getCellByPosition(col_pos, row_pos)
    cell.Value = int(self.total_row['Total Date'])

    cell.CharWeight = BOLD
    cell.HoriJustify = CENTER # or just 2
    cell.TopBorder = self.lineFormat
    cell.CellBackColor = tealScale[1]

  def write_rows(self) -> None:
    # Fill the rows
    row_index = 0
    for date, row in self.pivot_table.iterrows():
      row_index += 1
      self.write_row_header(row_index, date)
      self.write_row_content(row_index, row)
      self.write_row_total(row_index, row)

  def write_column_total(self) -> None:
    self.write_column_total_header()
    self.write_column_total_content()
    self.write_column_total_grand()

  def process(self) -> None:
    self.prepare_sheet()

    self.write_column_headers()
    self.write_rows()
    self.write_column_total()

