# Local Library
from lib.helper import (
  get_desktop, create_calc_instance, get_file_path)
from lib.CSVReader import CSVReader
from lib.TableWriter import TableWriter

def main() -> int:
  source_csv  = 'sample-data.csv'

  csv_reader = CSVReader(source_csv)
  csv_reader.process()
  dataframe = csv_reader.dataframe

  # Getting the source sheet
  desktop   = get_desktop()
  document  = create_calc_instance(desktop)

  if document:
    table_writer = TableWriter(
      desktop, document, 'Table', dataframe)
    table_writer.process()

  return 0

if __name__ == "__main__":
  raise SystemExit(main())
