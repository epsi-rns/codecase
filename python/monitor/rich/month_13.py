from random import randint
from rich import print

# Fake Data Generator Class 
class MonthData:
  MONTHS = {
    1: 'January',   2: 'February',
    3: 'March',     4: 'April',
    5: 'May',       6: 'June',
    7: 'July',      8: 'August',
    9: 'September', 10: 'October',
    11: 'November', 12: 'December'}

  def __init__(self):
    # save initial parameter
    [self.start, self.end] = self.__get_month_rnd()

  def __get_month_rnd(self):
    while True:
      start = randint(1, 12)
      end   = randint(start, 12)
      if end - start > 3: break
    return [start, end]

  def __get_months_dict(self):
    m_all   = list(self.MONTHS.items())
    m_slice = m_all[self.start:self.end]
    return dict(m_slice)

  def main(self):
    print(self.__get_months_dict())

# Program Entry Point
month_data = MonthData()
month_data.main()
