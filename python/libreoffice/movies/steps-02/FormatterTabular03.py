from abc import ABC, abstractmethod
from com.sun.star.sheet import XSpreadsheetDocument

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterBase(ABC):
  @property
  @abstractmethod
  def _document(self) -> XSpreadsheetDocument:
    pass

  def __init__(self) -> None:
    self._sheet = None
    self._controller = self._document.getCurrentController()
    self._gaps = []

    self._merge_metadatas()

  # -- -- --

  @abstractmethod
  def _merge_metadatas(self) -> None:
    pass

  @abstractmethod
  def _reset_pos_columns(self) -> None:
    pass

  @abstractmethod
  def _reset_pos_rows(self) -> None:
    pass

  @abstractmethod
  def _set_sheetwide_view(self) -> None:
    pass

  # -- -- --

  # Basic Flow
  def __format_one_sheet(self) -> None:
    self._max_row = self.__get_last_used_row()

    if not self.__is_first_column_empty():
      # Rearranging Columns
      print(' * Rearranging Columns')
      self._reset_pos_columns()
      print(' * Setting Rows Width')
      self._reset_pos_rows()
      self._max_row += 1

    # Apply Sheet Wide
    print(' * Formatting Columns')
    self._set_sheetwide_view()

    # Call the hook method (default does nothing)
    self._format_one_sheet_post()

    print(' * Finished')
    print()

  # Basic Flow: Hook
  def _format_one_sheet_post(self) -> None:
    """Hook method to be overridden by subclasses if needed."""
    pass

  # Basic Flow
  def process_one(self) -> None:
    self._sheet = self._controller.getActiveSheet()
    self.__format_one_sheet()

  # Basic Flow
  def process_all(self) -> None:
    for sheet in self._document.Sheets:
      print(sheet.Name)
      self._sheet = sheet
      self.__format_one_sheet()

  # -- -- --

  # Helper: Multiple Usages
  def _column_index_to_letter(self, index: int) -> str:
    """Convert a 0-based column index to Excel-style column letters."""
    letters = ''
    while index >= 0:
      letters = chr(index % 26 + ord('A')) + letters
      index = index // 26 - 1
    return letters

  # -- -- --

  # Sheet Helper
  # To be used only within the formatOneSheet(), _reset_pos_rows()
  def __get_last_used_row(self) -> int:
    cursor = self._sheet.createCursor()
    cursor.gotoEndOfUsedArea(False)
    cursor.gotoStartOfUsedArea(True)
    rows = cursor.getRows()
    
    return len(rows)

  # Sheet Helper
  # To be used only within the formatOneSheet()
  def __is_first_column_empty(self) -> bool:
    rows = self._sheet.Rows
    max_sampling_row = 10

    for row_index in range(max_sampling_row + 1):
      cell = self._sheet.getCellByPosition(0, row_index)
      # indicates an empty cell
      if cell.String != "": return False
    return True

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterCommon(FormatterBase):

  # Formatting Procedure: Abstract Override
  def _reset_pos_columns(self) -> None:
    columns = self._sheet.Columns
    column_width_div = 0.5 * 1000  # Width of 0.5 cm

    # Insert column, and set width
    for gap in self._gaps:
      columns.insertByIndex(gap, 1)
      columns.getByIndex(gap).Width  = column_width_div

      letter = self._column_index_to_letter(gap)
      print(f"   - Insert Gap: {letter}")

  # Formatting Procedure: Abstract Override
  def _reset_pos_rows(self) -> None:
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

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabular(FormatterCommon):
  def _set_sheetwide_view(self) -> None:
    # activate sheet
    spreadsheetView = self._controller
    spreadsheetView.setActiveSheet(self._sheet)

    # sheet wide
    spreadsheetView.ShowGrid = False
    spreadsheetView.freezeAtPosition(3, 3)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularData(FormatterTabular):
  @property
  def _document(self) -> XSpreadsheetDocument:
    return XSCRIPTCONTEXT.getDocument()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularMovies(FormatterTabularData):
  # Merge Configuration
  def _merge_metadatas(self) -> None:
    # Columns:   A, H,  L
    self._gaps = [0, 7, 11]

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Represent Class in Macro

def tabular_single_movies() -> None:
  movies = FormatterTabularMovies()
  movies.process_one()

def tabular_multi_movies() -> None:
  movies = FormatterTabularMovies()
  movies.process_all()
