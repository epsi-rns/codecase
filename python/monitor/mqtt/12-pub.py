import paho.mqtt.client as mqtt
import asyncio
import random
from aioconsole import ainput

# This is the Publisher
class mqPublisher:
  def __init__(self):
    # save initial parameter
    self.lim_lower  =  5
    self.lim_upper  = 70
    self.num_normal = 21
    self.current    = self.num_normal

    self.client = mqtt.Client()
    self.client.connect("localhost",1883,60)

  def update_num(self):
    while True:
      neo = self.current
      neo += random.uniform(-1, 1)
      if self.lim_lower <= neo <= self.lim_upper:
        break

    self.current = neo

  def set_within(self, num):
    if num < self.lim_lower:
       num = self.lim_lower 
    if num > self.lim_upper:
       num = self.lim_upper
    return num

  async def do_produce(self):
    while True:
      self.update_num()
      self.client.publish(
        "topic/test", str(self.current))
    
      await asyncio.sleep(1)

  async def do_adjust(self):
    while True:

      float_num = float(
        await ainput('Adjustment: '))
      float_num = self.set_within(float_num)
      print("Adjust to: %.2f" % float_num) 

      while abs(self.current - float_num) >  1:
        self.current = (self.current + float_num)/2
        await asyncio.sleep(1)


  async def main(self):
    task_produce = asyncio.create_task(
      self.do_produce())
    task_adjust = asyncio.create_task(
      self.do_adjust())

    await(task_produce)
    await(task_adjust)

mqPub = mqPublisher()
asyncio.run(mqPub.main())
