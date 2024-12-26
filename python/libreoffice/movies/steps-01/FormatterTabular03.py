from abc import abstractmethod
from com.sun.star.sheet import XSpreadsheetDocument

class FormatterBase(ABC):
  def __init__(self, document: XSpreadsheetDocument) -> None:
    self.__document = document
    self._sheet = None
    self._controller = self.__document.getCurrentController()

  @abstractmethod
  def _reset_pos_columns(self) -> None:
    pass

  @abstractmethod
  def _set_sheetwide_view(self) -> None:
    pass

  # Sheet Helper
  # To be used only within the formatOneSheet(), reset_pos_rows()
  def __get_last_used_row(self) -> int:
    cursor = self._sheet.createCursor()
    cursor.gotoEndOfUsedArea(False)
    cursor.gotoStartOfUsedArea(True)
    rows = cursor.getRows()
    
    return len(rows)

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

  # Sheet Helper
  # To be used only within the formatOneSheet()
  def __is_first_column_empty(self) -> bool:
    rows = self._sheet.Rows
    max_sampling_row = 10

    for row_index in range(max_sampling_row + 1):
      cell = self._sheet.getCellByPosition(0, row_index)
      # Indicates an empty cell
      if cell.String != "": return False
    return True

  # Basic Flow
  def __format_one_sheet(self) -> None:
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

  # Basic Flow
  def process_one(self) -> None:
    self._sheet = self._controller.getActiveSheet()
    self.__format_one_sheet()

  # Basic Flow
  def process_all(self) -> None:
    for sheet in self.__document.Sheets:
      print(sheet.Name)
      self._sheet = sheet
      self.__format_one_sheet()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularMovies(FormatterBase):
  def __init__(self) -> None:
    super().__init__(XSCRIPTCONTEXT.getDocument())

  # Formatting Procedure: Abstract Override
  def _set_sheetwide_view(self) -> None:
    # activate sheet
    spreadsheetView = self._controller
    spreadsheetView.setActiveSheet(self._sheet)

    # sheet wide
    spreadsheetView.ShowGrid = False
    spreadsheetView.freezeAtPosition(2, 3)

  # Formatting Procedure
  def _reset_pos_columns(self) -> None:
    columns = self._sheet.Columns
    column_width_div = 0.5 * 1000  # Width of 0.5 cm

    # Insert one column at the specified indexes
    columns.insertByIndex( 0, 1) # Column A
    columns.insertByIndex( 7, 1) # Column H
    columns.insertByIndex(11, 1) # Column L

    # Set widths for columns A, H
    columns.getByIndex( 0).Width = column_width_div
    columns.getByIndex( 7).Width = column_width_div
    columns.getByIndex(11).Width = column_width_div

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Represent Class in Macro

def tabular_single_movies() -> None:
  tabular = FormatterTabularMovies()
  tabular.process_one()

def tabular_multi_movies() -> None:
  tabular = FormatterTabularMovies()
  tabular.process_all()