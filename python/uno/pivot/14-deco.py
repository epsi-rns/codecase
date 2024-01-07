import pandas as pd

# Local Library
from lib.helper import (
  get_desktop, open_document, get_file_path)
from lib.PivotReader   import PivotReader
from lib.PivotWriter14 import PivotWriter

def main() -> int:
  columns = {
    'index' : 'A',
    'date'  : 'B',
    'cat'   : 'C'
  }

  categories = [
    "Apple", "Banana", "Dragon Fruit",
    "Durian", "Grape", "Mango",
    "Orange", "Strawberry"]

  pd.set_option('display.max_rows', 10)
  pd.set_option('display.max_columns', 5)

  # Getting the source sheet
  file_path = get_file_path('Example.ods')
  desktop   = get_desktop()
  document  = open_document(desktop, file_path)

  if document:
    reader = PivotReader(document,
      'Table', columns, categories)
    pivot_table = reader.get_pivot()
  
    # Print the newly created pivot table
    # on terminal console for monitoring
    print(pivot_table)
    print()
  
    writer = PivotWriter(document,
      'Pivot', pivot_table, categories, 'B2')
    writer.process()

  return 0

if __name__ == "__main__":
  raise SystemExit(main())

