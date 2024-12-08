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

from com.sun.star.\
  table import TableBorder2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabular(FormatterCommon):
  def set_sheetwide_view(self) -> None:
    # activate sheet
    spreadsheetView = self.controller
    spreadsheetView.setActiveSheet(self.sheet)

    # sheet wide
    spreadsheetView.ShowGrid = False
    spreadsheetView.freezeAtPosition(3, 3)

  # Rebuild array of tuple using the helper function
  def get_rows_affected_letter(self):
    return [
      (self.column_index_to_letter(start_col_index + start - 1),
       self.column_index_to_letter(start_col_index + end - 1))
      for metadata in self.metadatas
        # Inline temporary variable
        for start_col_index in [
          self.column_letter_to_index(metadata['col-start'])]
        # Inner loop
        for start, end, *_ in metadata['head-borders']
    ]

  def color_row(self, row) -> None:
    # get cell address value for current row and previous
    col = self.color_group
    value_current = self.sheet[f'{col}{row}'].Value
    value_prev    = self.sheet[f'{col}{row-1}'].Value

    # flip state whenever log index changed
    if (value_current!=value_prev):
      self.color_state = 1 if self.color_state==0 else 0

    if self.color_state == 1:
      # color row based on color_state
      for letter_start, letter_end in self.rows_affected:
        self.sheet[f'{letter_start}{row}:{letter_end}{row}']\
          .CellBackColor = blueScale[0]

  def color_logs(self) -> None:
    # reset color state, flip flop, 0 or 1
    self.color_state = 0

    self.rows_affected = self.get_rows_affected_letter()
    print(f'   {self.rows_affected}')

    for row in range(3, self.max_row+2):
      self.color_row(row)
     
      # Show progress every 5,000 rows
      if (row - 3) % 2500 == 0:
        print(f"   - Processing rows: {row-2}")