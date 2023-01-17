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

  def __init__(self, baseline):
    # save initial parameter
    self.baseline = baseline

    # build initial data
    [self.start, self.end] = self.__get_month_rnd()
    self.__init_fakes()

  def __get_indices(self):
    return list(range(self.start, self.end+1))

  def __get_month_rnd(self):
    while True:
      start = randint(1, 12)
      end   = randint(start, 12)
      if end - start > 3: break
    return [start, end]

  def get_months_dict(self):
    m_all   = list(self.MONTHS.items())
    m_slice = m_all[self.start-1:self.end]
    return dict(m_slice)

  def __init_random(self):
    budget = self.baseline + randint(-20, 100)
    actual = self.baseline + randint(-50, 10)
    gap    = budget - actual

    return [budget, actual, gap]

  def __init_fakes(self):
    self.fakes = {}
    for key in self.__get_indices():
      self.fakes[key] = self.__init_random()

  def main(self):
    print(self.get_months_dict())
    print(self.fakes)

# Program Entry Point
month_data = MonthData(1500)
month_data.main()
