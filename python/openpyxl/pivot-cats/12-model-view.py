#!/usr/bin/env python3

# Local Library
from lib.TableSample12 import TableSample
from lib.PivotSample12 import PivotSample

def main() -> None:
  source_csv = 'sample_data.csv'

  table_sample = TableSample(source_csv)
  table_sample.process()
  table_sample.display()

  pivot_sample = PivotSample(
    table_sample.get_df_table())
  pivot_sample.process()
  pivot_sample.display()

if __name__ == "__main__":
  main()









