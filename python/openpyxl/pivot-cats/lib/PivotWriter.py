from typing import List
from pandas import DataFrame
from datetime import datetime

# openPyXL
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import (Color,
  PatternFill, Font, Border, Side, Alignment)

from openpyxl.utils import (
  get_column_letter, column_index_from_string)
from openpyxl.utils.cell import coordinate_from_string

# Local Library
from lib.BaseWriter import BaseWriter

class PivotWriter(BaseWriter):
  def __init__(self,
      pivot_table: DataFrame,
      sheet: Worksheet,
      categories: List[str],
      start_cell: str) -> None:

    # save initial parameter
    self.pivot_table = pivot_table
    self.sheet = sheet
    self.categories = categories
    self.init_start_cell(start_cell)

    # Get the 'Total' row as a separate variable
    self.total_row = self.pivot_table.loc['Total']

    # Exclude the 'Total' row from the DataFrame
    self.pivot_table = self.pivot_table.drop('Total')

  def init_start_cell(self, start_cell: str) -> None:
    # Split the cell address into column and row parts
    column_letter, row_number = \
      coordinate_from_string(start_cell)

    # Convert the column letter to column index
    self.col1 = column_index_from_string(column_letter)

    # Convert the row number to row index
    self.row1 = int(row_number)

  def write_column_headers(self) -> None:
    # Get the list of catssify values
    lookup_cats = ['Date'] + self.categories + ['Total']

    # column width shortcut
    wscd = self.sheet.column_dimensions
    
    # Fill the cells horizontally
    for col, cat in enumerate(lookup_cats, start=0):

      # calculate position, respect start cell
      col_pos = self.col1 + col
      row_pos = self.row1

      cell = self.sheet.cell(row_pos, col_pos)
      cell.value = cat

      cell.font = self.headerFont
      cell.alignment = self.centerText
      cell.border = self.bottom_border

      if col_pos % 2:
        cell.fill  = self.blueFills[1]
      else:
        cell.fill  = self.blueFills[0]

      # take care of column width by 2.5
      letter = get_column_letter(col_pos)
      wscd[letter].width = 5.1 * 2.5

    # left and right padding
    if self.col1 > 1:
      letter = get_column_letter(self.col1 - 1)
      wscd[letter].width = 5.1 * 0.5

    letter = get_column_letter(
      self.col1 + len(lookup_cats))
    wscd[letter].width = 5.1 * 0.5

    # Set the freeze point to Offset (1,1)
    column_index  = self.col1 + 1
    row_index     = self.row1 + 1
    column_letter = get_column_letter(column_index)
    self.sheet.freeze_panes = \
      f'{column_letter}{row_index}'

  def write_row_header(self,
      row_index: int, date: int) -> None:

    # calculate position, respect start cell
    col_pos = self.col1
    row_pos = self.row1 + row_index

    cell = self.sheet.cell(row_pos, col_pos)
    cell.value = date
    cell.number_format = 'DD-MMM-YY;@'

    cell.font      = self.normalFont
    cell.alignment = self.centerText
    cell.border    = self.right_border
    cell.fill      = self.blueFills[0]

  def write_row_content(self,
      row_index: int, row) -> None:

    # calculate position, respect start cell 
    row_pos = self.row1 + row_index

    for col, cat in enumerate(self.categories, start=1):
      if count := int(row[('Number', cat)]):
        col_pos = self.col1 + col
        cell = self.sheet.cell(row_pos, col_pos)

        cell.value = count
        cell.alignment = self.centerText

  def write_row_total(self,
      row_index: int, row) -> None:

    # calculate position, respect start cell 
    len_col = len(self.categories)
    row_pos = self.row1 + row_index
    col_pos = self.col1 + len_col + 1

    cell = self.sheet.cell(row_pos, col_pos)
    cell.value     = int(row['Total'])

    cell.alignment = self.centerText
    cell.border    = self.left_border
    cell.fill      = self.blueFills[0]

  def write_column_total_header(self):
    # calculate position, respect start cell
    len_row = len(self.pivot_table)
    col_pos = self.col1
    row_pos = self.row1 + len_row + 1

    cell = self.sheet.cell(row_pos, col_pos)
    cell.value = 'Total'

    cell.font   = self.headerFont
    cell.border = self.top_border
    cell.fill   = self.blueFills[1]

  def write_column_total_content(self):
    # calculate position, respect start cell
    len_row = len(self.pivot_table)
    row_pos = self.row1 + len_row + 1

    len_row = len(self.pivot_table)
    for col, cat in enumerate(self.categories, start=1):
      col_pos = self.col1 + col
      cell = self.sheet.cell(row_pos, col_pos)
      cell.value = int(self.total_row[('Number', cat)])

      cell.font = self.headerFont
      cell.alignment = self.centerText
      cell.border = self.top_border
      cell.fill  = self.blueFills[0]

  def write_column_total_grand(self):
    # calculate position, respect start cell
    len_col = len(self.categories)
    len_row = len(self.pivot_table)
    col_pos = self.col1 + len_col + 1
    row_pos = self.row1 + len_row + 1

    cell = self.sheet.cell(row_pos, col_pos)
    cell.value = int(self.total_row['Total'])

    cell.font      = self.headerFont
    cell.alignment = self.centerText
    cell.border    = self.top_border
    cell.fill      = self.blueFills[1]

  def write_rows(self) -> None:
    # Fill the rows
    row_index = 0
    for date, row in self.pivot_table.iterrows():
      row_index += 1
      self.write_row_header (row_index, date)
      self.write_row_content(row_index, row)
      self.write_row_total  (row_index, row)

  def write_column_total(self) -> None:
    self.write_column_total_header()
    self.write_column_total_content()
    self.write_column_total_grand()

  def process(self) -> None:
    self.init_sheet_style()

    self.write_column_headers()
    self.write_rows()
    self.write_column_total()
