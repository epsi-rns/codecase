import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md

import pandas as pd
import numpy as np
import random

from time import sleep

class rndGenerator:
  def __init__(self):
    # save initial parameter
    self.index = 0
    self.timeframe = pd.DataFrame({
      "time": [], "temp": [] })

    self.chart_setup()
    self.number_setup()

  def chart_setup(self):
    self.fig, self.axes = plt.subplots()

    xfmt = md.DateFormatter('%H:%M:%S')
    self.axes.xaxis.set_major_formatter(xfmt)

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

  def print_new_pair(self, new_pair):
    if self.index == 0:
      new_str = new_pair.to_string(
        index=False)
    else:
      new_str = new_pair.to_string(
        index=False, header=False)
    print(new_str)

  def update_data(self):
    new_num  = self.current
    new_time = pd.Timestamp.now()

    new_pair = pd.DataFrame({
      "time": new_time,
      "temp": new_num
    }, index=[self.index])

    self.print_new_pair(new_pair)

    self.index += 1
    self.timeframe = pd.concat(
      [self.timeframe, new_pair])
    
  def __call__(self):
    for i in range(0, 40):
      self.update_num()
      self.update_data()
      sleep(0.25)

    self.timeframe.info()

    plt.plot(
      self.timeframe.time,
      self.timeframe.temp)
 
    plt.xticks(rotation=90, ha='right')
    plt.title('Value by Time')

    plt.xlabel('Time')
    plt.ylabel('Value')

    plt.show()

rndGen = rndGenerator()
rndGen()

