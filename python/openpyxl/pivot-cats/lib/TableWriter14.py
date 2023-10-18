from pandas import DataFrame

# openPyXL
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import (Color,
  PatternFill, Font, Border, Side, Alignment)

class TableWriter:
  def __init__(self,
      dataframe: DataFrame,
      sheet: Worksheet) -> None:

    # save initial parameter
    self.dataframe = dataframe
    self.sheet = sheet

  def write_column_headers(self) -> None:
    # Access the cell using address

    cell = self.sheet['A1']
    cell.value = 'Number'

    cell = self.sheet['B1']
    cell.value = 'Date'

    cell = self.sheet['C1']
    cell.value = 'Categories'

  def write_rows(self) -> None:
    # Access the cell using indices
    for index, row in self.dataframe.iterrows():
      # Index: Number
      cell = self.sheet.cell(index + 2, 1)
      cell.value = row['Number']

      # Date: Date
      cell = self.sheet.cell(index + 2, 2)
      cell.value = row['Date']

      # Categories: Fruit
      cell = self.sheet.cell(index + 2, 3)
      cell.value = row['Fruit']

  def process(self) -> None:
    self.write_column_headers()
    self.write_rows()
