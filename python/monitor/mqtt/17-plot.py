import asyncio
from mq17Subscriber import mqSubscriber

mqSub = mqSubscriber()

try:
  asyncio.run(mqSub.main())
except KeyboardInterrupt:
  print("\nGoodbye!")