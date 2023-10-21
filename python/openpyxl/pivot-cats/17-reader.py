#!/usr/bin/env python3

# openPyXL
from openpyxl import Workbook, load_workbook

# Local Library
from lib.TableReader import TableReader

def main() -> None:
  file_source = 'Example.xlsx'

  columns = {
    'index' : 'A',
    'date'  : 'B',
    'cat'   : 'C'
  }

  wb = load_workbook(file_source)
  ws = wb['Table']

  table_reader = TableReader(ws, columns)
  table_reader.process()
  table_reader.display()

if __name__ == "__main__":
  main()
