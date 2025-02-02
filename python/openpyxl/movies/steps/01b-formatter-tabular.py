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

    def __init__(self, workbook):
        self._workbook = workbook
        self._sheet = None
        self._gaps = []

        self._merge_metadatas()

    # -- -- --

    # Basic Flow
    def __format_one_sheet(self) -> None:
        print(" * Rearranging Columns")
        self._reset_pos_columns()

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

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterCommon(FormatterBase):
    # Formatting Procedure: Abstract Override
    def _reset_pos_columns(self) -> None:
        factor = 5.1
        width_cm = 0.5

        # take care of column width
        wscd = self._sheet.column_dimensions
        for gap in self._gaps:
            letter = get_column_letter(gap + 1)

            # Insert a column
            self._sheet.insert_cols(gap + 1)
            wscd[letter].width = width_cm * factor

            print(f"   - Insert Gap: {letter}")

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
