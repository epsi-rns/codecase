from abc import abstractmethod
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

  # -- -- --

  # Basic Flow
  def __format_one_sheet(self) -> None:
    # Rearranging Columns
    print(' * Rearranging Columns')
    self._reset_pos_columns()

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

    letters = ''
    while index >= 0:
      letters = chr(index % 26 + ord('A')) + letters
      index = index // 26 - 1
    return letters

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

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularData(FormatterCommon):
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
