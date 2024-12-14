from abc import ABC, abstractmethod

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterBase:
  def __init__(self) -> None:
    self.controller = self.document.getCurrentController()
    self.merge_metadatas()

  # -- -- --

  @abstractmethod
  def reset_pos_columns(self) -> None:
    pass

  @abstractmethod
  def reset_pos_rows(self) -> None:
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

  # -- -- --

  # Sheet Helper
  # To be used only within the formatOneSheet(), reset_pos_rows()
  def get_last_used_row(self) -> None:
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

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularData(FormatterCommon):
  def __init__(self) -> None:
    self.document = XSCRIPTCONTEXT.getDocument()
    super().__init__()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularMovies(FormatterTabularData):
  # Merge Configuration
  def merge_metadatas(self) -> None:
    # Columns:   A, H,  L
    self.gaps = [0, 7, 11]

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Represent Class in Macro

def tabular_single_movies() -> None:
  movies = FormatterTabularMovies()
  movies.process_one()

def tabular_multi_movies() -> None:
  movies = FormatterTabularMovies()
  movies.process_all()
