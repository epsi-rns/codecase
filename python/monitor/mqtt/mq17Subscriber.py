import asyncio
import asyncio_mqtt as aiomqtt

from datetime      import datetime
from mq17Chart     import mqChart
from mq17DataFrame import mqDataFrame

# This is the Subscriber
class mqSubscriber:
  # Maximum Buffered Data in Second
  MAX_DURATION = 40

  def __init__(self):
    # save initial parameter
    self.index = 0

    self.mqCha = mqChart(self.MAX_DURATION)
    self.mqDfr = mqDataFrame(self.MAX_DURATION)

  def update(self, new_num):
    new_time = datetime.now()
    self.mqDfr.update_data(
        self.index, new_num, new_time)
    self.index += 1

    if self.index > 3:
      self.mqDfr.build_df_smooth()
      self.mqDfr.remove_old(self.index, new_time)

    self.mqCha.update_ylimit(new_num)

    self.mqCha.update_xlimit(
      self.index, new_time)

    self.mqCha.update_view(
      self.index,
      self.mqDfr.get_timeframe(),
      self.mqDfr.get_df_smooth())

  async def main(self):
    client = aiomqtt.Client(
      hostname="localhost", port=1883)

    async with client:
      async with client.messages() as messages:
        await client.subscribe("topic/signal")

        async for message in messages:
          new_num = float(message.payload)
          self.update(new_num)

