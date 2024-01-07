import uno
import pandas as pd

from datetime import datetime, timedelta
from typing import Dict, List
from pandas import DataFrame

# Debugging purpose, just in case
from pprint import pprint

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

class TableWriter:
  def __init__(self,
      document    : 'com.sun.star.sheet.SpreadsheetDocument',
      sheetName: str,
      dataframe: DataFrame) -> None:

    # save initial parameter
    self.document = document
    self.dataframe = dataframe
    self.sheetName = sheetName

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

    # sheet wide
    spreadsheetView.ShowGrid = False
    spreadsheetView.freezeAtPosition(1,1)

  def write_column_headers(self) -> None:
    cell = self.sheet['A1']
    cell.String = 'Number'
    cell.CellBackColor = tealScale[0]

    cell = self.sheet['B1']
    cell.String = 'Date'
    cell.CellBackColor = tealScale[1]

    cell = self.sheet['C1']
    cell.String = 'Categories'
    cell.CellBackColor = tealScale[0]

    sCellRange = self.sheet. \
      getCellRangeByName('A1:C1')
    sCellRange.HoriJustify = CENTER # or just 2
    sCellRange.CharWeight = BOLD

    column = self.sheet. \
      getColumns().getByIndex(4). \
      Width = 500

  def write_rows(self) -> None:
    for index, row in self.dataframe.iterrows():
      # Index: Number
      cell = self.sheet. \
        getCellByPosition(0, index + 1)
      cell.Value = row['Number']

      # Date: Date
      cell = self.sheet. \
        getCellByPosition(1, index + 1)
      cell.Value = row['Date']
      cell.NumberFormat = self.dateFormat

      # Categories: Fruit
      cell = self.sheet. \
        getCellByPosition(2, index + 1)
      cell.String = row['Fruit']

  def decorate_border(self) -> None:
    sCellRange = self.sheet.getCellRangeByPosition(
      0, 1, 1, len(self.dataframe))
    sCellRange.RightBorder = self.lineFormat

    sCellRange = self.sheet. \
      getCellRangeByName('A1:C1')
    sCellRange.HoriJustify = CENTER # or just 2
    sCellRange.CharWeight = BOLD
    sCellRange.BottomBorder = self.lineFormat

  def process(self) -> None:
    self.prepare_sheet()

    self.write_column_headers()
    self.write_rows()
    self.decorate_border()

