import csv, random
from datetime import datetime, timedelta
from pprint import pprint

# Define the date range for one and a half months
start_date = datetime(2017, 2, 19)
end_date = start_date + timedelta(days=45)

# Define categories
categories = ["Apple", "Banana", "Orange",
  "Grape", "Strawberry", "Durian", "Mango", "Dragon Fruit"]

# Categories to simulate zero counts for
zero_count_categories = ["Durian", "Dragon Fruit"]

# Create a list to store the data
data = []

# Generate random data for a thousand rows
# within a specified date range
for i in range(1, 1001):
  current_date = start_date \
    + timedelta(days=random.randint(0, 45))

  # Randomly select a category
  category = random.choice(categories)

  # Check if the category is one
  # of the zero count categories
  if category in zero_count_categories:
    # Simulate zero count by skipping
    continue

  # Append the data to the list
  data.append([
    current_date.strftime("%d/%m/%Y"), category])

# Sort the data by date
data.sort(
  key=lambda x: datetime.strptime(x[0],
  "%d/%m/%Y"))

# Add a numbering column
for i, row in enumerate(data):
  # Add the numbering column
  row.insert(0, i + 1)

# Add a header
header = ["Number", "Date", "Fruit"]

# Write the data to a CSV file with header
with open('sample_data.csv',
    mode='w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(header)
  writer.writerows(data)

print("Sample data has been generated "
  + "and saved to 'sample_data.csv'.")

