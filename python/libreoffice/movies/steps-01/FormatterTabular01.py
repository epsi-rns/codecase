class FormatterBase:
  def __init__(self, document) -> None:
    self.__document = document
    self.controller = self.__document.getCurrentController()

  # Basic Flow
  def __format_one_sheet(self) -> None:
    self._reset_pos_columns()

  # Basic Flow
  def process_one(self) -> None:
    self._sheet = self.controller.getActiveSheet()
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
  movies = FormatterTabularMovies()
  movies.process_one()

def tabular_multi_movies() -> None:
  movies = FormatterTabularMovies()
  movies.process_all()