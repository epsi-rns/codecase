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

class CSVReader:
  def __init__(self, filename: str) -> None:

    # save initial parameter
    self.filename = filename

  def date_ordinal(self, value, format_source):
    # Offset of the date value
    # for the date of 1900-01-00
    offset = 693594

    date_value = datetime.strptime(
                   value, format_source)
    return date_value.toordinal() - offset

  def load_data(self):
    try:
      # Load data into a DataFrame
      self.dataframe = pd.read_csv(self.filename)

      # Define the format of the original date in CSV
      format_source = '%d/%m/%Y'

      # Apply the date_ordinal function
      # to the "Date" column
      self.dataframe['Date'] = self.dataframe['Date'].\
        apply(lambda date: self.date_ordinal(
          date, format_source))

      print("Data:")
      print(self.dataframe)

    except FileNotFoundError:
      print("Error: The file "\
        + f"'{self.filename}' was not found.")
    except Exception as e:
      print("An error occurred "
         + f"while loading data: {e}")

  def process(self) -> None:
    self.load_data()

class TableWriter:
  def __init__(self,
      dataframe: DataFrame,
      sheetPlainName: str) -> None:

    # save initial parameter
    self.dataframe = dataframe
    self.sheetPlainName = sheetPlainName

  def get_number_format(self, format_string):
    nf = self.numberfmt.queryKey(  \
              format_string, self.locale, True)
    if nf == -1:
       nf = self.numberfmt.addNew( \
              format_string, self.locale)
    return nf

  def prepare_sheet(self):
    document   = XSCRIPTCONTEXT.getDocument()
    sheets_dst = document.Sheets

    sheetName = self.sheetPlainName
    if not sheets_dst.hasByName(sheetName):
      sheets_dst.insertNewByName(sheetName, 1)
    self.sheet_dst = sheets_dst[sheetName]

    # activate sheet
    desktop    = XSCRIPTCONTEXT.getDesktop()
    model      = desktop.getCurrentComponent()
    controller = model.getCurrentController()
    controller.setActiveSheet(self.sheet_dst)

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
    controller.freezeAtPosition(1,1)

  def write_column_headers(self) -> None:
    cell = self.sheet_dst['A1']
    cell.String = 'Number'
    cell.CellBackColor = tealScale[0]

    cell = self.sheet_dst['B1']
    cell.String = 'Date'
    cell.CellBackColor = tealScale[1]

    cell = self.sheet_dst['C1']
    cell.String = 'Categories'
    cell.CellBackColor = tealScale[0]

    sCellRange = self.sheet_dst. \
      getCellRangeByName('A1:C1')
    sCellRange.HoriJustify = CENTER # or just 2
    sCellRange.CharWeight = BOLD

    column = self.sheet_dst. \
      getColumns().getByIndex(4). \
      Width = 500

  def write_rows(self) -> None:
    for index, row in self.dataframe.iterrows():
      # Index: Number
      cell = self.sheet_dst. \
        getCellByPosition(0, index + 1)
      cell.Value = row['Number']

      # Date: Date
      cell = self.sheet_dst. \
        getCellByPosition(1, index + 1)
      cell.Value = row['Date']
      cell.NumberFormat = self.dateFormat

      # Categories: Fruit
      cell = self.sheet_dst. \
        getCellByPosition(2, index + 1)
      cell.String = row['Fruit']

  def decorate_border(self) -> None:
    sCellRange = self.sheet_dst.getCellRangeByPosition(
      0, 1, 1, len(self.dataframe))
    sCellRange.RightBorder = self.lineFormat

    sCellRange = self.sheet_dst. \
      getCellRangeByName('A1:C1')
    sCellRange.HoriJustify = CENTER # or just 2
    sCellRange.CharWeight = BOLD
    sCellRange.BottomBorder = self.lineFormat

  def process(self) -> None:
    self.prepare_sheet()

    self.write_column_headers()
    self.write_rows()
    self.decorate_border()

def main() -> None:
  source_path = '/home/epsi/.config/libreoffice/' \
              + '4/user/Scripts/python/Pivot/'
  source_csv  = source_path + 'sample-data.csv'

  csv_reader = CSVReader(source_csv)
  csv_reader.process()
  dataframe = csv_reader.dataframe

  table_writer = TableWriter(dataframe, 'Table')
  table_writer.process()

