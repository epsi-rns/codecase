#!/usr/bin/env python3

# Local Library
from lib.TableSample11 import TableSample
from lib.PivotSample11 import PivotSample

def main() -> None:
  source_csv = 'sample_data.csv'

  table_sample = TableSample(source_csv)
  table_sample.process()

  pivot_sample = PivotSample(table_sample.df_table)
  pivot_sample.process()

if __name__ == "__main__":
  main()

