import month_15
from rich import print

# Program Entry Point
month_data = month_15.MonthData(1300)
print(month_data.get_strings())

for c in range(1, 5+1):
  month_data.update()
  print(month_data.get_strings())