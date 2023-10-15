from datetime import datetime, timedelta
from pprint import pprint

class PivotSample:
  def __init__(self, col_date: str, col_cats: str) -> None:
    document = XSCRIPTCONTEXT.getDocument()
    self.sheet_src = document.Sheets["Example"]

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

  def get_formatted_date(self, excel_date):
    # Convert the number to a datetime object
    # Excel's epoch is two days off from the standard epoch
    excel_epoch = datetime(1899, 12, 30)
    date_obj = excel_epoch + timedelta(days=excel_date)

    # Format the datetime object as 'dd/mm/yyyy'
    return date_obj.strftime('%d/%m/%Y')

  def run(self):
    # range to be proceed
    # omit header and plus one for the last
    max_row = self.get_last_used_row()
    range_rows = range(2, max_row+1)

    print(f'Range  : {range_rows}')

    # retrieving all rows data
    all_values = [{
        'date' : int(self.sheet_src[f'{self.col_date}{row}'].Value),
        'cats' : self.sheet_src[f'{self.col_cats}{row}'].String
      } for row in range_rows]

    # print(all_values)
    # print()
    # {'date': 42830, 'cats': 'Banana'}

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

    # print(occurrences)
    # print()
    # 42830: {'Grape': 1, 'Banana': 1, 'Strawberry': 4, 'Apple': 3, 'Orange': 2, 'Mango': 2}

    # Get the list of class values from get_lookup_cls
    lookup_cats = self.get_lookup_cats()

    # Create a new dictionary with all class values
    # and their counts (zero if not found)
    ensure_occurrences = {
      date: {
        cats: row.get(cats, 0)
        for cats in lookup_cats
      }
      for date, row in occurrences.items()}

    for date, row in ensure_occurrences.items():
      formatted_date = self.get_formatted_date(date)
      print(f"  Date : {formatted_date}")
      print(f"  Cats : {row}")
      print()

    print()

def main():
  sample = PivotSample('B', 'C')
  sample.run()

"""
  Date : 05/04/2017
  Cats : {'Apple': 3, 'Banana': 1, 'Orange': 2, 'Grape': 1, 'Strawberry': 4, 'Durian': 0, 'Mango': 2, 'Dragon Fruit': 0}
"""
