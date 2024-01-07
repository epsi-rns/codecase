# Local Library
from lib.helper import (
  get_desktop, create_calc_instance, get_file_path)
from lib.PivotSample import PivotSample
from lib.TableWriter import TableWriter
from lib.PivotWriter import PivotWriter

def main() -> int:
  source_csv  = 'sample-data.csv'

  categories = [
    "Apple", "Banana", "Dragon Fruit",
    "Durian", "Grape", "Mango",
    "Orange", "Strawberry"]

  pivot_sample = PivotSample(source_csv, categories)
  pivot_sample.process()
  dataframe   = pivot_sample.get_dataframe()
  pivot_table = pivot_sample.get_pivot()

  # Print the newly created pivot table on console 
  print(pivot_table)
  print()  

  # Getting the source sheet
  desktop   = get_desktop()
  document  = create_calc_instance(desktop)

  if document:
    table_writer = TableWriter(document, 
      'Table', dataframe)
    table_writer.process()

    writer = PivotWriter(document, 
      'Pivot', pivot_table, categories, 'B2')
    writer.process()

  return 0

if __name__ == "__main__":
  raise SystemExit(main())

