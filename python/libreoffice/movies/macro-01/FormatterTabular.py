import sys

# Linux Based
lib_path = '/home/epsi/.config/libreoffice/4/user/Scripts/python/Movies'

# Windows Based
# lib_path =  'C:\\Users\\epsir\\AppData\\Roaming\\LibreOffice\\4\\user\\Scripts\\python\\Movies'

# Add the path to the macro
sys.path.append(lib_path)

from FormatterBase import FormatterBase
from ColorScale import (
  clBlack, blueScale, tealScale, amberScale, brownScale)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -

from com.sun.star.\
  awt.FontWeight import BOLD
from com.sun.star.\
  table.CellHoriJustify import CENTER
from com.sun.star.\
  table import BorderLine2, BorderLineStyle, TableBorder2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularMovies(FormatterBase):
  def __init__(self) -> None:
    super().__init__(XSCRIPTCONTEXT.getDocument())

  # Simple Configuration
  def _init_field_metadata(self) -> None:
    self._fields = {
       'Year'     : { 'col': 'B', 'width': 1.5, 'bg': blueScale[3],
                      'align': 'center' },
       'Title'    : { 'col': 'C', 'width': 6,   'bg': blueScale[2] },
       'Genre'    : { 'col': 'D', 'width': 3,   'bg': blueScale[1] },
       'Plot'     : { 'col': 'E', 'width': 6,   'bg': blueScale[2] },
       'Actors'   : { 'col': 'F', 'width': 6,   'bg': blueScale[1] },
       'Director' : { 'col': 'G', 'width': 5,   'bg': blueScale[2] },

       'Rated'    : { 'col': 'I', 'width': 2,   'bg': tealScale[2],
                      'align': 'center' },
       'Runtime'  : { 'col': 'J', 'width': 2.5, 'bg': tealScale[1],
                      'align': 'center' },
       'Metascore': { 'col': 'K', 'width': 2,   'bg': tealScale[2],
                      'align': 'center' }
    }

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

  # Formatting Procedure
  def _add_merged_title(self) -> None:
    self._sheet['B2:K3'].HoriJustify = CENTER
    self._sheet['B2:K2'].CharWeight = BOLD 

    cell = self._sheet['B2']
    cell.String = 'Base Movie Data'
    cell.CellBackColor = blueScale[3]
    cell.CharColor = clBlack
    self._format_cell_rectangle(
      1, 1, 1, 1, self.lfBlack)
    self._sheet['B2:G2'].merge(True)

    cell = self._sheet['I2']
    cell.String = 'Additional'
    cell.CellBackColor = tealScale[3]
    cell.CharColor = clBlack
    self._format_cell_rectangle(
      1, 1, 8, 8, self.lfBlack)
    self._sheet['I2:K2'].merge(True)

  # Formatting Procedure
  def _format_head_borders(self) -> None:  
    # Base Movie Data
    self._apply_head_border(
      'B', 'G', self.lfBlack, self.lfBlack)

    # Additional Data
    self._apply_head_border(
      'I', 'K', self.lfBlack, self.lfBlack)

  # Formatting Procedure
  def _format_data_borders(self) -> None:  
    # Base Movie Data
    self._apply_data_border(
      'B', 'C', self.lfBlack, self.lfBlack, self.lfGray)
    self._apply_data_border(
      'D', 'G', self.lfBlack, self.lfGray, self.lfGray)

    # Additional Data
    self._apply_data_border(
      'I', 'K', self.lfBlack, self.lfGray, self.lfGray)

  # Sheet Helper
  def _color_row(self, row: int) -> None:
    # get cell address value for current row and previous
    value_current = self._sheet[f'B{row}'].Value
    value_prev    = self._sheet[f'B{row-1}'].Value

    # flip state whenever log index changed_
    if (value_current!=value_prev):
      self._color_state = 1 if self._color_state==0 else 0

    if self._color_state == 1:
      # color row based on color_state
      self._sheet[f'B{row}:G{row}'].CellBackColor = blueScale[0]
      self._sheet[f'I{row}:K{row}'].CellBackColor = blueScale[0]

  def _format_one_sheet(self) -> None:
    super()._format_one_sheet() 

    # Additional formatting
    print(f' * Additional Formatting: {self._max_row} rows')
    self._color_groups()

    print(' * Finished')

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Represent Class in Macro

def tabular_single_movies() -> None:
  tabular = FormatterTabularMovies()
  tabular.process_one()

def tabular_multi_movies() -> None:
  tabular = FormatterTabularMovies()
  tabular.process_all()
  