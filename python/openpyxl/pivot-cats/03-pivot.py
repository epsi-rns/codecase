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

      # Count occurrences by break into an array
      self.occurrences = {
        date: {cat: value.count(cat) for cat in set(value)}
        for date, row in self.all_dates.items()
        for value in [row]
      }

      # Create a new dictionary with all class values
      # and their counts (zero if not found)
      self.ensure_occurrences = {
        date: {
          cat: pairs.get(cat, 0)
          for cat in self.categories
        }
        for date, pairs in self.occurrences.items()}

    except Exception as e:
      print("An error occurred " \
        + f"while processing data: {e}")

  def display_basic(self) -> None:
    # Display the header
    # ['Number', 'Date', 'Fruit']
    print(self.header)

    # Display the data
    # ['1', '19/02/2017', 'Orange']
    for row in self.all_values:
      print(row)

    print()

  def display_process(self) -> None:
      # '19/02/2017': ['Orange', 'Grape', 'Strawberry', 'Orange',
      #   'Apple', 'Banana', 'Strawberry', 'Banana', 'Strawberry']
      print(self.all_dates)
      print()

      # '19/02/2017': {'Mango': 2, 'Banana': 3, 'Apple': 1,
      #   'Strawberry': 4, 'Grape': 2, 'Orange': 3}
      print(self.occurrences)
      print()

      # {'19/02/2017': {'Apple': 1, 'Banana': 3, 'Dragon Fruit': 0,
      #   'Durian': 0, 'Grape': 2, 'Mango': 2,
      #  'Orange': 3, 'Strawberry': 4}
      print(self.ensure_occurrences)
      print()

  def display_pivot_header(self) -> None:
    # Create a header row
    line_title = "Date/Fruit"
    for cat in self.categories:
       line_title += f"\t{cat}"

    line_title += f"\tSub Total"
    print(line_title)

  def display_pivot_rows(self) -> None:
    # Create rows for each category
    for date, pairs in \
        self.ensure_occurrences.items():
      line_row = f"{date}"

      for cat, count in pairs.items():
        line_row += f"\t{count}"

      # Calculate the total for each column
      total = sum(pairs.values())
      line_row += f"\t{total}"

      print(line_row)

  def display_pivot_total(self) -> None:
    # Create a total row: sum of the column
    line_total = "Grand Total"
    total = {}

    for cat in self.categories:
      total[cat] = 0

      for date, pairs in \
          self.ensure_occurrences.items():
        total[cat] += pairs[cat]

      line_total += f"\t{total[cat]}"

    line_total += f"\t{sum(total.values())}"
    print(line_total)


  def display(self) -> None:
    if self.header is None:
      print("No data to display.")
    else:
      # self.display_basic()
      # self.display_process()

      self.display_pivot_header()
      self.display_pivot_rows()
      self.display_pivot_total()

  def process(self):
    self.header = None
    self.load_data()
    self.build_pivot()

def main() -> None:
  source_csv = 'sample_data.csv'
  categories = [
    "Apple", "Banana", "Dragon Fruit",
    "Durian", "Grape", "Mango",
    "Orange", "Strawberry"]

  pv = PivotSample(source_csv, categories)
  pv.process()
  pv.display()

if __name__ == "__main__":
  main()
