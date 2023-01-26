import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md

import pandas as pd
import numpy as np
import random

from datetime import datetime
from time     import sleep
from scipy    import interpolate

class rndGenerator:
  def __init__(self):
    # save initial parameter
    self.index = 0
    self.timeframe = pd.DataFrame({
      "time": [], "ftime": [], "temp": [] })

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
    print(new_str, end="\r", flush=True)

  def update_data(self):
    new_num  = self.current
    new_time = datetime.now()
    new_time_as_float = datetime.timestamp(new_time)

    new_pair = pd.DataFrame({
      "time" : new_time,
      "ftime": new_time_as_float,
      "temp" : new_num
    }, index=[self.index])

    self.print_new_pair(new_pair)

    self.index += 1
    self.timeframe = pd.concat(
      [self.timeframe, new_pair])

  def get_df_smooth(self):
    df_t = self.timeframe['ftime']   
    tck = interpolate.splrep(
        df_t, self.timeframe['temp'], s=0)
    xfit = np.arange(df_t[0], df_t.values[-1], 0.1)
    yfit = interpolate.splev(xfit, tck, der=0)
    tfit = [datetime.fromtimestamp(f) for f in xfit]

    return pd.DataFrame({
      "time": tfit,
      "temp": yfit
    })

  def __call__(self):
    for i in range(0, 10):
      self.update_num()
      self.update_data()
      sleep(0.25)
    print()
    
    self.timeframe.info()
    df_smooth = self.get_df_smooth()

    self.axes.plot(
      self.timeframe.time,
      self.timeframe.temp, 'ro')

    self.axes.plot(
      df_smooth.time,
      df_smooth.temp, '-b.')

    for tick in self.axes.get_xticklabels():
      tick.set_rotation(90)

    plt.show()

rndGen = rndGenerator()
rndGen()

