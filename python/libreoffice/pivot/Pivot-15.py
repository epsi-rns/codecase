from datetime import datetime, timedelta
from pprint import pprint
from collections import Counter

from com.sun.star.\
  awt.FontWeight import BOLD
from com.sun.star.\
  table.CellHoriJustify import CENTER
from com.sun.star.\
  table import BorderLine2, BorderLineStyle

tealScale = {
  0: 0xE0F2F1, 1: 0xB2DFDB, 2: 0x80CBC4,
  3: 0x4DB6AC, 4: 0x26A69A, 5: 0x009688,
  6: 0x00897B, 7: 0x00796B, 8: 0x00695C,
  9: 0x004D40
}

class PivotSample:
  def __init__(self,
      sheetSourceName: str,
      col_date: str, col_cats: str,
      start_cell: str) -> None:

    document = XSCRIPTCONTEXT.getDocument()
    self.sheet_src = document.Sheets[sheetSourceName]
    self.start_cell = start_cell

    self.col_date = col_date
    self.col_cats = col_cats

    # Get the list of catssify values
    self.lookup_cats = self.get_lookup_cats()

  def get_lookup_cats(self):
    return ["Apple", "Banana", "Orange", "Grape",
      "Strawberry", "Durian", "Mango", "Dragon Fruit"]

  def get_last_used_row(self):
    cursor = self.sheet_src.createCursor()
    cursor.gotoEndOfUsedArea(False)
    cursor.gotoStartOfUsedArea(True)
    rows = cursor.getRows()
    
    return len(rows)

  def get_number_format(self, format_string):
    nf = self.numberfmt.queryKey(  \
              format_string, self.locale, True)
    if nf == -1:
       nf = self.numberfmt.addNew( \
              format_string, self.locale)
    return nf

  def prepare_sheet(self):
    document   = XSCRIPTCONTEXT.getDocument()
    sheets_dst = document.Sheets
    if not sheets_dst.hasByName('Pivot'):
      sheets_dst.insertNewByName('Pivot', 1)
    self.sheet_dst = sheets_dst['Pivot']

    # activate sheet
    desktop    = XSCRIPTCONTEXT.getDesktop()
    model      = desktop.getCurrentComponent()
    controller = model.getCurrentController()
    controller.setActiveSheet(self.sheet_dst)

    # Initial Position
    self.addr = self.sheet_dst[self.start_cell].CellAddress

    # number and date format
    self.numberfmt = model.NumberFormats
    self.locale    = model.CharLocale

    date_format = 'DD-MMM-YY;@'
    self.dateFormat = \
      self.get_number_format(date_format)

    # table border
    lineFormat = BorderLine2()
    lineFormat.LineStyle = BorderLineStyle.SOLID
    lineFormat.LineWidth = 20
    lineFormat.Color = tealScale[9]
    self.lineFormat = lineFormat

  def get_formatted_date(self, excel_date):
    # Convert the number to a datetime object
    # Excel's epoch is two days off from the standard epoch
    excel_epoch = datetime(1899, 12, 30)
    date_obj = excel_epoch + timedelta(days=excel_date)

    # Format the datetime object as 'dd/mm/yyyy'
    return date_obj.strftime('%d/%m/%Y')

  # dump into terminal for convenience
  def build_records(self):
    # range to be proceed
    # omit header and plus one for the last
    max_row = self.get_last_used_row()
    range_rows = range(2, max_row+1)

    print(f'Range  : {range_rows}')

    # retrieving all rows data
    all_values = []
    for row in range_rows:
      if int(round(row/100))*100==row: print(f'{row} ...')
      all_values.append({
        'date' : int(self.sheet_src[f'{self.col_date}{row}'].Value),
        'cats' : self.sheet_src[f'{self.col_cats}{row}'].String
        })

    # Grouping using list comprehension
    # keep the dictionary for further use
    all_dates = {
      row['date']: [{'cats': item['cats']}
      for item in all_values
      if item['date'] == row['date']]
        for row in all_values
    }

    # Count occurrences by break into an array
    occurrences = {
      date: {cats: values.count(cats) for cats in set(values)}
      for date, row in all_dates.items()
      for values in [[item['cats'] for item in row]]
    }

    # Get the list of catss values
    lookup_cats = self.lookup_cats

    # Create a new dictionary with all catss values
    # and their counts (zero if not found)
    ensure_occurrences = {
      date: {
        cats: row.get(cats, 0)
        for cats in lookup_cats
      }
      for date, row in occurrences.items()}

    self.ensure_occurrences = ensure_occurrences

  def get_sum_occurrences(self):
    # Initialize an empty dictionary to store the sums
    sum_dict = {}

    for cats_dict in self.ensure_occurrences.values():
      for key, value in cats_dict.items():
        sum_dict[key] = sum_dict.get(key, 0) + value
    
    return sum_dict

  def write_column_headers(self):
    # Get the list of catssify values
    column_header = ['Date'] \
      + self.lookup_cats + ['Total']

    # Fill the cells horizontally
    for col, header in enumerate(column_header, start=0):
      col_pos = self.addr.Column + col
      col_row = self.addr.Row

      cell = self.sheet_dst. \
        getCellByPosition(col_pos, col_row)
      cell.String = header

      cell.CharWeight = BOLD
      cell.BottomBorder = self.lineFormat

      if col_pos % 2:
        cell.CellBackColor = tealScale[1]
      else:
        cell.CellBackColor = tealScale[0]

      column = self.sheet_dst. \
        getColumns().getByIndex(col_pos)
      column.Width = 3000

    column = self.sheet_dst. \
      getColumns().getByIndex(0). \
      Width = 500
    column = self.sheet_dst. \
      getColumns().getByIndex(len(column_header) + 1). \
      Width = 500

  def write_row_a_header(self, row_index: int, date: int):
    col_pos = self.addr.Column
    row_pos = self.addr.Row + row_index

    formatted_date = self.get_formatted_date(date)
    print(f"  Date : {formatted_date}")

    cell = self.sheet_dst. \
      getCellByPosition(col_pos, row_pos)
    cell.Value = date

    cell.NumberFormat = self.dateFormat
    cell.HoriJustify = CENTER # or just 2
    cell.RightBorder = self.lineFormat
    cell.CellBackColor = tealScale[0]

  def write_row_content(self,
      row_index: int, row):

    # Fill the each row
    row_pos = self.addr.Row + row_index
    for col, cats in enumerate(self.lookup_cats, start=1):
      col_pos = self.addr.Column + col

      cell = self.sheet_dst. \
        getCellByPosition(col_pos, row_pos)
      if row[cats]:
        cell.Value = row[cats]
        cell.HoriJustify = CENTER # or just 2

  def write_row_a_total(self,
      row_index: int, row):

    col_pos = self.addr.Column \
            + len(self.lookup_cats) + 1
    row_pos = self.addr.Row + row_index

    cell = self.sheet_dst. \
      getCellByPosition(col_pos, row_pos)
    cell.Value = sum(row.values())

    cell.HoriJustify = CENTER # or just 2
    cell.LeftBorder = self.lineFormat
    cell.CellBackColor = tealScale[0]

  def write_rows(self):
    # Fill the rows
    row_index = 0
    for date, row in self.ensure_occurrences.items():
      row_index += 1
      self.write_row_a_header(row_index, date)
      self.write_row_content(row_index, row)
      self.write_row_a_total(row_index, row)

  def write_column_total_header(self):
    col_pos = self.addr.Column
    row_pos = self.addr.Row \
            + len(self.ensure_occurrences) + 1

    cell = self.sheet_dst. \
      getCellByPosition(col_pos, row_pos)
    cell.String = 'Total'

    cell.CharWeight = BOLD
    cell.TopBorder = self.lineFormat
    cell.CellBackColor = tealScale[1]

  def write_column_total_content(self):
    # Get the sum of catssify values
    sum_dict = self.get_sum_occurrences()

    row_pos = self.addr.Row \
            + len(self.ensure_occurrences) + 1

    # Fill the cells horizontally
    for col, cats in enumerate(self.lookup_cats, start=1):
      col_pos = self.addr.Column + col

      cell = self.sheet_dst. \
        getCellByPosition(col_pos, row_pos)
      cell.Value = sum_dict[cats]

      cell.CharWeight = BOLD
      cell.HoriJustify = CENTER # or just 2
      cell.TopBorder = self.lineFormat
      cell.CellBackColor = tealScale[0]

  def write_column_total_grand(self):
    col_pos = self.addr.Column \
            + len(self.lookup_cats) + 1
    row_pos = self.addr.Row \
            + len(self.ensure_occurrences) + 1

    # Get the sum of catssify values
    sum_dict = self.get_sum_occurrences()

    cell = self.sheet_dst. \
      getCellByPosition(col_pos, row_pos)
    cell.Value = sum(sum_dict.values())

    cell.CharWeight = BOLD
    cell.HoriJustify = CENTER # or just 2
    cell.TopBorder = self.lineFormat
    cell.CellBackColor = tealScale[1]

  def process(self):
    self.build_records()
    self.prepare_sheet()

    self.write_column_headers()
    self.write_rows()
    self.write_column_total_header()
    self.write_column_total_content()
    self.write_column_total_grand()

def main():
  sample = PivotSample('Table', 'B', 'C',  'B2')
  sample.process()

