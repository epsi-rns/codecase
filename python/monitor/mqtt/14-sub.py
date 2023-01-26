import asyncio_mqtt  as aiomqtt
import asyncio
import pandas as pd

# This is the Subscriber
class mqSubscriber:
  def __init__(self):
    # save initial parameter
    self.index = 0
    self.timeframe = pd.DataFrame({
      "time": [], "temp": []  })

  def update(self, msg):
    new_pair =  pd.DataFrame({
      "time": pd.Timestamp.now(),
      "temp": float(msg.payload)
    }, index=[self.index])

    if self.index == 0:
      new_str = new_pair.to_string(
        index=False)
    else:
      new_str = new_pair.to_string(
        index=False, header=False)

    print(new_str)
    self.index += 1

    self.timeframe = pd.concat(
      [self.timeframe, new_pair])

  async def main(self):
    client = aiomqtt.Client(
      hostname="localhost", port=1883)

    async with client:
      async with client.messages() as messages:
        await client.subscribe("topic/test")
        async for message in messages:
          self.update(message)

mqSub = mqSubscriber()
asyncio.run(mqSub.main())
