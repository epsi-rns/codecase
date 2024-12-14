from abc import ABC, abstractmethod

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterBase:
  @property
  @abstractmethod
  def document(self): pass

  def __init__(self) -> None:
    self.controller = self.document.getCurrentController()
    self.merge_metadatas()

  # -- -- --

  @abstractmethod
  def reset_pos_columns(self) -> None:
    pass

  # -- -- --

  # Basic Flow
  def format_one_sheet(self) -> None:
    # Rearranging Columns
    print(' * Rearranging Columns')
    self.reset_pos_columns()

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

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularData(FormatterCommon):
  @property
  def document(self): return XSCRIPTCONTEXT.getDocument()

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
