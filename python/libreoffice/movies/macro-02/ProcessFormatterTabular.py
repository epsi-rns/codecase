import sys

# Linux Based
lib_path = '/home/epsi/.config/libreoffice/4/user/Scripts/python/Movies'

# Windows Based
# lib_path =  'C:\\Users\\epsir\\AppData\\Roaming\\LibreOffice\\4\\user\\Scripts\\python\\Movies'

# Add the path to the macro
sys.path.append(lib_path)

from lib.ColorScale import (
  clBlack, blueScale, tealScale, amberScale, brownScale, redScale)
from lib.BorderFormat import (lfBlack, lfGray, lfNone)
from lib.FormatterTabular import FormatterTabular

from com.sun.star.sheet import XSpreadsheetDocument

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularData(FormatterTabular):
  @property
  def _document(self) -> XSpreadsheetDocument:
    return XSCRIPTCONTEXT.getDocument()

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
        'col-start-id' : 1, 'col-end-id' : 6, 'text' : 'Base Movie Data', 
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
        'col-start-id' : 1, 'col-end-id' : 3, 'text' : 'Additional Data', 
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
    # Columns:   A, H,  L
    self._gaps = [0, 7, 11]

    self._metadatas = [{
      'col-start'     : 'B',
      **self._metadata_movies_base
    }, {
      'col-start'     : 'I',
      **self._metadata_movies_additional
    }]

  def _add_merged_titles_post(self) -> None:
    # Altering Manually
    self._sheet['F3'].String = 'Actors/Actress'

  def _format_one_sheet_post(self) -> None:
    print(f' * Additional Formatting: {self._max_row} rows')
    self._color_group = 'B'
    self._color_groups()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Represent Class in Macro

def tabular_single_movies() -> None:
  movies = FormatterTabularMovies()
  movies.process_one()

def tabular_multi_movies() -> None:
  movies = FormatterTabularMovies()
  movies.process_all()
