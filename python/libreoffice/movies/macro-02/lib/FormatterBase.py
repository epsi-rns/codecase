import sys

# Linux Based
lib_path = '/home/epsi/.config/libreoffice/4/user/Scripts/python/Movies'

# Windows Based
# lib_path =  'C:\\Users\\epsir\\AppData\\Roaming\\LibreOffice\\4\\user\\Scripts\\python\\Movies'

# Add the path to the macro
sys.path.append(lib_path)

from lib.BorderFormat import (lfBlack, lfGray, lfNone)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

from abc import ABC, abstractmethod

from com.sun.star.\
  awt.FontWeight import BOLD
from com.sun.star.\
  table.CellHoriJustify import LEFT, CENTER, RIGHT
from com.sun.star.\
  table import TableBorder2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterBase:
  @property
  @abstractmethod
  def document(self): pass

  def __init__(self) -> None:
    self.controller = self.document.getCurrentController()

    self.prepare_sheet()
    self.init_metadatas()
    self.merge_metadatas()

  # Class Property: Sheet Variables
  def prepare_sheet(self):
    # number and date format
    self.numberfmt = self.document.NumberFormats
    self.locale    = self.document.CharLocale

  # -- -- --

  @abstractmethod
  def init_metadatas(self) -> None:
    pass

  @abstractmethod
  def reset_pos_columns(self) -> None:
    pass

  @abstractmethod
  def reset_pos_rows(self) -> None:
    pass

  @abstractmethod
  def set_sheetwide_view(self) -> None:
    pass

  @abstractmethod
  def set_columns_format(self) -> None:
    pass

  @abstractmethod
  def add_merged_titles(self) -> None:
    pass

  @abstractmethod
  def format_head_borders(self) -> None:  
    pass

  @abstractmethod
  def format_head_colors(self) -> None:
    pass

  @abstractmethod
  def format_data_borders(self) -> None:  
    pass

  # -- -- --

  # Basic Flow
  def format_one_sheet(self) -> None:
    self.max_row = self.get_last_used_row()

    if not self.is_first_column_empty():
      # Rearranging Columns
      print(' * Rearranging Columns')
      self.reset_pos_columns()
      print(' * Setting Rows Width')
      self.reset_pos_rows()
      self.max_row += 1

    # Apply Sheet Wide
    print(' * Formatting Columns')
    self.set_sheetwide_view()
    self.set_columns_format()

    # Apply Header Settings
    print(' * Formatting Header')
    self.add_merged_titles()
    self.format_head_borders()
    self.format_head_colors()

    # Apply borders to the specified range
    print(' * Formatting Border')
    self.format_data_borders()

    # Call the hook method (default does nothing)
    self.format_one_sheet_post()

    print(' * Finished')
    print()

  # Basic Flow: Hook
  def format_one_sheet_post(self) -> None:
    """Hook method to be overridden by subclasses if needed."""
    pass

  # Basic Flow
  def process_one(self) -> None:
    self.sheet = self.controller.getActiveSheet()
    self.format_one_sheet()

  # Basic Flow
  def process_all(self) -> None:
    for sheet in self.document.Sheets:
      print(sheet.Name)
      self.sheet = sheet
      self.format_one_sheet()

  # -- -- --

  # Helper: Multiple Usages
  def column_index_to_letter(self, index: int) -> str:
    """Convert a 0-based column index to Excel-style column letters."""
    letters = ''
    while index >= 0:
      letters = chr(index % 26 + ord('A')) + letters
      index = index // 26 - 1
    return letters

  # Helper: Multiple Usages
  def column_letter_to_index(self, column_letter: str) -> int:
    """Convert Excel-style column letters to a 0-based column index."""
    index = 0
    for i, char in enumerate(reversed(column_letter)):
      index += (ord(char) - ord('A') + 1) * (26 ** i)
    return index - 1

  # Helper: Multiple Usages
  def get_relative_column_letter(self, start_letter: str, offset: int) -> str:
    """Get the Excel-style column letter at an offset from the start_letter."""
    start_index    = self.column_letter_to_index(start_letter)
    relative_index = start_index + offset - 1
    return self.column_index_to_letter(relative_index)

  # -- -- --

  # Sheet Helper
  # To be used only within the formatOneSheet(), reset_pos_rows()
  def get_last_used_row(self) -> int:
    cursor = self.sheet.createCursor()
    cursor.gotoEndOfUsedArea(False)
    cursor.gotoStartOfUsedArea(True)
    rows = cursor.getRows()
    
    return len(rows)

  # Sheet Helper
  # To be used only within the formatOneSheet()
  def is_first_column_empty(self) -> bool:
    rows = self.sheet.Rows
    max_sampling_row = 10

    for row_index in range(max_sampling_row + 1):
      cell = self.sheet.getCellByPosition(0, row_index)
      # 0 indicates an empty cell
      if cell.String != "": return False
    return True

  # Sheet Helper
  # To be used only within the set_columns_format()
  def get_number_format(self, format_string):
    nf = self.numberfmt.queryKey(  \
              format_string, self.locale, True)
    if nf == -1:
       nf = self.numberfmt.addNew( \
              format_string, self.locale)
    return nf

  # Sheet Helper: Multiple Usages
  def format_cell_rectangle(self,
        a_t, a_b, a_l, a_r, line_format) -> None:

    func_gcrb = self.sheet.getCellRangeByPosition

    # Formatting Rectangle Edges
    cr_top = func_gcrb(a_l, a_t, a_r, a_t)
    cr_top.TopBorder       = line_format

    cr_bottom = func_gcrb(a_l, a_b, a_r, a_b)
    cr_bottom.BottomBorder = line_format
    
    cr_left = func_gcrb(a_l, a_t, a_l, a_b)
    cr_left.LeftBorder     = line_format

    cr_right = func_gcrb(a_r, a_t, a_r, a_b)
    cr_right.RightBorder   = line_format

    # Formatting Rectangle Corner
    cr_top_left = func_gcrb(a_l, a_t, a_l, a_t)
    cr_top_left.TopBorder        = line_format
    cr_top_left.LeftBorder       = line_format

    cr_top_right = func_gcrb(a_r, a_t, a_r, a_t)
    cr_top_right.TopBorder       = line_format
    cr_top_right.RightBorder     = line_format

    cr_bottom_left = func_gcrb(a_l, a_b, a_l, a_b)
    cr_bottom_left.BottomBorder  = line_format
    cr_bottom_left.LeftBorder    = line_format

    cr_bottom_right = func_gcrb(a_r, a_b, a_r, a_b)
    cr_bottom_right.BottomBorder = line_format
    cr_bottom_right.RightBorder  = line_format

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterCommon(FormatterBase):

  # Formatting Procedure: Abstract Override
  def reset_pos_columns(self) -> None:
    columns = self.sheet.Columns
    column_width_div = 0.5 * 1000  # Width of 0.5 cm

    # Insert column, and set width
    for gap in self.gaps:
      columns.insertByIndex(gap, 1)
      columns.getByIndex(gap).Width  = column_width_div

      letter = self.column_index_to_letter(gap)
      print(f"   - Insert Gap: {letter}")

  # Formatting Procedure: Abstract Override
  def reset_pos_rows(self) -> None:
    rows = self.sheet.Rows
    row_height = 0.5 * 1000  # Height of 0.5 cm

    # Range to be processed
    # Omit header and plus one for the last
    range_rows = range(2, self.max_row + 1)

    for row_index in range_rows:
      rows.getByIndex(row_index).Height = row_height

    # Insert one row at the specified indexes
    rows.insertByIndex(0, 2)  # Row 0

    row_height_div = 0.3 * 1000  # Height of 0.3 cm
    rows.getByIndex(0).Height = row_height_div
    rows.getByIndex(self.max_row + 2).Height = row_height_div

  # Formatting Procedure: Abstract Override
  def set_columns_format(self) -> None:
    columns = self.sheet.Columns

    # Alignment mapping
    alignment_map = {
        'left'  : LEFT,  'center': CENTER, 'right' : RIGHT }

    for metadata in self.metadatas:
      start_letter = metadata['col-start']

      pairs = metadata['fields'].items()
      for pair_index, (field, data) in enumerate(pairs, start=1):
        letter = self.get_relative_column_letter(
          start_letter, pair_index)
        width  = data['width'] * 1000
        align  = data.get('align')

        col_index = self.column_letter_to_index(letter)
        column = columns.getByIndex(col_index)
        column.Width = width

        start_row = 3
        end_row = self.max_row
        cell_range = self.sheet.getCellRangeByPosition(
          col_index, start_row, col_index, end_row)

        if align in alignment_map:
           cell_range.HoriJustify = alignment_map[align]

        if cell_format := data.get('format'):
           cell_range.NumberFormat = self.get_number_format(cell_format)

  # Formatting Procedure: Refactored from add_merged_titles()
  def set_merged_title(self, metadata) -> None:
    start_letter = metadata['col-start']

    for title in metadata['titles']:
      col_letter_start = self.get_relative_column_letter(
          start_letter, title['col-start-id'])  
      col_letter_end   = self.get_relative_column_letter(
          start_letter, title['col-end-id'])

      cell = self.sheet[f"{col_letter_start}2"]
      cell.String        = title['text']
      cell.CellBackColor = title['bg']
      cell.CharColor     = title['fg']

      pos = self.column_letter_to_index(col_letter_start)
      self.format_cell_rectangle(
        1, 1, pos, pos, lfBlack)

      merge_address = f"{col_letter_start}2:{col_letter_end}2"
      self.sheet[merge_address].merge(True)
      self.sheet[merge_address].CharWeight = BOLD

      header_address = f"{col_letter_start}2:{col_letter_end}3"
      self.sheet[header_address].HoriJustify = CENTER

  # Formatting Procedure: Abstract Override
  def add_merged_titles(self) -> None:
    self.sheet['B2:BC3'].HoriJustify = CENTER
    self.sheet['B2:BC2'].CharWeight  = BOLD 

    for metadata in self.metadatas:
      self.set_merged_title(metadata)

    # Call the hook method (default does nothing)
    self.add_merged_titles_post()

  # Formatting Procedure: Hook
  def add_merged_titles_post(self) -> None:
    """Hook method to be overridden by subclasses if needed."""
    pass

  # Formatting Procedure: Abstract Override
  def format_head_borders(self) -> None:
    for metadata in self.metadatas:
      start_letter = metadata['col-start']

      for border_config in metadata['head-borders']:
        col_start_id, col_end_id, outer_line, vert_line = border_config

        letter_start = self.get_relative_column_letter(
          start_letter, col_start_id)  
        letter_end   = self.get_relative_column_letter(
          start_letter, col_end_id)

        self.apply_head_border(
          letter_start, letter_end, outer_line, vert_line)

  # Formatting Procedure: Abstract Override
  def format_head_colors(self) -> None:
    for metadata in self.metadatas:
      start_letter = metadata['col-start']
      start_index  = self.column_letter_to_index(start_letter)

      pairs = metadata['fields'].items()
      for pair_index, (field, data) in enumerate(pairs, start=1):
        if bg_color := data.get('bg'): 
          row_index = 2
          col_index = start_index + pair_index - 1

          cell = self.sheet.getCellByPosition(
            col_index , row_index)
          cell.CellBackColor = bg_color 

  # Formatting Procedure: Abstract Override
  def format_data_borders(self) -> None:
    for metadata in self.metadatas:
      start_letter = metadata['col-start']

      for border_config in metadata['data-borders']:
        col_start_id, col_end_id, \
        outer_line, vert_line, horz_line = border_config

        letter_start = self.get_relative_column_letter(
          start_letter, col_start_id)  
        letter_end   = self.get_relative_column_letter(
          start_letter, col_end_id)  

        self.apply_data_border(
          letter_start, letter_end,
          outer_line, vert_line, horz_line)

  # -- -- --

  # Sheet Helper
  # To be used only within the apply_head_border()
  def get_head_range(self, letter_start, letter_end):
    # Define the cell range for rows and columns
    head_row = 2
    col_start = self.column_letter_to_index(letter_start)
    col_end   = self.column_letter_to_index(letter_end)

    # Define the cell range for the outer border and vertical lines
    return self.sheet.getCellRangeByPosition(
      col_start, head_row, col_end, head_row)

  # Sheet Helper
  # To be used only within the apply_data_border()
  def get_data_range(self, letter_start, letter_end):
    # Define the cell range for rows and columns
    start_row = 3
    end_row = self.max_row
    col_start = self.column_letter_to_index(letter_start)
    col_end   = self.column_letter_to_index(letter_end)

    # Define the cell range for the outer border and vertical lines
    return self.sheet.getCellRangeByPosition(
      col_start, start_row, col_end, end_row)

  # Sheet Helper
  # To be used only within the apply_head_border()
  def set_head_rectangle(self,
        letter_start, letter_end, line_format) -> None:
    # Define the cell range for rows and columns
    # Top, Bottom (max row), Left, Right
    a_t = 2
    a_b = 2
    a_l = self.column_letter_to_index(letter_start)
    a_r = self.column_letter_to_index(letter_end)

    self.format_cell_rectangle(a_t, a_b, a_l, a_r, line_format)

  # Sheet Helper
  # To be used only within the apply_data_border()
  def set_data_rectangle(self,
        letter_start, letter_end, line_format) -> None:
    # Define the cell range for rows and columns
    # Top, Bottom (max row), Left, Right
    a_t = 3
    a_b = self.max_row
    a_l = self.column_letter_to_index(letter_start)
    a_r = self.column_letter_to_index(letter_end)

    self.format_cell_rectangle(a_t, a_b, a_l, a_r, line_format)

  # Sheet Helper
  # To be used only within the format_head_borders()
  def apply_head_border(self,
        letter_start, letter_end,
        outer_line, vert_line) -> None:
    self.set_head_rectangle(
      letter_start, letter_end, outer_line)

    border = TableBorder2()
    border.IsVerticalLineValid   = True
    border.VerticalLine   = vert_line

    cell_range = self.get_head_range(
      letter_start, letter_end)
    cell_range.TableBorder2 = border

  # Sheet Helper
  # To be used only within the format_data_borders()
  def apply_data_border(self,
        letter_start, letter_end,
        outer_line, vert_line, horz_line) -> None:
    self.set_data_rectangle(
      letter_start, letter_end, outer_line)

    border = TableBorder2()
    border.IsVerticalLineValid   = True
    border.IsHorizontalLineValid = True
    border.VerticalLine   = vert_line
    border.HorizontalLine = horz_line

    cell_range = self.get_data_range(
      letter_start, letter_end)
    cell_range.TableBorder2 = border
