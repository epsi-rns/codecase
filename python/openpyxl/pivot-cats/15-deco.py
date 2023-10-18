#!/usr/bin/env python3

# openPyXL
from openpyxl import Workbook

# Local Library
from lib.TableSample   import TableSample
from lib.TableWriter15 import TableWriter

def main() -> None:
  file_source = 'sample_data.csv'
  file_target = 'Example.xlsx'

  table_sample = TableSample(file_source)
  table_sample.process()

  df_table = table_sample.get_df_table()

  wb = Workbook()
  ws = wb.active
  ws.title = 'Example'

  table_writer = TableWriter(df_table, ws)
  table_writer.process()

  # Save the file
  wb.save(file_target)

if __name__ == "__main__":
  main()









