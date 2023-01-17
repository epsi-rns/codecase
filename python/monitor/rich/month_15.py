from random import randint

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

  def __update_month_rnd(self):
    while True:
      if randint(0, 1):
        self.start = self.start + randint(-1, 1)
        if self.start < 1: self.start = 1
      else:
        self.end   = self.end   + randint(-1, 1)
        if self.end > 12: self.end = 12
      if self.end - self.start > 3: break

  def __get_months_dict(self):
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

  def __update_fakes(self):
    # remove key
    unwanted = set(self.fakes.keys()) \
             - set(self.__get_indices())
    for key in unwanted:
      self.fakes.pop(key, None)

    # add key
    wanted = set(self.__get_indices()) \
           - set(self.fakes.keys())
    for key in wanted:
      self.fakes[key] = self.__init_random()

  def __update_fakes_value(self):
    for key in self.__get_indices():
      [budget, actual, gap] = self.fakes[key]

      actual = actual + randint(-10, 10)
      gap    = budget - actual

      self.fakes[key] = [budget, actual, gap]

  def get_strings(self):
    rows = {}
    for key in self.__get_indices():
      [budget, actual, gap] = self.fakes[key]
      rows[key] = [self.MONTHS[key],
        str(budget), str(actual), str(gap)]
    return rows

  def update(self):
    self.__update_month_rnd()
    self.__update_fakes()
    self.__update_fakes_value()
