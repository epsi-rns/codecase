from lib.ColorScale import (blueScale, redScale)
from lib.FormatterBase import FormatterCommon

from openpyxl.styles import (Side, PatternFill)
from openpyxl.utils import (
  get_column_letter, column_index_from_string)

lfNone  = Side(style=None, color=None)
lfBlack = Side(style='thin', color='000000')
lfGray  = Side(style='thin', color='E0E0E0') #gray300

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabular(FormatterCommon):
    # Rebuild array of tuple using the helper function
    def __get_rows_affected_letter(self):
        return [
            (get_column_letter(start_col_index + start - 1),
             get_column_letter(start_col_index + end - 1))
            for metadata in self._metadatas
                # Inline temporary variable
                for start_col_index in [
                    column_index_from_string(metadata['col-start'])]
                # Inner loop
                for start, end, *_ in metadata['head-borders']
        ]

    def __color_row(self, row) -> None:
        # get cell address value for current row and previous
        col = self._color_group
        value_current = self._sheet[f'{col}{row}'].value
        value_prev    = self._sheet[f'{col}{row-1}'].value

        # flip state whenever group value changed
        if (value_current!=value_prev):
            self._color_state = 1 if self._color_state==0 else 0

        if self._color_state == 1:
            # Set background color
            hex_color = f"ff{blueScale[0]:06x}"
            pattern = PatternFill(
                start_color=hex_color,
                end_color=hex_color,
                fill_type='solid')

            # color row based on color_state
            for letter_start, letter_end in self._rows_affected:
                index_start = column_index_from_string(letter_start)
                index_end   = column_index_from_string(letter_end)

                for col in range(index_start, index_end+1):
                    cell = self._sheet.cell(row=row, column=col)
                    cell.fill = pattern

    def _color_groups(self) -> None:
        # reset color state, flip flop, 0 or 1
        self._color_state = 1

        self._rows_affected = self.__get_rows_affected_letter()
        print(f'   {self._rows_affected}')

        for row in range(4, self._max_row):
            self.__color_row(row)
     
            # Show progress every 2,500 rows
            if (row - 3) % 2500 == 0:
                print(f"   - Processing rows: {row-2}")
