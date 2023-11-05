import pandas as pd

# Local Library
from lib.helper import (
  open_document, get_file_path)
from lib.PivotReader11 import PivotReader

def main() -> int:
  columns = {
    'index' : 'A',
    'date'  : 'B',
    'cat'   : 'C'
  }

  pd.set_option('display.max_rows', 10)

  # Getting the source sheet
  file_path = get_file_path('Example.ods')
  document = open_document(file_path)

  if document:
    reader = PivotReader(
      document, 'Table', columns)
    reader.process()
  
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
