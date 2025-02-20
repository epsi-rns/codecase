from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterBase:
    def __init__(self, workbook) -> None:
        self.__workbook = workbook
        self._sheet = None

    # Basic Flow
    def __format_one_sheet(self) -> None:
        self._reset_pos_columns()

    # Basic Flow
    def process_all(self) -> None:
        for sheet in self.__workbook.worksheets:
            print(sheet.title)
            self._sheet: Worksheet = sheet
            self.__format_one_sheet()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularMovies(FormatterBase):
    def _reset_pos_columns(self):
        # Approximate width, inch to cm.
        factor   = 5.1
        width_cm = 0.5

        # Insert columns at A, H, and L
        # (1-based index in openpyxl)
        self._sheet.insert_cols(1)  # Column A
        self._sheet.insert_cols(8)  # Column H
        self._sheet.insert_cols(12) # Column L

        # take care of column width
        wscd = self._sheet.column_dimensions
        for col in ["A", "H", "L"]:
            wscd[col].width = width_cm * factor

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Represent Class in Script

def main() -> None:
    input_xlsx  = '../xlsx/movies_by_year.xlsx'
    output_xlsx = '../xlsx/movies_by_year_formatted.xlsx'

    wb = load_workbook(input_xlsx)
    formatter = FormatterTabularMovies(wb)
    formatter.process_all()
    wb.save(output_xlsx )

if __name__ == "__main__":
    main()
