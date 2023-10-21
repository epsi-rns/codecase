from datetime import datetime, timedelta
from pprint import pprint

class PivotSample:
  def __init__(self,
      sheetSourceName: str,
      col_date: str, col_cats: str) -> None:
    document = XSCRIPTCONTEXT.getDocument()
    self.sheet_src = document.Sheets[sheetSourceName]

    self.col_date = col_date
    self.col_cats = col_cats

  def get_lookup_cats(self):
    return ["Apple", "Banana", "Orange", "Grape",
      "Strawberry", "Durian", "Mango", "Dragon Fruit"]

  def get_last_used_row(self):
    cursor = self.sheet_src.createCursor()
    cursor.gotoEndOfUsedArea(False)
    cursor.gotoStartOfUsedArea(True)
    rows = cursor.getRows()
    
    return len(rows)

  def prepare_sheet(self):
    document   = XSCRIPTCONTEXT.getDocument()
    sheets_dst = document.Sheets
    if not sheets_dst.hasByName('Pivot'):
      sheets_dst.insertNewByName('Pivot', 1)
    self.sheet_dst = sheets_dst['Pivot']

    desktop    = XSCRIPTCONTEXT.getDesktop()
    model      = desktop.getCurrentComponent()
    controller = model.getCurrentController()
    controller.setActiveSheet(self.sheet_dst)

    self.numberfmt = model.NumberFormats
    self.locale    = model.CharLocale

    self.dateFormat = self.numberfmt. \
      getStandardFormat(2, self.locale)

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

    # Get the list of class values
    lookup_cats = self.get_lookup_cats()

    # Create a new dictionary with all class values
    # and their counts (zero if not found)
    ensure_occurrences = {
      date: {
        cats: row.get(cats, 0)
        for cats in lookup_cats
      }
      for date, row in occurrences.items()}

    self.ensure_occurrences = ensure_occurrences

  def process(self):
    self.build_records()
    self.prepare_sheet()

    # Get the list of classify values
    lookup_cats = self.get_lookup_cats()

    # Assuming you want to start filling from cell B4 horizontally
    start_cell = 'B4'
    addr = self.sheet_dst[start_cell].CellAddress

    # Fill the cells horizontally
    for col, cats in enumerate(lookup_cats, start=1):
      col_pos = addr.Column + col

      cell = self.sheet_dst. \
        getCellByPosition(col_pos, addr.Row)
      cell.String = cats

    row_index = 0
    for date, row in self.ensure_occurrences.items():
      row_index += 1
      row_pos = addr.Row + row_index

      formatted_date = self.get_formatted_date(date)
      print(f"  Date : {formatted_date}")

      cell = self.sheet_dst. \
        getCellByPosition(addr.Column, row_pos)
      cell.String = formatted_date
      cell.Value = date
      cell.NumberFormat = self.dateFormat

      for col, cats in enumerate(lookup_cats, start=1):
        col_pos = addr.Column + col

        cell = self.sheet_dst. \
          getCellByPosition(col_pos, row_pos)
        cell.Value = row[cats]

def main():
  sample = PivotSample('Table', 'B', 'C')
  sample.process()

