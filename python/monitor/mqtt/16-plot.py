import asyncio
import asyncio_mqtt  as aiomqtt

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md

import pandas as pd
import numpy  as np

from datetime import datetime, timedelta
from time     import sleep
from scipy    import interpolate

# This is the Subscriber
class mqSubscriber:
  # Maximum Buffered Data in Second
  MAX_DURATION = 40

  def __init__(self):
    # save initial parameter
    self.index = 0
    self.timeframe = pd.DataFrame({
      "time": [], "ftime": [], "temp": [] })

    self.lim_lower = 10
    self.lim_upper = 40

    self.lim_start = None
    self.lim_end   = None

    self.chart_setup()
    
  def chart_setup(self):
    self.fig, self.axes = plt.subplots()
    self.axes.set_ylim(
      self.lim_lower, self.lim_upper)

    xfmt = md.DateFormatter('%H:%M:%S')
    self.axes.xaxis.set_major_formatter(xfmt)
    plt.subplots_adjust(bottom=0.3)
    plt.xticks(rotation=90, ha='right')

    plt.title('Value by Time')
    plt.xlabel('Time')
    plt.ylabel('Value')

    self.axes.grid(
      which='major',
      color = '#004d40',
      linestyle = '--',
      linewidth = 0.8)

    self.axes.grid(
      which='minor',
      color = '#009688',
      linestyle = ':',
      linewidth = 0.4)

    self.axes.minorticks_on()

    self.line, = self.axes.plot(
      [], [], linestyle="None",
      marker='+', markerfacecolor='#00796b')
    self.smooth, = self.axes.plot(
      [], [], color='#1976d2')

    self.fig.canvas.mpl_connect(
      'close_event', exit)

  def update_limit(self, new_time, new_num):
    self.lim_lower = min(new_num, self.lim_lower)
    self.lim_upper = max(new_num, self.lim_upper)

    self.axes.set_ylim(
      self.lim_lower - 15, self.lim_upper + 10)

    self.lim_end = new_time
    if self.index <= 1:
      self.lim_start = new_time
    else:
      self.axes.set_xlim(
        self.lim_start - timedelta(seconds=1),
        self.lim_end   + timedelta(seconds=1))

  def build_df_smooth(self):
    df_t = self.timeframe['ftime']   
    tck = interpolate.splrep(
        df_t, self.timeframe['temp'], s=0)

    idx = self.timeframe.index
    fst = df_t[idx[0]]
    lst = df_t[idx[-1]]

    xfit = np.arange(fst, lst, 0.1)
    yfit = interpolate.splev(xfit, tck, der=0)
    tfit = [datetime.fromtimestamp(f) for f in xfit]

    self.df_smooth = pd.DataFrame({
      "time": tfit,
      "temp": yfit
    })

  def remove_old(self, new_time):
    # remove old data
    obsolete = new_time \
      - timedelta(seconds=self.MAX_DURATION)

    self.timeframe = self.timeframe\
      [self.timeframe.time >= obsolete]

    if self.index >= self.MAX_DURATION:
      self.lim_start = obsolete + timedelta(seconds=2)

  def update_data(self, msg):
    new_num  = float(msg.payload)
    new_time = datetime.now()
    new_time_as_float = datetime.timestamp(new_time)

    new_pair = pd.DataFrame({
      "time" : new_time,
      "ftime": new_time_as_float,
      "temp" : new_num
    }, index=[self.index])

    self.index += 1
    self.timeframe = pd.concat(
      [self.timeframe, new_pair])

    self.update_limit(new_time, new_num)
    self.remove_old(new_time)

  def update_view(self):
    if self.index > 3:
      self.build_df_smooth()
      self.line.set_xdata(self.timeframe.time)
      self.line.set_ydata(self.timeframe.temp)
      self.smooth.set_xdata(self.df_smooth.time)
      self.smooth.set_ydata(self.df_smooth.temp)

    # tips: not to steal focus
    plt.draw()
    self.fig.canvas.draw_idle()
    self.fig.canvas.start_event_loop(0.001)

    sleep(0.1)

  async def main(self):
    plt.ion()
    plt.show()

    client = aiomqtt.Client(
      hostname="localhost", port=1883)

    async with client:
      async with client.messages() as messages:
        await client.subscribe("topic/signal")
        async for message in messages:
          self.update_data(message)
          self.update_view()

mqSub = mqSubscriber()
asyncio.run(mqSub.main())
