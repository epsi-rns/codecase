import asyncio_mqtt as aiomqtt
import asyncio
import pandas as pd

# This is the Subscriber
class mqSubscriber:
  def __init__(self):
    # save initial parameter
    self.index = 0
    self.timeframe = pd.DataFrame({
      "time": [], "temp": []  })

  def print_new_pair(self, new_pair):
    if self.index == 0:
      new_str = new_pair.to_string(
        index=False)
    else:
      new_str = new_pair.to_string(
        index=False, header=False)
    print(new_str, end="\r", flush=True)

  def update(self, msg):
    new_pair =  pd.DataFrame({
      "time": pd.Timestamp.now(),
      "temp": float(msg.payload)
    }, index=[self.index])

    self.print_new_pair(new_pair)

    self.index += 1
    self.timeframe = pd.concat(
      [self.timeframe, new_pair])

  async def main(self):
    client = aiomqtt.Client(
      hostname="localhost", port=1883)

    async with client:
      async with client.messages() as messages:
        await client.subscribe("topic/signal")
        async for message in messages:
          self.update(message)

mqSub = mqSubscriber()

try:
  asyncio.run(mqSub.main())
except KeyboardInterrupt:
  print('Goodbye!')