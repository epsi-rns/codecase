import tomli
from abc import ABC, abstractmethod
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterBase(ABC):
    @abstractmethod
    def _merge_metadatas(self) -> None:
        pass

    @abstractmethod
    def _reset_pos_columns(self) -> None:
        pass

    @abstractmethod
    def _reset_pos_rows(self) -> None:
        pass

    def __init__(self, workbook):
        self._workbook = workbook
        self._sheet = None
        self._gaps = []
        self._max_row = 0

        self._merge_metadatas()

    # -- -- --

    # Basic Flow
    def __format_one_sheet(self) -> None:
        self._max_row = self._sheet.max_row

        if not self.__is_first_column_empty():
            print(" * Rearranging Columns")
            self._reset_pos_columns()
            print(" * Setting Rows Height")
            self._reset_pos_rows()
            self._max_row += 1

        # Call the hook method (default does nothing)
        self._format_one_sheet_post()

        print(" * Finished\n")

    # Basic Flow: Hook
    def _format_one_sheet_post(self) -> None:
        """Hook method to be overridden by subclasses if needed."""
        pass

    # Basic Flow
    def process_all(self) -> None:
        for sheet in self._workbook.worksheets:
            print(sheet.title)
            self._sheet = sheet
            self.__format_one_sheet()

    # -- -- --

    # Sheet Helper
    # To be used only within the formatOneSheet()
    def __is_first_column_empty(self) -> bool:
        max_sampling_row = 10

        for row_index in range(1, max_sampling_row+1):
            cell = self._sheet.cell(row_index, 1)
            # indicates an empty cell
            if cell.value != None: return False
        return True

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterCommon(FormatterBase):
    # Formatting Procedure: Abstract Override
    def _reset_pos_columns(self) -> None:
        factor = 5.1
        width_cm = 0.5
        wscd = self._sheet.column_dimensions

        for gap in self._gaps:
            letter = get_column_letter(gap + 1)

            # Insert a column
            self._sheet.insert_cols(gap + 1)
            wscd[letter].width = width_cm * factor

            print(f"   - Insert Gap: {letter}")

    # Formatting Procedure: Abstract Override
    def _reset_pos_rows(self) -> None:
        # Approx. conversion of cm row height
        factor = 29.53
        row_height = 0.5 * factor
        wsrd = self._sheet.row_dimensions

        # Range to be processed
        # Omit header and plus one for the last
        range_rows = range(2, self._max_row + 1)

        for row_index in range_rows :
            wsrd[row_index].height = row_height

        # Insert two rows at the top
        self._sheet.insert_rows(1, 2)

        # Adjust header row height
        row_height_div = 0.3 * factor
        wsrd[1].height = row_height_div
        wsrd[self._max_row + 2].height = row_height_div

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularMovies(FormatterCommon):
    # Merge Configuration
    def _merge_metadatas(self) -> None:
        # Columns:    A, H,  L
        self._gaps = [0, 7, 11]

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

def main() -> None:
    input_xlsx  = "../xlsx/movies_by_year.xlsx"
    output_xlsx = "../xlsx/movies_by_year_formatted.xlsx"

    wb = load_workbook(input_xlsx)
    formatter = FormatterTabularMovies(wb)
    formatter.process_all()
    wb.save(output_xlsx)

if __name__ == "__main__":
    main()
