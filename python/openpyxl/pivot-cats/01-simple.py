import csv

class PivotSample:
  def __init__(self, filename: str) -> None:
    self.filename = filename

  def run(self) -> None:
    try:
      # Create a list to store the data
      all_values = []

      # Read the data from the CSV file
      with open(self.filename,
          mode='r', newline='') as file:

        reader = csv.reader(file)

        # Read the header
        header = next(reader)
        for row in reader:
          all_values.append(row)

      # Display the header
      print(header)

      # Display the data
      for row in all_values:
        print(row)

    except FileNotFoundError:
      print("Error: The file "
        + f"'{self.filename}' was not found.")
    except Exception as e:
      print(f"An error occurred: {e}")

def main() -> None:
  source_csv = 'sample-data.csv'

  pv = PivotSample(source_csv)
  pv.run()

if __name__ == "__main__":
  main()


