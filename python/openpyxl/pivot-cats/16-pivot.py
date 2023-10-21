#!/usr/bin/env python3

# openPyXL
from openpyxl import Workbook

# Local Library
from lib.TableSample import TableSample
from lib.PivotSample import PivotSample
from lib.TableWriter import TableWriter
from lib.PivotWriter import PivotWriter

def main() -> None:
  file_source = 'sample-data.csv'
  file_target = 'Example.xlsx'

  categories = [
    "Apple", "Banana", "Dragon Fruit",
    "Durian", "Grape", "Mango",
    "Orange", "Strawberry"]

  table_sample = TableSample(file_source)
  table_sample.process()
  table_sample.display()
  df_table = table_sample.get_df_table()

  pivot_sample = PivotSample(df_table, categories)
  pivot_sample.process()
  pivot_sample.display()
  df_pivot = pivot_sample.get_df_pivot()

  wb = Workbook()
  ws = wb.active
  ws.title = 'Table'

  table_writer = TableWriter(df_table, ws)
  table_writer.process()

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






