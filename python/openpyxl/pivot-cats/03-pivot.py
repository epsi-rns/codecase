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

  def build_pivot(self) -> None:
    # Perform pivot operations
    try:
      # Grouping using list comprehension
      # keep the dictionary for further use
      self.all_dates = {
        row[1]: [item[2]
        for item in self.all_values
        if item[1] == row[1]]
          for row in self.all_values
      }

      pprint(self.all_dates)

      # Count occurrences by break into an array
      self.occurrences = {
        date: {cat: value.count(cat) for cat in set(value)}
        for date, row in self.all_dates.items()
        for value in [row]
      }

      pprint(self.occurrences)

      # Create a new dictionary with all class values
      # and their counts (zero if not found)
      self.ensure_occurrences = {
        date: {
          cat: pairs.get(cat, 0)
          for cat in self.categories
        }
        for date, pairs in self.occurrences.items()}

      pprint(self.ensure_occurrences)

    except Exception as e:
      print("An error occurred " \
        + f"while processing data: {e}")

  def display(self) -> None:
    pass

  def process(self):
    self.header = None
    self.load_data()
    self.build_pivot()

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
