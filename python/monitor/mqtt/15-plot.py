import paho.mqtt.client as mqtt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

from scipy import interpolate

# This is the Subscriber
class mqSubscriber:
  def __init__(self):
    # save initial parameter
    self.index = 0
    self.chart_setup()

  def chart_setup(self):
    self.xdata = []
    self.ydata = []

    self.fig, self.axes = plt.subplots()
    self.line, = self.axes.plot(
      self.xdata, self.ydata, 'r-')

    self.fig.canvas.mpl_connect(
      'close_event', exit)

  def update_line(self, new_num):
    self.index += 1
    self.xdata.append(self.index)
    self.ydata.append(new_num)

    if self.index <= 3:
      self.line.set_xdata(self.xdata)
      self.line.set_ydata(self.ydata)
    else:
      n = len(self.ydata)
      tck = interpolate.splrep(
        self.xdata, self.ydata, s=0)
      xfit = np.arange(0, n-1, np.pi/50)
      yfit = interpolate.splev(xfit, tck, der=0)

      self.line.set_xdata(xfit)
      self.line.set_ydata(yfit)

  def on_connect(self,
      client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/test")

  def on_message(self,
      client, userdata, msg):
    float_num = float(msg.payload.decode())

    self.update_line(float_num)

    # recompute the ax.dataLim
    # update ax.viewLim using the new dataLim
    self.axes.relim()
    self.axes.autoscale_view()

    # issue: steal focus
    plt.draw()
    
    # https://stackoverflow.com/questions/45729092/
    # make-interactive-matplotlib-window-not-pop-
    # to-front-on-each-update-windows-7
    self.fig.canvas.draw_idle()
    self.fig.canvas.start_event_loop(0.001)

    time.sleep(0.1)

  def main(self):
    plt.ion()
    plt.show()

    client = mqtt.Client()
    client.connect("localhost",1883,60)

    client.on_connect = self.on_connect
    client.on_message = self.on_message

    client.loop_forever()

mqSub = mqSubscriber()
mqSub.main()
