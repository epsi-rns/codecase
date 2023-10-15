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

class PivotSample:
  def __init__(self, source_csv: str,
      categories: List[str]) -> None:

    # save initial parameter
    self.filename = source_csv
    self.categories = categories

  def date_ordinal(self, value, format_source):
    # Offset of the date value
    # for the date of 1900-01-00
    offset = 693594

    date_value = datetime.strptime(
                   value, format_source)
    return date_value.toordinal() - offset

  def load_data(self) -> None:
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

    except FileNotFoundError:
      print("Error: The file "\
        + f"'{self.filename}' was not found.")
    except Exception as e:
      print("An error occurred "
         + f"while loading data: {e}")

  def build_pivot(self) -> None:
    try:
      # Perform pivot operations
      self.pivot_table = self.dataframe.pivot_table(
        index='Date', columns='Fruit',
        aggfunc='count', fill_value=0)

      # Ensure all specified columns are present
      for cat in self.categories:
        if ('Number', cat) not in \
            self.pivot_table.columns:
          self.pivot_table[('Number', cat)] = 0

      # Sort the columns (fruits) in alphabetical order
      self.pivot_table = \
        self.pivot_table.sort_index(axis=1)

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

  def get_dataframe(self) -> None:
    return self.dataframe

  def get_pivot(self) -> None:
    return self.pivot_table

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

    sheetName = self.sheetDestName
    if not sheets_dst.hasByName(sheetName):
      sheets_dst.insertNewByName(sheetName, 1)
    self.sheet_dst = sheets_dst[sheetName]

    # activate sheet
    desktop    = XSCRIPTCONTEXT.getDesktop()
    model      = desktop.getCurrentComponent()
    controller = model.getCurrentController()
    controller.setActiveSheet(self.sheet_dst)

    # Initial Position
    self.addr = self.sheet_dst[self.start_cell].CellAddress

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

      cell = self.sheet_dst. \
        getCellByPosition(col_pos, col_row)

      cell.String = cat
      cell.CharWeight = BOLD
      cell.BottomBorder = self.lineFormat

      if col_pos % 2:
        cell.CellBackColor = tealScale[1]
      else:
        cell.CellBackColor = tealScale[0]

      column = self.sheet_dst. \
        getColumns().getByIndex(col_pos)
      column.Width = 3000

    column = self.sheet_dst. \
      getColumns().getByIndex(0). \
      Width = 500
    column = self.sheet_dst. \
      getColumns().getByIndex(len(lookup_cats) + 1). \
      Width = 500

  def write_row_header(self,
      row_index: int, date: int) -> None:

    # Cell Address
    col_pos = self.addr.Column
    row_pos = self.addr.Row + row_index

    formatted_date = self.get_formatted_date(date)

    cell = self.sheet_dst. \
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

      cell = self.sheet_dst. \
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

    cell = self.sheet_dst. \
      getCellByPosition(col_pos, row_pos)
    cell.Value = int(row['Total'])

    cell.HoriJustify = CENTER # or just 2
    cell.LeftBorder = self.lineFormat
    cell.CellBackColor = tealScale[0]

  def write_column_total_header(self):
    col_pos = self.addr.Column
    row_pos = self.addr.Row \
            + len(self.pivot_table) + 1

    cell = self.sheet_dst. \
      getCellByPosition(col_pos, row_pos)
    cell.String = 'Total'

    cell.CharWeight = BOLD
    cell.TopBorder = self.lineFormat
    cell.CellBackColor = tealScale[1]

  def write_column_total_content(self):
    row_pos = self.addr.Row \
            + len(self.pivot_table) + 1

    # Fill the cells horizontally
    for col, cat in enumerate(self.categories, start=1):
      col_pos = self.addr.Column + col

      cell = self.sheet_dst. \
        getCellByPosition(col_pos, row_pos)
      cell.Value = int(self.total_row[('Number', cat)])

      cell.CharWeight = BOLD
      cell.HoriJustify = CENTER # or just 2
      cell.TopBorder = self.lineFormat
      cell.CellBackColor = tealScale[0]

  def write_column_total_grand(self):
    col_pos = self.addr.Column \
            + len(self.categories) + 1
    row_pos = self.addr.Row \
            + len(self.pivot_table) + 1

    cell = self.sheet_dst. \
      getCellByPosition(col_pos, row_pos)
    cell.Value = int(self.total_row['Total'])

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

  def run(self) -> None:
    self.prepare_sheet()

    self.write_column_headers()
    self.write_rows()
    self.write_column_total()

def main() -> None:
  source_path = '/home/epsi/Coding/pivot-cats/'
  source_csv  = source_path + 'sample_data.csv'

  categories = [
    "Apple", "Banana", "Dragon Fruit",
    "Durian", "Grape", "Mango",
    "Orange", "Strawberry"]

  pivot_sample = PivotSample(source_csv, categories)
  pivot_sample.process()
  dataframe   = pivot_sample.get_dataframe()
  pivot_table = pivot_sample.get_pivot()

  table_writer = TableWriter(dataframe, 'Example')
  table_writer.process()

  # Print the newly created pivot table on console 
  print(pivot_table)
  print()

  writer = PivotWriter(
    'Pivot', pivot_table, categories, 'B2')
  writer.run()
