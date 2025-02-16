import sys

# Linux Based
lib_path = '/home/epsi/.config/libreoffice/4/user/Scripts/python/Movies'

# Windows Based
# lib_path =  'C:\\Users\\epsir\\AppData\\Roaming\\LibreOffice\\4\\user\\Scripts\\python\\Movies'

# Add the path to the macro
sys.path.append(lib_path)

from lib.ColorScale import (blueScale, redScale)
from lib.BorderFormat import (lfBlack, lfGray, lfNone)
from lib.FormatterBase import FormatterCommon

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabular(FormatterCommon):
  def _set_sheetwide_view(self) -> None:
    # activate sheet
    spreadsheetView = self._controller
    spreadsheetView.setActiveSheet(self._sheet)

    # sheet wide
    spreadsheetView.ShowGrid = False
    spreadsheetView.freezeAtPosition(3, 3)

  # Rebuild array of tuple using the helper function
  def __get_cols_affected_letter(self):
    return [
      (self._column_index_to_letter(start_col_index + start - 1),
       self._column_index_to_letter(start_col_index + end - 1))
      for metadata in self._metadatas
        # Inline temporary variable
        for start_col_index in [
          self._column_letter_to_index(metadata['col-start'])]
        # Inner loop
        for start, end, *_ in metadata['head-borders']
    ]

  def __color_row(self, row) -> None:
    # get cell address value for current row and previous
    col = self._color_group
    value_current = self._sheet[f'{col}{row}'].Value
    value_prev    = self._sheet[f'{col}{row-1}'].Value

    # flip state whenever log index changed
    if (value_current!=value_prev):
      self._color_state = 1 if self._color_state==0 else 0

    if self._color_state == 1:
      # color row based on color_state
      for letter_start, letter_end in self._cols_affected:
        self._sheet[f'{letter_start}{row}:{letter_end}{row}']\
          .CellBackColor = blueScale[0]

  def _color_groups(self) -> None:
    # reset color state, flip flop, 0 or 1
    self._color_state = 1

    self._cols_affected = self.__get_cols_affected_letter()
    print(f'   {self._cols_affected}')

    for row in range(4, self._max_row+2):
      self.__color_row(row)
     
      # Show progress every 5,000 rows
      if (row - 3) % 2500 == 0:
        print(f"   - Processing rows: {row-2}")
