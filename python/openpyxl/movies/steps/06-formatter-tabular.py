import toml

from abc import ABC, abstractmethod

from openpyxl import (Workbook, load_workbook)
from openpyxl.styles import (Font,
  Alignment, Border, Side, PatternFill)

from openpyxl.utils import (
  get_column_letter, column_index_from_string)
from openpyxl.utils.cell import coordinate_from_string

lfNone  = Side(style=None, color=None)
lfBlack = Side(style='thin', color='000000')
lfGray  = Side(style='thin', color='E0E0E0') #gray300

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Google Material Color Scale 
blueScale = {
    0: 0xE3F2FD, 1: 0xBBDEFB, 2: 0x90CAF9,
    3: 0x64B5F6, 4: 0x42A5F5, 5: 0x2196F3,
    6: 0x1E88E5, 7: 0x1976D2, 8: 0x1565C0,
    9: 0x0D47A1
}

tealScale = {
    0: 0xE0F2F1, 1: 0xB2DFDB, 2: 0x80CBC4,
    3: 0x4DB6AC, 4: 0x26A69A, 5: 0x009688,
    6: 0x00897B, 7: 0x00796B, 8: 0x00695C,
    9: 0x004D40
}

amberScale = {
    0: 0xFFF8E1, 1: 0xFFECB3, 2: 0xFFE082,
    3: 0xFFD54F, 4: 0xFFCA28, 5: 0xFFC107,
    6: 0xFFB300, 7: 0xFFA000, 8: 0xFF8F00,
    9: 0xFF6F00
}

brownScale = {
    0: 0xEFEBE9, 1: 0xD7CCC8, 2: 0xBCAAA4,
    3: 0xA1887F, 4: 0x8D6E63, 5: 0x795548,
    6: 0x6D4C41, 7: 0x5D4037, 8: 0x4E342E,
    9: 0x3E2723
}

redScale = {
    0: 0xffebee, 1: 0xffcdd2, 2: 0xef9a9a,
    3: 0xe57373, 4: 0xef5350, 5: 0xf44336,
    6: 0xe53935, 7: 0xd32f2f, 8: 0xc62828,
    9: 0xb71c1c
}

clBlack = 0x000000

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

    @abstractmethod
    def _add_merged_titles(self) -> None:
        pass

    @abstractmethod
    def _format_head_borders(self) -> None:
        pass

    @abstractmethod
    def _format_head_colors(self) -> None:
        pass

    def __init__(self, workbook: Workbook) -> None:
        self.__workbook = workbook
        self._sheet = None
        self._gaps = []
        self._metadatas = []
        self._max_row = 0

        self._init_metadatas()
        self._merge_metadatas()

    # Class Property: Sheet Variables
    def __prepare_sheet(self) -> None:
        # For later use
        pass

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
        print(" * Formatting Columns")
        self._set_sheetwide_view()
        self._set_columns_format()

        print(" * Formatting Header")
        self._add_merged_titles()
        self._format_head_borders()
        self._format_head_colors()

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

    # -- -- --

    # Sheet Helper: Multiple Usages
    def _border_cell_outer(self,
            a_t: int, a_b: int, a_l: int, a_r: int,
            side: Side) -> None:

        for col in range(a_l, a_r+1):
            # top
            cell = self._sheet.cell(row=a_t, column=col)
            current = cell.border
            new_top = current.top if current.top and current.top.style else side

            cell.border = Border(
                top    = new_top,
                bottom = current.bottom,
                left   = current.left,
                right  = current.right)

            # bottom
            cell = self._sheet.cell(row=a_b, column=col)
            current = cell.border
            new_bottom = current.bottom if current.bottom and current.bottom.style else side

            cell.border = Border(
                top    = current.top,
                bottom = new_bottom,
                left   = current.left,
                right  = current.right)

        for row in range(a_t, a_b+1):
            # left
            cell = self._sheet.cell(row=row, column=a_l)
            current = cell.border
            new_left = current.left if current.left and current.left.style else side

            cell.border = Border(
                top    = current.top,
                bottom = current.bottom,
                left   = new_left,
                right  = current.right)

            # right
            cell = self._sheet.cell(row=row, column=a_r)
            current = cell.border
            new_right = current.right if current.right and current.right.style else side

            cell.border = Border(
                top    = current.top,
                bottom = current.bottom,
                left   = current.left,
                right  = new_right)   

    # Sheet Helper: Multiple Usages
    def _border_cell_inner_oneliner(self,
            a_t: int, a_b: int, a_l: int, a_r: int,
            side: Side) -> None:

        for col in range(a_l+1, a_r):
            # inner top only
            cell = self._sheet.cell(row=a_t, column=col)

            current = cell.border
            new_left = current.left if current.left and current.left.style else side
            new_right = current.right if current.right and current.right.style else side

            cell.border = Border(
                top    = current.top,
                bottom = current.bottom,
                left   = new_left,
                right  = new_right)

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

    # Formatting Procedure: Refactored from _add_merged_titles()
    def __set_merged_title(self, metadata: dict[str, any]) -> None:
        start_letter = metadata['col-start']

        for title in metadata['titles']:
            col_letter_start = self._get_relative_column_letter(
                start_letter, title['col-start-id']-1)  
            col_letter_end   = self._get_relative_column_letter(
                start_letter, title['col-end-id']-1)

            # Set title text
            cell = self._sheet[f"{col_letter_start}2"]
            cell.value = title['text']

            # Set background color
            hex_color = f"ff{title['bg']:06x}"
            cell.fill = PatternFill(
                start_color=hex_color,
                end_color=hex_color,
                fill_type='solid')
            
            # Define the border style and color
            side = lfBlack
            cell.border = Border(top = side,
                bottom = side, left  = side, right = side)

            cell.font = Font(
                name='Arial', sz='10', bold=True,
                color='000000')
            
            cell.alignment = Alignment(horizontal='center')

            # Merge the cells for the title
            merge_address = f"{col_letter_start}2:{col_letter_end}2"
            self._sheet.merge_cells(merge_address)

    # Formatting Procedure: Abstract Override
    def _add_merged_titles(self) -> None:
        for metadata in self._metadatas:
            self.__set_merged_title(metadata)

        # Call the hook method (default does nothing)
        self._add_merged_titles_post()

    # Formatting Procedure: Hook
    def _add_merged_titles_post(self) -> None:
        """Hook method to be overridden by subclasses if needed."""
        pass

    # Formatting Procedure: Abstract Override
    def _format_head_borders(self) -> None:
        pass

    # Formatting Procedure: Abstract Override
    def _format_head_borders(self) -> None:
        for metadata in self._metadatas:
            start_letter = metadata['col-start']
            for border_config in metadata.get('head-borders', []):

                # border_config: (col_start_id, col_end_id, outer_line, vert_line)
                col_start_id, col_end_id, outer_line, vert_line = border_config

                letter_start = self._get_relative_column_letter(
                    start_letter, col_start_id)
                letter_end   = self._get_relative_column_letter(
                    start_letter, col_end_id)

                self.__apply_head_border(
                    letter_start, letter_end, outer_line, vert_line)

    # Formatting Procedure: Abstract Override
    def _format_head_colors(self) -> None:
        for metadata in self._metadatas:
            start_letter = metadata['col-start']
            start_index  = column_index_from_string(start_letter)

            pairs = metadata['fields'].items()
            for pair_index, (field, data) in enumerate(pairs, start=0):
                row_index = 3
                col_index = start_index + pair_index
                cell = self._sheet.cell(row=row_index, column=col_index)

                # Define font
                cell.font = Font(
                    name='Arial', sz='10', color='000000')
            
                cell.alignment = Alignment(horizontal='center')            

                if bg_color := data.get('bg'):
                    # Apply header background color using PatternFill
                    hex_color = f"ff{bg_color:06x}"
                    cell.fill = PatternFill(
                        start_color=hex_color, end_color=hex_color,
                        fill_type='solid')
    # -- -- --

    # Sheet Helper
    # To be used only within the _format_head_borders()
    def __apply_head_border(self,
        letter_start: str, letter_end: str,
        outer_line: Side, vert_line: Side) -> None:

        # Define the cell range for rows and columns
        # Top, Bottom (max row), Left, Right
        a_t = 3
        a_b = 3
        a_l = column_index_from_string(letter_start) - 1
        a_r = column_index_from_string(letter_end) - 1

        self._border_cell_outer(a_t, a_b, a_l, a_r, outer_line)
        self._border_cell_inner_oneliner(a_t, a_b, a_l, a_r, vert_line)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularData(FormatterCommon):
    # Unified Configuration
    def _init_metadatas(self) -> None:
        self._metadata_movies_base = {
            'fields': {
                'Year'     : { 'width': 1.5, 'bg': blueScale[3],
                               'align': 'center' },
                'Title'    : { 'width': 6,   'bg': blueScale[2] },
                'Genre'    : { 'width': 3,   'bg': blueScale[1] },
                'Plot'     : { 'width': 6,   'bg': blueScale[2] },
                'Actors'   : { 'width': 6,   'bg': blueScale[1] },
                'Director' : { 'width': 5,   'bg': blueScale[2] }
            },

            'titles': [{ 
                'col-start-id' : 1, 'col-end-id' : 6,
                'text' : 'Base Movie Data', 
                'bg' : blueScale[3], 'fg' : clBlack                    
            }],

            # letter_start, letter_end, outer_line, vert_line
            'head-borders': [
                ( 1, 6, lfBlack, lfBlack)]
        }

        self._metadata_movies_additional = {
            'fields': {
                'Rated'    : { 'width': 2,   'bg': tealScale[2],
                               'align': 'center' },
                'Runtime'  : { 'width': 2.5, 'bg': tealScale[1],
                               'align': 'center' },
                'Metascore': { 'width': 2,   'bg': tealScale[2],
                            'align': 'center' }
            },

            'titles': [{ 
                'col-start-id' : 1, 'col-end-id' : 3,
                'text' : 'Additional Data', 
                'bg' : tealScale[3], 'fg' : clBlack                    
            }],
            'head-borders': [
                ( 1, 3, lfBlack, lfBlack)]
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

