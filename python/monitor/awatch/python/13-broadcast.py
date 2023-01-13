import asyncio, websockets
from watchfiles import awatch

# Excel to Web, Class Example
class Xl2WebExample:
  def __init__(self, filepath, filename, site, port):
    # save initial parameter
    self.filepath = filepath
    self.filename = filename
    self.site = site
    self.port = port
    self.connections = set()

  # websocket handler
  async def __broadcast_changes(self):
    async for changes in awatch(self.filepath):
      for change in changes:
        print(change[0])
        print(change[1])
        websockets.broadcast(
          self.connections, change[1])

  async def __handler(self, websocket):
    self.connections.add(websocket)
    try:
      await websocket.wait_closed()
    finally:
      self.connections.remove(websocket)

  async def main(self):
    # Start the server
    async with await websockets.serve(
      self.__handler, self.site, self.port):
        await self.__broadcast_changes()

# Program Entry Point
example = Xl2WebExample(
  '/home/epsi/awatch/code-01-base', 'test-a.xlsx',
  'localhost', 8765)
asyncio.run(example.main())
