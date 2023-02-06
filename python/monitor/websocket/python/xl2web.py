import asyncio, websockets, json, os
from watchfiles import awatch

# Excel to Web, Base Class
class Xl2WebBase:
  def __init__(self, filepath, filename, site, port):
    # save initial parameter
    self.filepath = filepath
    self.filename = filename
    self.site = site
    self.port = port

    # websocket broadcast collection
    self.connections = set()

    # self.xlsx required in descendent class
    self.xlsx = None

  # websocket related
  async def __monitor_localfile(self):
    async for changes in awatch(self.filepath):
      self.xlsx = os.path.join(self.filepath, self.filename)
      for change in changes:
        if change[1] == self.xlsx:
          print(change[0])

          event_data = self._pack_data(self.xlsx)
          self._dump_data(event_data)

          websockets.broadcast(
            self.connections, json.dumps(event_data))

  async def __monitor_webclient(self, websocket):
    while True:
      try:
        message = await websocket.recv()
      except websockets.exceptions.ConnectionClosed:
         break

      self.xlsx = os.path.join(self.filepath, self.filename)

      event_data = self._pack_data(self.xlsx)
      self._dump_data(event_data)
      await websocket.send(
        json.dumps(event_data))

  # websocket handler
  async def __monitor_localfileconn(self, websocket):
    self.connections.add(websocket)
    try:
      await websocket.wait_closed()
    finally:
      self.connections.remove(websocket)

  async def __handler(self, websocket, path):
    task_localfile = asyncio.create_task(
      self.__monitor_localfileconn(websocket))

    task_webclient = asyncio.create_task(
      self.__monitor_webclient(websocket))

    # run these two coroutines concurrently
    await(task_localfile)
    await(task_webclient)

  async def main(self):
    # Start the server
    async with await websockets.serve(
      self.__handler, self.site, self.port):
        await self.__monitor_localfile()
