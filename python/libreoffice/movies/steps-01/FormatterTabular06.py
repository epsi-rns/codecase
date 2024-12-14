from abc import ABC, abstractmethod

from com.sun.star.\
  awt.FontWeight import BOLD
from com.sun.star.\
  table.CellHoriJustify import LEFT, CENTER, RIGHT
from com.sun.star.\
  table import BorderLine2, BorderLineStyle, TableBorder2

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
  def __init__(self) -> None:
    self.controller = self.document.getCurrentController()

    self.init_field_metadata()
    self.prepare_sheet()

  @abstractmethod
  def init_field_metadata(self) -> None:
    pass

  @abstractmethod
  def reset_pos_columns(self) -> None:
    pass

  @abstractmethod
  def set_sheetwide_view(self) -> None:
    pass

  @abstractmethod
  def add_merged_title(self) -> None:
    pass

  @abstractmethod
  def format_head_borders(self) -> None:  
    pass

  # Class Property: Sheet Variables
  def prepare_sheet(self):
    # number and date format
    self.numberfmt = self.document.NumberFormats
    self.locale    = self.document.CharLocale

    # table border
    lineFormatNone = BorderLine2()
    lineFormatNone.LineStyle = BorderLineStyle.NONE
    self.lfNone= lineFormatNone

    # table border
    lineFormatBlack = BorderLine2()
    lineFormatBlack.LineStyle = BorderLineStyle.SOLID
    lineFormatBlack.LineWidth = 20
    lineFormatBlack.Color = 0x000000 #black
    self.lfBlack = lineFormatBlack

    # table border
    lineFormatGray = BorderLine2()
    lineFormatGray.LineStyle = BorderLineStyle.SOLID
    lineFormatGray.LineWidth = 20
    lineFormatGray.Color = 0xE0E0E0 #gray300
    self.lfGray = lineFormatGray

  # Sheet Helper
  # To be used only within the formatOneSheet(), reset_pos_rows()
  def get_last_used_row(self) -> None:
    cursor = self.sheet.createCursor()
    cursor.gotoEndOfUsedArea(False)
    cursor.gotoStartOfUsedArea(True)
    rows = cursor.getRows()
    
    return len(rows)

  # Sheet Helper
  # To be used only within the set_columns_format()
  def get_number_format(self, format_string):
    nf = self.numberfmt.queryKey(  \
              format_string, self.locale, True)
    if nf == -1:
       nf = self.numberfmt.addNew( \
              format_string, self.locale)
    return nf

  # Formatting Procedure
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

  # Helper: Multiple Usages
  def column_letter_to_index(self, column_letter) -> None:
    index = 0
    for i, char in enumerate(reversed(column_letter)):
      index += (ord(char) - ord('A') + 1) * (26 ** i)
    return index - 1  # Convert to 0-based index

  # Sheet Helper
  # To be used only within the apply_head_border()
  def get_head_range(self, letter_start, letter_end):
    # Define the cell range for rows and columns
    head_row = 2
    col_start = self.column_letter_to_index(letter_start)
    col_end   = self.column_letter_to_index(letter_end)

    # Define the cell range for the outer border and vertical lines
    return self.sheet.getCellRangeByPosition(
      col_start, head_row, col_end, head_row)

  # Helper: Multiple Usages
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

  # Sheet Helper
  # To be used only within the apply_head_border()
  def set_head_rectangle(self,
        letter_start, letter_end, line_format) -> None:
    # Define the cell range for rows and columns  
    # Top, Bottom (max row), Left, Right
    a_t = 2
    a_b = 2
    a_l = self.column_letter_to_index(letter_start)
    a_r = self.column_letter_to_index(letter_end)

    self.format_cell_rectangle(a_t, a_b, a_l, a_r, line_format)

  # Sheet Helper
  # To be used only within the format_head_borders()
  def apply_head_border(self,
        letter_start, letter_end,
        outer_line, vert_line) -> None:
    self.set_head_rectangle(
      letter_start, letter_end, outer_line)

    border = TableBorder2()
    border.IsVerticalLineValid   = True
    border.VerticalLine   = vert_line

    cell_range = self.get_head_range(
      letter_start, letter_end)
    cell_range.TableBorder2 = border

  # Formatting Procedure
  def set_columns_format(self) -> None:
    columns = self.sheet.Columns

    # Alignment mapping
    alignment_map = {
        'left'  : LEFT,  'center': CENTER, 'right' : RIGHT }

    for field, data in self.fields.items():
      letter = data['col']
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

  # Formatting Procedure
  def format_head_colors(self) -> None:  
    for field, data in self.fields.items():
      if bg_color := data.get('bg'):
        letter = data['col']      
        row_index = 2
        col_index = self.column_letter_to_index(letter)

        cell = self.sheet.getCellByPosition(
          col_index , row_index)
        cell.CellBackColor = bg_color 

  # Basic Flow
  def formatOneSheet(self) -> None:
    self.max_row = self.get_last_used_row()

    if not self.is_first_column_empty():
      # Rearranging Columns
      print(' * Rearranging Columns')
      self.reset_pos_columns()
      self.reset_pos_rows()
      self.max_row += 1

    # Apply Sheet Wide
    print(' * Formatting Columns')
    self.set_sheetwide_view()
    self.set_columns_format()

    # Apply Header Settings
    print(' * Formatting Header')
    self.add_merged_title()
    self.format_head_borders()
    self.format_head_colors()

  # Basic Flow
  def processOne(self) -> None:
    self.sheet = self.controller.getActiveSheet()
    self.formatOneSheet()

  # Basic Flow
  def processAll(self) -> None:
    for sheet in self.document.Sheets:
      print(sheet.Name)
      self.sheet = sheet
      self.formatOneSheet()

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class TabularFormatterCommon(FormatterBase):
  def __init__(self) -> None:
    self.document = XSCRIPTCONTEXT.getDocument()
    super().__init__()

  # Simple Configuration
  def init_field_metadata(self) -> None:
    self.fields = {
       'Year'     : { 'col': 'B', 'width': 1.5, 'bg': blueScale[3],
                      'align': 'center' },
       'Title'    : { 'col': 'C', 'width': 6,   'bg': blueScale[2] },
       'Genre'    : { 'col': 'D', 'width': 3,   'bg': blueScale[1] },
       'Plot'     : { 'col': 'E', 'width': 6,   'bg': blueScale[2] },
       'Actors'   : { 'col': 'F', 'width': 6,   'bg': blueScale[1] },
       'Director' : { 'col': 'G', 'width': 5,   'bg': blueScale[2] },

       'Rated'    : { 'col': 'I', 'width': 2,   'bg': tealScale[2],
                      'align': 'center' },
       'Runtime'  : { 'col': 'J', 'width': 2.5, 'bg': tealScale[1],
                      'align': 'center' },
       'Metascore': { 'col': 'K', 'width': 2,   'bg': tealScale[2],
                      'align': 'center' }
    }

  # Formatting Procedure: Abstract Override
  def set_sheetwide_view(self) -> None:
    # activate sheet
    spreadsheetView = self.controller
    spreadsheetView.setActiveSheet(self.sheet)

    # sheet wide
    spreadsheetView.ShowGrid = False
    spreadsheetView.freezeAtPosition(2, 3)

  # Formatting Procedure
  def reset_pos_columns(self) -> None:
    columns = self.sheet.Columns
    column_width_div = 0.5 * 1000  # Width of 0.5 cm

    # Insert one column at the specified indexes
    columns.insertByIndex( 0, 1) # Column A
    columns.insertByIndex( 7, 1) # Column H
    columns.insertByIndex(11, 1) # Column L

    # Set widths for columns A, H
    columns.getByIndex( 0).Width = column_width_div
    columns.getByIndex( 7).Width = column_width_div
    columns.getByIndex(11).Width = column_width_div

  # Formatting Procedure
  def add_merged_title(self) -> None:
    self.sheet['B2:K3'].HoriJustify = CENTER
    self.sheet['B2:K2'].CharWeight = BOLD 

    cell = self.sheet['B2']
    cell.String = 'Base Movie Data'
    cell.CellBackColor = blueScale[3]
    cell.CharColor = clBlack
    self.format_cell_rectangle(
      1, 1, 1, 1, self.lfBlack)
    self.sheet['B2:G2'].merge(True)

    cell = self.sheet['I2']
    cell.String = 'Additional'
    cell.CellBackColor = tealScale[3]
    cell.CharColor = clBlack
    self.format_cell_rectangle(
      1, 1, 8, 8, self.lfBlack)
    self.sheet['I2:K2'].merge(True)

  # Formatting Procedure
  def format_head_borders(self) -> None:  
    # Base Movie Data
    self.apply_head_border(
      'B', 'G', self.lfBlack, self.lfBlack)

    # Additional Data
    self.apply_head_border(
      'I', 'K', self.lfBlack, self.lfBlack)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

def processOne() -> None:
  sample = TabularFormatterCommon()
  sample.processOne()

def processAll() -> None:
  sample = TabularFormatterCommon()
  sample.processAll()