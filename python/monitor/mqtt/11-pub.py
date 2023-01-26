import paho.mqtt.client as mqtt
import random

from time import sleep

# This is the Publisher
class mqPublisher:
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

  def main(self):
    client = mqtt.Client()
    client.connect("localhost",1883,60)

    while True:
      self.update_num()
      client.publish(
        "topic/test", str(self.current))
    
      sleep(1)

    client.disconnect();

mqPub = mqPublisher()
mqPub.main()
