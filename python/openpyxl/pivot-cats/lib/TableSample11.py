import pandas as pd
from pandas import DataFrame

class TableSample:
  def __init__(self, filename: str) -> None:
    # save initial parameter
    self.filename = filename

  def process(self) -> None:
    # Load data into a DataFrame
    self.df_table = pd.read_csv(self.filename)

    # Display the header
    print("Header:", self.df_table.columns)

    # Display the data
    print("Data:")
    print(self.df_table)

