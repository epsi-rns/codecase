from lib.ColorScale import (
  clBlack, blueScale, tealScale, amberScale, brownScale, redScale)
from lib.FormatterTabular import FormatterTabular

from openpyxl import load_workbook
from openpyxl.styles import Side

lfNone  = Side(style=None, color=None)
lfBlack = Side(style='thin', color='000000')
lfGray  = Side(style='thin', color='E0E0E0') #gray300

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularData(FormatterTabular):
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
                ( 1, 6, lfBlack, lfBlack)],

           # letter_start, letter_end, outer_line, vert_line, horz_line
           'data-borders': [
                ( 1,  2, lfBlack, lfBlack, lfGray),
                ( 3,  6, lfBlack, lfGray,  lfGray)]
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
                ( 1, 3, lfBlack, lfBlack)],
            'data-borders': [
                ( 1, 3, lfBlack, lfGray, lfGray)]
        }

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularMovies(FormatterTabularData):
    # Merge Configuration
    def _merge_metadatas(self) -> None:
        # Columns:    A, H,  L
        self._gaps  = [0, 7, 11]
        self._freeze = "C4"

        self._metadatas = [{
            'col-start'     : 'B',
            **self._metadata_movies_base
        }, {
            'col-start'     : 'I',
            **self._metadata_movies_additional
        }]

    def _add_merged_titles_post(self) -> None:
        # Altering Manually
        self._sheet['F3'].value = 'Actors/Actress'

    def _format_one_sheet_post(self) -> None:
        print(f' * Additional Formatting: {self._max_row} rows')
        self._color_group = 'B'
        self._color_groups()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

def main() -> None:
    input_xlsx  = "./xlsx/movies_all.xlsx"
    output_xlsx = "./xlsx/movies_all_formatted.xlsx"

    wb = load_workbook(input_xlsx)
    formatter = FormatterTabularMovies(wb)
    formatter.process_all()
    wb.save(output_xlsx)

if __name__ == "__main__":
    main()

