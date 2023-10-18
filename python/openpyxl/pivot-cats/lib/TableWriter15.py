from pandas import DataFrame
from datetime import datetime

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

  def init_sheet_style(self):
    self.blueFills = {}  # Dictionary to store PatternFill objects
    blueScale = {
      0: 0xE3F2FD, 1: 0xBBDEFB, 2: 0x90CAF9,
      3: 0x64B5F6, 4: 0x42A5F5, 5: 0x2196F3,
      6: 0x1E88E5, 7: 0x1976D2, 8: 0x1565C0,
      9: 0x0D47A1
    }

    for key, color_value in blueScale.items():
      # Convert the color value to a hexadecimal string
      hex_color = f'ff{color_value:06x}'
      self.blueFills[key] = PatternFill(
        start_color=hex_color,
        end_color=hex_color,
        fill_type='solid')

    self.headerFont = Font(name='Arial', sz='10', bold=True)
    self.normalFont = Font(name='Arial', sz='10')
    self.centerText = Alignment(horizontal='center')
    
    # Define the border style and color
    self.bottom_border = Border(
      bottom=Side(style='thin', color='0D47A1'))
    self.inner_border = Border(
      left=Side(style='thin', color='0D47A1'),
      right=Side(style='thin', color='0D47A1'))

  def write_column_headers(self) -> None:
    # Access the cell using address

    cell = self.sheet['A1']
    cell.value = 'Number'
    cell.fill  = self.blueFills[0]

    cell = self.sheet['B1']
    cell.value = 'Date'
    cell.fill  = self.blueFills[1]

    cell = self.sheet['C1']
    cell.value = 'Categories'
    cell.fill  = self.blueFills[0]

    for index in [0,1,2]:
      cell = self.sheet.cell(1, index + 1)
      cell.font = self.headerFont
      cell.alignment = self.centerText
      cell.border = self.bottom_border

    # take care of column width
    wscd = self.sheet.column_dimensions
    for letter, width in \
        {'B': 2.5, 'C': 2.5, 'D': 0.5}.items():
      wscd[letter].width = 5.1 * width

    # Set the freeze point to B2
    self.sheet.freeze_panes = 'B2'

  def write_rows(self) -> None:
    # Access the cell using indices
    for index, row in self.dataframe.iterrows():
      # Index: Number
      cell = self.sheet.cell(index + 2, 1)
      cell.value = row['Number']
      cell.number_format = '000\.'
      cell.font = self.normalFont
      cell.alignment = self.centerText

      # Date: Date
      cell = self.sheet.cell(index + 2, 2)
      cell.value = \
        datetime.strptime(row['Date'], "%d/%m/%Y")
      cell.number_format = 'DD-MMM-YY;@'
      cell.font = self.normalFont
      cell.alignment = self.centerText
      cell.border = self.inner_border

      # Categories: Fruit
      cell = self.sheet.cell(index + 2, 3)
      cell.value = row['Fruit']
      cell.font = self.normalFont

  def process(self) -> None:
    self.init_sheet_style()

    self.write_column_headers()
    self.write_rows()
