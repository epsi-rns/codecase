import asyncio_mqtt as aiomqtt
import asyncio
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

  async def main(self):
    client = aiomqtt.Client(
      hostname="localhost", port=1883)

    async with client:
      while True:
        self.update_num()
        await client.publish(
          "topic/signal",
          payload=str(self.current))
        await asyncio.sleep(1)

mqPub = mqPublisher()
asyncio.run(mqPub.main())
