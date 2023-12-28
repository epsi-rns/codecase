#!/usr/bin/env python3

import pandas as pd

# Local Library
from lib.TableSample import TableSample
from lib.PivotSample12 import PivotSample

def main() -> None:
  source_csv = 'sample-data.csv'
  categories = [
    "Apple", "Banana", "Dragon Fruit",
    "Durian", "Grape", "Mango",
    "Orange", "Strawberry"]

  pd.set_option('display.max_rows', 10)

  table_sample = TableSample(source_csv)
  table_sample.process()
  table_sample.display()

  pivot_sample = PivotSample(
    table_sample.get_df_table(), categories)
  pivot_sample.process()
  pivot_sample.display()

if __name__ == "__main__":
  main()

