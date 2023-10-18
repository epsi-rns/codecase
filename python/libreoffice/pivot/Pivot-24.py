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

class PivotReader:
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
    lookup_cats = ['Date'] + self.categories

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

  def write_row_header(self,
      row_index: int, date: int) -> None:

    # Cell Address
    col_pos = self.addr.Column
    row_pos = self.addr.Row + row_index

    formatted_date = self.get_formatted_date(date)
    print(f"  Date : {formatted_date}")

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

  reader = PivotReader(
    'Example', columns, categories)
  pivot_table = reader.get_pivot()

  # Print the newly created pivot table
  # on terminal console for debugging
  print(pivot_table)
  print()

  writer = PivotWriter(
    'Pivot', pivot_table, categories, 'B2')
  writer.process()
