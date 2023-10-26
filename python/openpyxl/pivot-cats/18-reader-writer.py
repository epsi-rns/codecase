#!/usr/bin/env python3

# openPyXL
from openpyxl import Workbook, load_workbook

# Local Library
from lib.TableReader   import TableReader
from lib.PivotSampleTS import PivotSampleTS
from lib.PivotWriter   import PivotWriter

def main() -> None:
  file_source = 'Example2.xlsx'
  file_target = file_source

  columns = {
    'index' : 'A',
    'date'  : 'B',
    'cat'   : 'C'
  }

  categories = [
    "Apple", "Banana", "Dragon Fruit",
    "Durian", "Grape", "Mango",
    "Orange", "Strawberry"]

  wb = load_workbook(file_source)
  ws = wb['Table']

  table_reader = TableReader(ws, columns)
  table_reader.process()
  table_reader.display()
  df_table = table_reader.get_df_table()

  pivot_sample = PivotSampleTS(df_table, categories)
  pivot_sample.process()
  pivot_sample.display()
  df_pivot = pivot_sample.get_df_pivot()

  # Create a new sheet
  ws = wb.create_sheet(title='Pivot')
  wb.active = ws

  pivot_writer = PivotWriter(
    df_pivot, ws, categories, 'B2')
  pivot_writer.process()

  # Save the file
  wb.save(file_target)

if __name__ == "__main__":
  main()
