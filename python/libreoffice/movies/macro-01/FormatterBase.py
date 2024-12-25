from abc import ABC, abstractmethod

from com.sun.star.sheet import XSpreadsheetDocument
from com.sun.star.util  import XNumberFormats
from com.sun.star.table import XCellRange

from com.sun.star.\
  awt.FontWeight import BOLD
from com.sun.star.\
  table.CellHoriJustify import LEFT, CENTER, RIGHT
from com.sun.star.\
  table import BorderLine2, BorderLineStyle, TableBorder2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterBase:
  def __init__(self, document: XSpreadsheetDocument) -> None:
    self.__document = document
    self._sheet = None
    self._controller = self.__document.getCurrentController()

    self._fields = {}
    self._init_field_metadata()
    self.__prepare_sheet()

  @abstractmethod
  def _init_field_metadata(self) -> None:
    pass

  @abstractmethod
  def _reset_pos_columns(self) -> None:
    pass

  @abstractmethod
  def _set_sheetwide_view(self) -> None:
    pass

  @abstractmethod
  def _add_merged_title(self) -> None:
    pass

  @abstractmethod
  def _format_head_borders(self) -> None:  
    pass

  @abstractmethod
  def _format_data_borders(self) -> None:  
    pass

  @abstractmethod
  def _color_row(self, row: int) -> None:
    pass

  @abstractmethod
  def _color_groups(self) -> None:
    pass

  # Class Property: Sheet Variables
  def __prepare_sheet(self) -> None:
    # number and date format
    self._numberfmt = self.__document.NumberFormats
    self._locale    = self.__document.CharLocale

    # table border
    lineFormatNone = BorderLine2()
    lineFormatNone.LineStyle = BorderLineStyle.NONE
    self.lfNone= lineFormatNone

    # table border
    lineFormatBlack = BorderLine2()
    lineFormatBlack.LineStyle = BorderLineStyle.SOLID
    lineFormatBlack.LineWidth = 20
    lineFormatBlack.Color = 0x000000 #black
    self.lfBlack = lineFormatBlack

    # table border
    lineFormatGray = BorderLine2()
    lineFormatGray.LineStyle = BorderLineStyle.SOLID
    lineFormatGray.LineWidth = 20
    lineFormatGray.Color = 0xE0E0E0 #gray300
    self.lfGray = lineFormatGray

  # Sheet Helper
  # To be used only within the formatOneSheet(), reset_pos_rows()
  def __get_last_used_row(self) -> int:
    cursor = self._sheet.createCursor()
    cursor.gotoEndOfUsedArea(False)
    cursor.gotoStartOfUsedArea(True)
    rows = cursor.getRows()
    
    return len(rows)

  # Sheet Helper
  # To be used only within the __set_columns_format()
  def __get_number_format(self,
        format_string: str) -> XNumberFormats:

    nf = self._numberfmt.queryKey(  \
              format_string, self._locale, True)
    if nf == -1:
       nf = self._numberfmt.addNew( \
              format_string, self._locale)
    return nf

  # Formatting Procedure
  def __reset_pos_rows(self) -> None:
    rows = self._sheet.Rows
    row_height = 0.5 * 1000  # Height of 0.5 cm

    # Range to be processed
    # Omit header and plus one for the last
    range_rows = range(2, self._max_row + 1)

    for row_index in range_rows:
      rows.getByIndex(row_index).Height = row_height

    # Insert one row at the specified indexes
    rows.insertByIndex(0, 2)  # Row 0

    row_height_div = 0.3 * 1000  # Height of 0.3 cm
    rows.getByIndex(0).Height = row_height_div
    rows.getByIndex(self._max_row + 2).Height = row_height_div

  # To be used only within the formatOneSheet()
  def __is_first_column_empty(self) -> bool:
    rows = self._sheet.Rows
    max_sampling_row = 10

    for row_index in range(max_sampling_row + 1):
      cell = self._sheet.getCellByPosition(0, row_index)
      # Indicates an empty cell
      if cell.String != "": return False
    return True

  # Helper: Multiple Usages
  def _column_letter_to_index(self, column_letter) -> None:
    index = 0
    for i, char in enumerate(reversed(column_letter)):
      index += (ord(char) - ord('A') + 1) * (26 ** i)
    return index - 1  # Convert to 0-based index

  # Sheet Helper
  # To be used only within the apply_head_border()
  def __get_head_range(self,
        letter_start: str, letter_end:  str) -> XCellRange:

    # Define the cell range for rows and columns
    head_row = 2
    col_start = self._column_letter_to_index(letter_start)
    col_end   = self._column_letter_to_index(letter_end)

    # Define the cell range for the outer border and vertical lines
    return self._sheet.getCellRangeByPosition(
      col_start, head_row, col_end, head_row)

  # Sheet Helper
  # To be used only within the apply_data_border()
  def __get_data_range(self,
        letter_start: str, letter_end:  str) -> XCellRange:

    # Define the cell range for rows and columns
    start_row = 3
    end_row = self._max_row
    col_start = self._column_letter_to_index(letter_start)
    col_end   = self._column_letter_to_index(letter_end)

    # Define the cell range for the outer border and vertical lines
    return self._sheet.getCellRangeByPosition(
      col_start, start_row, col_end, end_row)

  # Helper: Multiple Usages
  def _format_cell_rectangle(self,
        a_t: int, a_b: int, a_l: int, a_r: int,
        line_format: BorderLine2) -> None:

    func_gcrb = self._sheet.getCellRangeByPosition

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

  # Sheet Helper
  # To be used only within the apply_head_border()
  def __set_head_rectangle(self,
        letter_start: str, letter_end: str,
        line_format: BorderLine2) -> None:

    # Define the cell range for rows and columns  
    # Top, Bottom (max row), Left, Right
    a_t = 2
    a_b = 2
    a_l = self._column_letter_to_index(letter_start)
    a_r = self._column_letter_to_index(letter_end)

    self._format_cell_rectangle(a_t, a_b, a_l, a_r, line_format)

  # Sheet Helper
  # To be used only within the apply_data_border()
  def __set_data_rectangle(self,
        letter_start: str, letter_end: str,
        line_format: BorderLine2) -> None:

    # Define the cell range for rows and columns  
    # Top, Bottom (max row), Left, Right
    a_t = 3  
    a_b = self._max_row
    a_l = self._column_letter_to_index(letter_start)
    a_r = self._column_letter_to_index(letter_end)

    self._format_cell_rectangle(a_t, a_b, a_l, a_r, line_format)

  # Sheet Helper
  # To be used only within the format_head_borders()
  def _apply_head_border(self,
        letter_start: str, letter_end: str,
        outer_line: BorderLine2, vert_line: BorderLine2) -> None:

    # Border Outside: Edges and Corner
    self.__set_head_rectangle(
      letter_start, letter_end, outer_line)

    # Border Inside: Vertical only
    border = TableBorder2()
    border.IsVerticalLineValid = True
    border.VerticalLine = vert_line

    cell_range = self.__get_head_range(
      letter_start, letter_end)
    cell_range.TableBorder2 = border

  # Sheet Helper
  # To be used only within the format_data_borders()
  def _apply_data_border(self,
        letter_start: str, letter_end: str,
        outer_line: BorderLine2, vert_line: BorderLine2,
        horz_line: BorderLine2) -> None:

    # Border Outside: Edges and Corner
    self.__set_data_rectangle(
      letter_start, letter_end, outer_line)

    # Border Inside: Vertical and Horizontal
    border = TableBorder2()
    border.IsVerticalLineValid   = True
    border.IsHorizontalLineValid = True
    border.VerticalLine   = vert_line
    border.HorizontalLine = horz_line

    cell_range = self.__get_data_range(
      letter_start, letter_end)
    cell_range.TableBorder2 = border

  # Formatting Procedure
  def __set_columns_format(self) -> None:
    columns = self._sheet.Columns

    # Alignment mapping
    alignment_map = {
        'left'  : LEFT,  'center': CENTER, 'right' : RIGHT }

    for field, data in self._fields.items():
      letter = data['col']
      width  = data['width'] * 1000
      align  = data.get('align')

      col_index = self._column_letter_to_index(letter)
      column = columns.getByIndex(col_index)
      column.Width = width

      start_row = 3
      end_row = self._max_row
      cell_range = self._sheet.getCellRangeByPosition(
        col_index, start_row, col_index, end_row)

      if align in alignment_map:
         cell_range.HoriJustify = alignment_map[align]

      if cell_format := data.get('format'):
         cell_range.NumberFormat = self.__get_number_format(cell_format)

  # Formatting Procedure
  def _format_head_colors(self) -> None:  
    for field, data in self._fields.items():
      if bg_color := data.get('bg'):
        letter = data['col']      
        row_index = 2
        col_index = self._column_letter_to_index(letter)

        cell = self._sheet.getCellByPosition(
          col_index , row_index)
        cell.CellBackColor = bg_color 

  # Formatting Procedure
  def _color_groups(self) -> None:
    # reset color state, flip flop, 0 or 1
    self._color_state = 1

    for row in range(4, self._max_row+2):
      self._color_row(row)
     
      # Show progress every 5,000 rows
      if (row - 3) % 2500 == 0:
          print(f"   - Processing rows: {row-2}")

  # Basic Flow
  def _format_one_sheet(self) -> None:
    self._max_row = self.__get_last_used_row()

    if not self.__is_first_column_empty():
      # Rearranging Columns
      print(' * Rearranging Columns')
      self._reset_pos_columns()
      self.__reset_pos_rows()
      self._max_row += 1

    # Apply Sheet Wide
    print(' * Formatting Columns')
    self._set_sheetwide_view()
    self.__set_columns_format()

    # Apply Header Settings
    print(' * Formatting Header')
    self._add_merged_title()
    self._format_head_borders()
    self._format_head_colors()

    # Apply borders to the specified range
    print(' * Formatting Border')
    self._format_data_borders()

  # Basic Flow
  def process_one(self) -> None:
    self._sheet = self._controller.getActiveSheet()
    self._format_one_sheet()

  # Basic Flow
  def process_all(self) -> None:
    for sheet in self.__document.Sheets:
      print(sheet.Name)
      self._sheet = sheet
      self._format_one_sheet()
