from abc import ABC, abstractmethod

from com.sun.star.\
  awt.FontWeight import BOLD
from com.sun.star.\
  table.CellHoriJustify import LEFT, CENTER, RIGHT
from com.sun.star.\
  table import BorderLine2, BorderLineStyle

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

class BorderFormatManager:
  def create_line_format_none(self):
    lineFormatNone = BorderLine2()
    lineFormatNone.LineStyle = BorderLineStyle.NONE
    return lineFormatNone

  def create_line_format_black(self):
    lineFormatBlack = BorderLine2()
    lineFormatBlack.LineStyle = BorderLineStyle.SOLID
    lineFormatBlack.LineWidth = 20
    lineFormatBlack.Color = 0x000000 #black
    return lineFormatBlack

  def create_line_format_gray(self):
    lineFormatGray = BorderLine2()
    lineFormatGray.LineStyle = BorderLineStyle.SOLID
    lineFormatGray.LineWidth = 20
    lineFormatGray.Color = 0xE0E0E0 #gray300
    return lineFormatGray

# table border
bfm = BorderFormatManager()
lfNone  = bfm.create_line_format_none()
lfBlack = bfm.create_line_format_black()
lfGray  = bfm.create_line_format_gray()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterBase:
  def __init__(self) -> None:
    self.controller = self.document.getCurrentController()

    self.prepare_sheet()
    self.init_metadatas()
    self.merge_metadatas()

  # Class Property: Sheet Variables
  def prepare_sheet(self):
    # number and date format
    self.numberfmt = self.document.NumberFormats
    self.locale    = self.document.CharLocale

  # -- -- --

  @abstractmethod
  def init_metadatas(self) -> None:
    pass

  @abstractmethod
  def reset_pos_columns(self) -> None:
    pass

  @abstractmethod
  def reset_pos_rows(self) -> None:
    pass

  @abstractmethod
  def set_sheetwide_view(self) -> None:
    pass

  @abstractmethod
  def set_columns_format(self) -> None:
    pass

  @abstractmethod
  def add_merged_titles(self) -> None:
    pass

  # -- -- --

  # Basic Flow
  def format_one_sheet(self) -> None:
    self.max_row = self.get_last_used_row()

    if not self.is_first_column_empty():
      # Rearranging Columns
      print(' * Rearranging Columns')
      self.reset_pos_columns()
      print(' * Setting Rows Width')
      self.reset_pos_rows()
      self.max_row += 1

    # Apply Sheet Wide
    print(' * Formatting Columns')
    self.set_sheetwide_view()
    self.set_columns_format()

    # Apply Header Settings
    print(' * Formatting Header')
    self.add_merged_titles()

    # Call the hook method (default does nothing)
    self.format_one_sheet_post()

    print(' * Finished')
    print()

  # Basic Flow: Hook
  def format_one_sheet_post(self) -> None:
    """Hook method to be overridden by subclasses if needed."""
    pass

  # Basic Flow
  def process_one(self) -> None:
    self.sheet = self.controller.getActiveSheet()
    self.format_one_sheet()

  # Basic Flow
  def process_all(self) -> None:
    for sheet in self.document.Sheets:
      print(sheet.Name)
      self.sheet = sheet
      self.format_one_sheet()

  # -- -- --

  # Helper: Multiple Usages
  def column_index_to_letter(self, index: int) -> str:
    """Convert a 0-based column index to Excel-style column letters."""
    letters = ''
    while index >= 0:
      letters = chr(index % 26 + ord('A')) + letters
      index = index // 26 - 1
    return letters

  # Helper: Multiple Usages
  def column_letter_to_index(self, column_letter: str) -> int:
    """Convert Excel-style column letters to a 0-based column index."""
    index = 0
    for i, char in enumerate(reversed(column_letter)):
      index += (ord(char) - ord('A') + 1) * (26 ** i)
    return index - 1

  # Helper: Multiple Usages
  def get_relative_column_letter(self, start_letter: str, offset: int) -> str:
    """Get the Excel-style column letter at an offset from the start_letter."""
    start_index    = self.column_letter_to_index(start_letter)
    relative_index = start_index + offset - 1
    return self.column_index_to_letter(relative_index)

  # -- -- --

  # Sheet Helper
  # To be used only within the formatOneSheet(), reset_pos_rows()
  def get_last_used_row(self) -> None:
    cursor = self.sheet.createCursor()
    cursor.gotoEndOfUsedArea(False)
    cursor.gotoStartOfUsedArea(True)
    rows = cursor.getRows()
    
    return len(rows)

  # Sheet Helper
  # To be used only within the formatOneSheet()
  def is_first_column_empty(self) -> bool:
    rows = self.sheet.Rows
    max_sampling_row = 10

    for row_index in range(max_sampling_row + 1):
      cell = self.sheet.getCellByPosition(0, row_index)
      # 0 indicates an empty cell
      if cell.String != "": return False
    return True

  # Sheet Helper
  # To be used only within the set_columns_format()
  def get_number_format(self, format_string):
    nf = self.numberfmt.queryKey(  \
              format_string, self.locale, True)
    if nf == -1:
       nf = self.numberfmt.addNew( \
              format_string, self.locale)
    return nf

  # Sheet Helper: Multiple Usages
  def format_cell_rectangle(self,
        a_t, a_b, a_l, a_r, line_format) -> None:

    func_gcrb = self.sheet.getCellRangeByPosition

    # Formatting Rectangle Edges
    cr_top = func_gcrb(a_l, a_t, a_r, a_t)
    cr_top.TopBorder       = line_format

    cr_bottom = func_gcrb(a_l, a_b, a_r, a_b)
    cr_bottom.BottomBorder = line_format
    
    cr_left = func_gcrb(a_l, a_t, a_l, a_b)
    cr_left.LeftBorder     = line_format

    cr_right = func_gcrb(a_r, a_t, a_r, a_b)
    cr_right.RightBorder   = line_format

    # Formatting Rectangle Corner
    cr_top_left = func_gcrb(a_l, a_t, a_l, a_t)
    cr_top_left.TopBorder        = line_format
    cr_top_left.LeftBorder       = line_format

    cr_top_right = func_gcrb(a_r, a_t, a_r, a_t)
    cr_top_right.TopBorder       = line_format
    cr_top_right.RightBorder     = line_format

    cr_bottom_left = func_gcrb(a_l, a_b, a_l, a_b)
    cr_bottom_left.BottomBorder  = line_format
    cr_bottom_left.LeftBorder    = line_format

    cr_bottom_right = func_gcrb(a_r, a_b, a_r, a_b)
    cr_bottom_right.BottomBorder = line_format
    cr_bottom_right.RightBorder  = line_format

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterCommon(FormatterBase):

  # Formatting Procedure: Abstract Override
  def reset_pos_columns(self) -> None:
    columns = self.sheet.Columns
    column_width_div = 0.5 * 1000  # Width of 0.5 cm

    # Insert column, and set width
    for gap in self.gaps:
      columns.insertByIndex(gap, 1)
      columns.getByIndex(gap).Width  = column_width_div

      letter = self.column_index_to_letter(gap)
      print(f"   - Insert Gap: {letter}")

  # Formatting Procedure: Abstract Override
  def reset_pos_rows(self) -> None:
    rows = self.sheet.Rows
    row_height = 0.5 * 1000  # Height of 0.5 cm

    # Range to be processed
    # Omit header and plus one for the last
    range_rows = range(2, self.max_row + 1)

    for row_index in range_rows:
      rows.getByIndex(row_index).Height = row_height

    # Insert one row at the specified indexes
    rows.insertByIndex(0, 2)  # Row 0

    row_height_div = 0.3 * 1000  # Height of 0.3 cm
    rows.getByIndex(0).Height = row_height_div
    rows.getByIndex(self.max_row + 2).Height = row_height_div

  # Formatting Procedure: Abstract Override
  def set_columns_format(self) -> None:
    columns = self.sheet.Columns

    # Alignment mapping
    alignment_map = {
        'left'  : LEFT,  'center': CENTER, 'right' : RIGHT }

    for metadata in self.metadatas:
      start_letter = metadata['col-start']

      pairs = metadata['fields'].items()
      for pair_index, (field, data) in enumerate(pairs, start=1):
        letter = self.get_relative_column_letter(
          start_letter, pair_index)
        width  = data['width'] * 1000
        align  = data.get('align')

        col_index = self.column_letter_to_index(letter)
        column = columns.getByIndex(col_index)
        column.Width = width

        start_row = 3
        end_row = self.max_row
        cell_range = self.sheet.getCellRangeByPosition(
          col_index, start_row, col_index, end_row)

        if align in alignment_map:
           cell_range.HoriJustify = alignment_map[align]

        if cell_format := data.get('format'):
           cell_range.NumberFormat = self.get_number_format(cell_format)

  # Formatting Procedure: Refactored from add_merged_titles()
  def set_merged_title(self, metadata) -> None:
    start_letter = metadata['col-start']

    for title in metadata['titles']:
      col_letter_start = self.get_relative_column_letter(
          start_letter, title['col-start-id'])  
      col_letter_end   = self.get_relative_column_letter(
          start_letter, title['col-end-id'])

      cell = self.sheet[f"{col_letter_start}2"]
      cell.String        = title['text']
      cell.CellBackColor = title['bg']
      cell.CharColor     = title['fg']

      pos = self.column_letter_to_index(col_letter_start)
      self.format_cell_rectangle(
        1, 1, pos, pos, lfBlack)

      merge_address = f"{col_letter_start}2:{col_letter_end}2"
      self.sheet[merge_address].merge(True)
      self.sheet[merge_address].CharWeight = BOLD

      header_address = f"{col_letter_start}2:{col_letter_end}3"
      self.sheet[header_address].HoriJustify = CENTER

  # Formatting Procedure: Abstract Override
  def add_merged_titles(self) -> None:
    self.sheet['B2:BC3'].HoriJustify = CENTER
    self.sheet['B2:BC2'].CharWeight  = BOLD 

    for metadata in self.metadatas:
      self.set_merged_title(metadata)

    # Call the hook method (default does nothing)
    self.add_merged_titles_post()

  # Formatting Procedure: Hook
  def add_merged_titles_post(self) -> None:
    """Hook method to be overridden by subclasses if needed."""
    pass

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabular(FormatterCommon):
  def set_sheetwide_view(self) -> None:
    # activate sheet
    spreadsheetView = self.controller
    spreadsheetView.setActiveSheet(self.sheet)

    # sheet wide
    spreadsheetView.ShowGrid = False
    spreadsheetView.freezeAtPosition(3, 3)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularData(FormatterTabular):
  def __init__(self) -> None:
    self.document = XSCRIPTCONTEXT.getDocument()
    super().__init__()

  # Unified Configuration
  def init_metadatas(self) -> None:
    self.metadata_movies_base = {
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
      }]
    }

    self.metadata_movies_additional = {
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
      }]
    }

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class FormatterTabularMovies(FormatterTabularData):

  # Merge Configuration
  def merge_metadatas(self) -> None:
    # Columns:   A, H,  L
    self.gaps = [0, 7, 11]

    self.metadatas = [{
      'col-start'     : 'B',
      **self.metadata_movies_base
    }, {
      'col-start'     : 'I',
      **self.metadata_movies_additional
    }]

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Represent Class in Macro

def tabular_single_movies() -> None:
  sample = FormatterTabularMovies()
  sample.process_one()

def tabular_multi_movies() -> None:
  sample = FormatterTabularMovies()
  sample.process_all()
