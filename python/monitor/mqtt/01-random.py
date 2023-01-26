import numpy as np
import random
from time import sleep

class rndGenerator:
  def __init__(self):
    # save initial parameter
    self.lim_lower  =  5
    self.lim_upper  = 40
    self.num_normal = 21
    self.current    = self.num_normal

  def update_num(self):
    while True:
      neo = self.current
      neo += random.uniform(-5, 5)
      if self.lim_lower <= neo <= self.lim_upper:
        break

    self.current = neo

  def __call__(self):
    for i in range(0, 5):
      self.update_num()
      print("%.2f" % self.current)
      yield self.current
      sleep(0.2)


rndGen = rndGenerator()
numbers = np.array(list(rndGen()))

np.set_printoptions(precision=2)
print(numbers)
