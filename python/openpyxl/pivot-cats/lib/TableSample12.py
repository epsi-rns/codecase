import pandas as pd
from pandas import DataFrame

class TableSample:
  def __init__(self, filename: str) -> None:
    # save initial parameter
    self.filename = filename

  def load_data(self):
    try:
      # Load data into a DataFrame
      self.df_table = pd.read_csv(self.filename)

    except FileNotFoundError:
      print("Error: The file "\
        + f"'{self.filename}' was not found.")
    except Exception as e:
      print("An error occurred "
         + f"while loading data: {e}")

  def get_df_table(self) -> DataFrame:
    return self.df_table

  def process(self) -> None:
    self.load_data()

  def display(self) -> None:
    # Display the header
    print("Header:", self.df_table.columns)

    # Display the data
    print("Data:")
    print(self.df_table)
