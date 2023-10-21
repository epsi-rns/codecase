import csv
from typing import List
from pprint import pprint

class PivotSample:
  def __init__(self, source_csv: str,
      categories: List[str]) -> None:

    # save initial parameter
    self.filename = source_csv
    self.categories = categories
    self.all_values = []

  def load_data(self) -> None:
    try:
      with open(self.filename,
          mode='r', newline='') as file:

        reader = csv.reader(file)

        # Read the header
        self.header = next(reader)

        # retrieving all rows data
        for row in reader:
          self.all_values.append(row)

    except FileNotFoundError:
      print("Error: The file "
        + f"'{self.filename}' was not found.")
    except Exception as e:
      print(f"An error occurred: {e}")

  def display(self) -> None:
    if self.header is None:
      print("No data to display.")
    else:
      # Display the header
      # ['Number', 'Date', 'Fruit']
      print(self.header)

      # Display the data
      # ['1', '19/02/2017', 'Orange']
      for row in self.all_values:
        print(row)

  def process(self):
    self.header = None
    self.load_data()

def main() -> None:
  source_csv = 'sample-data.csv'
  categories = [
    "Apple", "Banana", "Dragon Fruit",
    "Durian", "Grape", "Mango",
    "Orange", "Strawberry"]

  pv = PivotSample(source_csv, categories)
  pv.process()
  pv.display()

if __name__ == "__main__":
  main()
