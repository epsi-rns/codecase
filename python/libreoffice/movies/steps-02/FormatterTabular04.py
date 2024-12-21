from abc import ABC, abstractmethod

from com.sun.star.sheet import XSpreadsheetDocument
from com.sun.star.util  import XNumberFormats

from com.sun.star.\
  table.CellHoriJustify import LEFT, CENTER, RIGHT

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterBase:
  @property
  @abstractmethod
  def _document(self): pass

  def __init__(self) -> None:
    self._sheet = None
    self._controller = self._document.getCurrentController()
    self._gaps = []
    self._metadatas = []

    self.__prepare_sheet()
    self._init_metadatas()
    self._merge_metadatas()

  # Class Property: Sheet Variables
  def __prepare_sheet(self) -> None:
    # number and date format
    self.numberfmt = self._document.NumberFormats
    self.locale    = self._document.CharLocale

  # -- -- --

  @abstractmethod
  def _init_metadatas(self) -> None:
    pass

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

  @abstractmethod
  def __set_columns_format(self) -> None:
    pass

  # -- -- --

  # Basic Flow
  def __format_one_sheet(self) -> None:
    self.max_row = self.__get_last_used_row()

    if not self.__is_first_column_empty():
      # Rearranging Columns
      print(' * Rearranging Columns')
      self._reset_pos_columns()
      print(' * Setting Rows Width')
      self._reset_pos_rows()
      self.max_row += 1

    # Apply Sheet Wide
    print(' * Formatting Columns')
    self._set_sheetwide_view()
    self._set_columns_format()

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
    self.sheet = self._controller.getActiveSheet()
    self.__format_one_sheet()

  # Basic Flow
  def process_all(self) -> None:
    for sheet in self._document.Sheets:
      print(sheet.Name)
      self.sheet = sheet
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

  # Helper: Multiple Usages
  def _column_letter_to_index(self, column_letter: str) -> int:
    """Convert Excel-style column letters to a 0-based column index."""
    index = 0
    for i, char in enumerate(reversed(column_letter)):
      index += (ord(char) - ord('A') + 1) * (26 ** i)
    return index - 1

  # Helper: Multiple Usages
  def _get_relative_column_letter(self, start_letter: str, offset: int) -> str:
    """Get the Excel-style column letter at an offset from the start_letter."""
    start_index    = self._column_letter_to_index(start_letter)
    relative_index = start_index + offset - 1
    return self._column_index_to_letter(relative_index)

  # -- -- --

  # Sheet Helper
  # To be used only within the formatOneSheet(), _reset_pos_rows()
  def __get_last_used_row(self) -> int:
    cursor = self.sheet.createCursor()
    cursor.gotoEndOfUsedArea(False)
    cursor.gotoStartOfUsedArea(True)
    rows = cursor.getRows()
    
    return len(rows)

  # Sheet Helper
  # To be used only within the formatOneSheet()
  def __is_first_column_empty(self) -> bool:
    rows = self.sheet.Rows
    max_sampling_row = 10

    for row_index in range(max_sampling_row + 1):
      cell = self.sheet.getCellByPosition(0, row_index)
      # 0 indicates an empty cell
      if cell.String != "": return False
    return True

  # Sheet Helper
  # To be used only within the _set_columns_format()
  def __get_number_format(self,
        format_string: str) -> XNumberFormats:

    nf = self.numberfmt.queryKey(  \
              format_string, self.locale, True)
    if nf == -1:
       nf = self.numberfmt.addNew( \
              format_string, self.locale)
    return nf

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterCommon(FormatterBase):

  # Formatting Procedure: Abstract Override
  def _reset_pos_columns(self) -> None:
    columns = self.sheet.Columns
    column_width_div = 0.5 * 1000  # Width of 0.5 cm

    # Insert column, and set width
    for gap in self._gaps:
      columns.insertByIndex(gap, 1)
      columns.getByIndex(gap).Width  = column_width_div

      letter = self._column_index_to_letter(gap)
      print(f"   - Insert Gap: {letter}")

  # Formatting Procedure: Abstract Override
  def _reset_pos_rows(self) -> None:
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
  def _set_columns_format(self) -> None:
    columns = self.sheet.Columns

    # Alignment mapping
    alignment_map = {
        'left'  : LEFT,  'center': CENTER, 'right' : RIGHT }

    for metadata in self._metadatas:
      start_letter = metadata['col-start']

      pairs = metadata['fields'].items()
      for pair_index, (field, data) in enumerate(pairs, start=1):
        letter = self._get_relative_column_letter(
          start_letter, pair_index)
        width  = data['width'] * 1000
        align  = data.get('align')

        col_index = self._column_letter_to_index(letter)
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

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabular(FormatterCommon):
  def _set_sheetwide_view(self) -> None:
    # activate sheet
    spreadsheetView = self._controller
    spreadsheetView.setActiveSheet(self.sheet)

    # sheet wide
    spreadsheetView.ShowGrid = False
    spreadsheetView.freezeAtPosition(3, 3)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularData(FormatterTabular):
  @property
  def _document(self) -> XSpreadsheetDocument:
    return XSCRIPTCONTEXT.getDocument()

  # Unified Configuration
  def _init_metadatas(self) -> None:
    self._metadata_movies_base = {
      'fields': {
        'Year'     : { 'width': 1.5, 'align': 'center' },
        'Title'    : { 'width': 6 },
        'Genre'    : { 'width': 3 },
        'Plot'     : { 'width': 6 },
        'Actors'   : { 'width': 6 },
        'Director' : { 'width': 5 }
      }
    }

    self._metadata_movies_additional = {
      'fields': {
        'Rated'    : { 'width': 2,   'align': 'center' },
        'Runtime'  : { 'width': 2.5, 'align': 'center' },
        'Metascore': { 'width': 2,   'align': 'center' }
      }
    }

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularMovies(FormatterTabularData):

  # Merge Configuration
  def _merge_metadatas(self) -> None:
    # Columns:   A, H,  L
    self._gaps = [0, 7, 11]

    self._metadatas = [{
      'col-start'     : 'B',
      **self._metadata_movies_base
    }, {
      'col-start'     : 'I',
      **self._metadata_movies_additional
    }]

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Represent Class in Macro

def tabular_single_movies() -> None:
  movies = FormatterTabularMovies()
  movies.process_one()

def tabular_multi_movies() -> None:
  movies = FormatterTabularMovies()
  movies.process_all()
