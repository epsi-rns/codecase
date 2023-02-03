import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md

from datetime import timedelta
from time     import sleep

class mqChart:
  def __init__(self, max_duration):
    # save initial parameter
    self.max_duration = max_duration

    self.lim_lower = 10
    self.lim_upper = 40

    self.lim_start = None
    self.lim_end   = None

    self.chart_setup()

    plt.ion()
    plt.show()

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

  def update_ylimit(self, new_num):
    self.lim_lower = min(new_num, self.lim_lower)
    self.lim_upper = max(new_num, self.lim_upper)

    self.axes.set_ylim(
      self.lim_lower - 15, self.lim_upper + 10)

  def update_xlimit(self, index, new_time):
    if index <= 1:
      self.lim_start = new_time
    else:
      self.lim_end = new_time

      obsolete = new_time \
        - timedelta(seconds=self.max_duration )

      if index > self.max_duration:
        self.lim_start = obsolete

      self.axes.set_xlim(
        self.lim_start - timedelta(seconds=1),
        self.lim_end   + timedelta(seconds=1))

      st = self.lim_start.strftime("%H:%M:%S")
      nd = self.lim_end.  strftime("%H:%M:%S")
      print("%d : %s - %s" % (index, st, nd),
        end="\r", flush=True)

  def update_view(self, index, timeframe, df_smooth):
    self.line.set_xdata(timeframe.time)
    self.line.set_ydata(timeframe.temp)

    if index > 3:
      self.smooth.set_xdata(df_smooth.time)
      self.smooth.set_ydata(df_smooth.temp)

    # tips: not to steal focus
    plt.draw()
    self.fig.canvas.draw_idle()
    self.fig.canvas.start_event_loop(0.001)

    sleep(0.1)