import pandas as pd
from datetime import datetime, timedelta

class CSVReader:
  def __init__(self, filename: str) -> None:

    # save initial parameter
    self.filename = filename

  def date_ordinal(self, value, format_source):
    # Offset of the date value
    # for the date of 1900-01-00
    offset = 693594

    date_value = datetime.strptime(
                   value, format_source)
    return date_value.toordinal() - offset

  def load_data(self):
    try:
      # Load data into a DataFrame
      self.dataframe = pd.read_csv(self.filename)

      # Define the format of the original date in CSV
      format_source = '%d/%m/%Y'

      # Apply the date_ordinal function
      # to the "Date" column
      self.dataframe['Date'] = self.dataframe['Date'].\
        apply(lambda date: self.date_ordinal(
          date, format_source))

      print("Data:")
      print(self.dataframe)

    except FileNotFoundError:
      print("Error: The file "\
        + f"'{self.filename}' was not found.")
    except Exception as e:
      print("An error occurred "
         + f"while loading data: {e}")

  def process(self) -> None:
    self.load_data()

