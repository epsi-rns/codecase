import asyncio_mqtt as aiomqtt
import asyncio

# This is the Subscriber
class mqSubscriber:
  def update(self, msg):
    float_num = float(msg.payload)
    print("%.2f" % float_num)

  async def main(self):
    client = aiomqtt.Client(
      hostname="localhost", port=1883)

    async with client:
      async with client.messages() as messages:
        await client.subscribe("topic/signal")
        async for message in messages:
          self.update(message)

mqSub = mqSubscriber()
asyncio.run(mqSub.main())
