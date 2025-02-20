import tomli
from abc import ABC, abstractmethod
from openpyxl import load_workbook
from openpyxl.utils import (get_column_letter,
    column_index_from_string)
from openpyxl.styles import Alignment

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterBase(ABC):
    @abstractmethod
    def _init_metadatas(self) -> None:
        pass

    @abstractmethod
    def _merge_metadatas(self) -> None:
        pass

    @abstractmethod
    def _reset_pos_columns(self) -> None:
        pass

    @abstractmethod
    def _reset_pos_rows(self) -> None:
        pass

    @abstractmethod
    def _set_sheetwide_view(self) -> None:
        pass

    @abstractmethod
    def _set_columns_format(self) -> None:
        pass

    def __init__(self, workbook):
        self.__workbook = workbook
        self._sheet = None
        self._gaps = []
        self._max_row = 0
        self._metadatas = []

        self._init_metadatas()
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

        # Apply Sheet Wide
        print(" * Formatting Sheet-Wide View")
        self._set_sheetwide_view()
        print(" * Formatting Columns")
        self._set_columns_format()

        # Call the hook method (default does nothing)
        self._format_one_sheet_post()

        print(" * Finished\n")

    # Basic Flow: Hook
    def _format_one_sheet_post(self) -> None:
        """Hook method to be overridden by subclasses if needed."""
        pass

    # Basic Flow
    def process_all(self) -> None:
        for sheet in self.__workbook.worksheets:
            print(sheet.title)
            self._sheet: Worksheet = sheet
            self.__format_one_sheet()

    # -- -- --

    # Helper: Multiple Usages
    def _get_relative_column_letter(self,
            start_letter: str, offset: int) -> str:

        """Get the column letter at an offset from the start_letter."""
        return get_column_letter(
            column_index_from_string(start_letter) + offset)

    # -- -- --

    # Sheet Helper
    # To be used only within the formatOneSheet()
    def __is_first_column_empty(self) -> bool:
        max_sampling_row = 10

        for row_index in range(1, max_sampling_row+1):
            cell = self._sheet.cell(row_index, 1)
            # indicates an empty cell
            if cell.value is not None:
                return False
        return True

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterCommon(FormatterBase):
    # Formatting Procedure: Abstract Override
    def _reset_pos_columns(self) -> None:
        # take care of column width
        wscd = self._sheet.column_dimensions
        factor   = 5.1
        width_cm = 0.5

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
        self._max_row = self._max_row + 2

        # Adjust header row height
        row_height_div = 0.3 * factor
        wsrd[1].height = row_height_div
        wsrd[self._max_row + 1].height = row_height_div

    # Formatting Procedure: Abstract Override
    def _set_sheetwide_view(self) -> None:
        # Disable gridlines
        self._sheet.sheet_view.showGridLines = False

        # Freeze at position C3 (Column 3, Row 3)
        self._sheet.freeze_panes = self._freeze

    # Sheet Helper
    # To be used only within the _set_columns_format()
    def _apply_cell_format(self, letter: str, data: dict) -> None:
        alignment_map = [
            "left", "center", "right",
            "justify", "general", "fill"]

        for row in range(3, self._max_row + 1):
            cell = self._sheet[f"{letter}{row}"]
            if (alignment := data.get("align")) in alignment_map:
                cell.alignment = Alignment(horizontal=alignment)
            if cell_format := data.get("format"):
                cell.number_format = cell_format

    # Formatting Procedure: Abstract Override
    def _set_columns_format(self) -> None:
        factor = 5.1
        wscd = self._sheet.column_dimensions
        alignment_map = [
            "left", "center", "right",
            "justify", "general", "fill"]

        for metadata in self._metadatas:
            start_letter = metadata["col-start"]

            pairs = metadata['fields'].items()
            for pair_index, (field, data) in enumerate(pairs, start=0):
                letter = self._get_relative_column_letter(
                    start_letter, pair_index)

                # Set column width
                wscd[letter].width = data["width"] * factor

                # Set alignment and format             
                self._apply_cell_format(letter, data)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularData(FormatterCommon):
    # Unified Configuration
    def _init_metadatas(self) -> None:
        self._metadata_movies_base = {
            'fields': {
                'Year'     : { 'width': 1.5, 'align': 'center' },
                'Title'    : { 'width': 6 },
                'Genre'    : { 'width': 3 },
                'Plot'     : { 'width': 6 },
                'Actors'   : { 'width': 6 },
                'Director' : { 'width': 5 }
            }
        }

        self._metadata_movies_additional = {
            'fields': {
                'Rated'    : { 'width': 2,   'align': 'center' },
                'Runtime'  : { 'width': 2.5, 'align': 'center' },
                'Metascore': { 'width': 2,   'align': 'center' }
            }
        }

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularMovies(FormatterTabularData):
    # Merge Configuration
    def _merge_metadatas(self) -> None:
        # Columns:    A, H,  L
        self._gaps = [0, 7, 11]
        self._freeze = "C4"

        self._metadatas = [{
            'col-start'     : 'B',
            **self._metadata_movies_base
        }, {
            'col-start'     : 'I',
            **self._metadata_movies_additional
        }]

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
