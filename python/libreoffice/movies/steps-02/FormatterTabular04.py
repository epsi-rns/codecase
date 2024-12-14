from abc import ABC, abstractmethod

from com.sun.star.\
  table.CellHoriJustify import LEFT, CENTER, RIGHT

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Google Material Color Scale 
blueScale = {
  0: 0xE3F2FD, 1: 0xBBDEFB, 2: 0x90CAF9,
  3: 0x64B5F6, 4: 0x42A5F5, 5: 0x2196F3,
  6: 0x1E88E5, 7: 0x1976D2, 8: 0x1565C0,
  9: 0x0D47A1
}

tealScale = {
  0: 0xE0F2F1, 1: 0xB2DFDB, 2: 0x80CBC4,
  3: 0x4DB6AC, 4: 0x26A69A, 5: 0x009688,
  6: 0x00897B, 7: 0x00796B, 8: 0x00695C,
  9: 0x004D40
}

amberScale = {
  0: 0xFFF8E1, 1: 0xFFECB3, 2: 0xFFE082,
  3: 0xFFD54F, 4: 0xFFCA28, 5: 0xFFC107,
  6: 0xFFB300, 7: 0xFFA000, 8: 0xFF8F00,
  9: 0xFF6F00
}

brownScale = {
  0: 0xEFEBE9, 1: 0xD7CCC8, 2: 0xBCAAA4,
  3: 0xA1887F, 4: 0x8D6E63, 5: 0x795548,
  6: 0x6D4C41, 7: 0x5D4037, 8: 0x4E342E,
  9: 0x3E2723
}

redScale = {
  0: 0xffebee, 1: 0xffcdd2, 2: 0xef9a9a,
  3: 0xe57373, 4: 0xef5350, 5: 0xf44336,
  6: 0xe53935, 7: 0xd32f2f, 8: 0xc62828,
  9: 0xb71c1c
}

clBlack = 0x000000

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

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabular(FormatterCommon):
  def set_sheetwide_view(self) -> None:
    # activate sheet
    spreadsheetView = self.controller
    spreadsheetView.setActiveSheet(self.sheet)

    # sheet wide
    spreadsheetView.ShowGrid = False
    spreadsheetView.freezeAtPosition(3, 3)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularData(FormatterTabular):
  @property
  def document(self): return XSCRIPTCONTEXT.getDocument()

  # Unified Configuration
  def init_metadatas(self) -> None:
    self.metadata_movies_base = {
      'fields': {
        'Year'     : { 'width': 1.5, 'bg': blueScale[3],
                       'align': 'center' },
        'Title'    : { 'width': 6,   'bg': blueScale[2] },
        'Genre'    : { 'width': 3,   'bg': blueScale[1] },
        'Plot'     : { 'width': 6,   'bg': blueScale[2] },
        'Actors'   : { 'width': 6,   'bg': blueScale[1] },
        'Director' : { 'width': 5,   'bg': blueScale[2] }
      }
    }

    self.metadata_movies_additional = {
      'fields': {
        'Rated'    : { 'width': 2,   'bg': tealScale[2],
                       'align': 'center' },
        'Runtime'  : { 'width': 2.5, 'bg': tealScale[1],
                       'align': 'center' },
        'Metascore': { 'width': 2,   'bg': tealScale[2],
                       'align': 'center' }
      }
    }

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularMovies(FormatterTabularData):

  # Merge Configuration
  def merge_metadatas(self) -> None:
    # Columns:   A, H,  L
    self.gaps = [0, 7, 11]

    self.metadatas = [{
      'col-start'     : 'B',
      **self.metadata_movies_base
    }, {
      'col-start'     : 'I',
      **self.metadata_movies_additional
    }]

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Represent Class in Macro

def tabular_single_movies() -> None:
  movies = FormatterTabularMovies()
  movies.process_one()

def tabular_multi_movies() -> None:
  movies = FormatterTabularMovies()
  movies.process_all()
