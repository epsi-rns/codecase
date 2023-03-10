import pandas as pd
import numpy as np
import random

from time import sleep

class rndGenerator:
  def __init__(self):
    # save initial parameter
    self.index = 0
    self.timeframe = pd.DataFrame({
      "time": [], "temp": []  })

    self.number_setup()

  def number_setup(self):
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

  def update_data(self):
    new_num  = self.current
    new_time = pd.Timestamp.now()

    new_pair = pd.DataFrame({
      "time": new_time,
      "temp": new_num
    }, index=[self.index])

    self.index += 1
    self.timeframe = pd.concat(
      [self.timeframe, new_pair])
    
  def __call__(self):
    for i in range(0, 5):
      self.update_num()
      self.update_data()

    return self.timeframe

np.set_printoptions(precision=2)
rndGen = rndGenerator()
print(rndGen())
