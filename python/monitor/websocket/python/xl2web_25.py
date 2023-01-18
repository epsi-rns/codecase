import asyncio, websockets, json, os, tomli

from watchfiles  import awatch
from rich.layout import Layout
from rich.panel  import Panel
from rich.table  import Table

# Excel to Web, Asbtract Base Class
class Xl2Web:
  def __init__(self, sheet_ident, 
      ref_live, ref_layout, layout_name):
    with open('config.toml', 'rb') as file_obj:
      config_root  = tomli.load(file_obj)
      env          = config_root['environment']
      config_env   = config_root[env]
      config_sheet = config_env[sheet_ident]

      # save initial parameter
      self.filepath = config_sheet['path']
      self.filename = config_sheet['file']
      self.site = config_sheet['site']
      self.port = config_sheet['port']

    # websocket broadcast collection
    self.connections = set()

    # openpyxl: required in descendent class
    self.xlsx = None

    # rich: required in descendent class
    self.live   = ref_live
    self.layout = ref_layout
    self.layout_name = layout_name

  # Rich TUI related
  def _dump_data(self, data):
    self.live.update(
      self.get_layout(data))

  def get_layout(self, data) -> Layout:
    self.layout[self.layout_name].update(
      self.get_panel(data))
    return self.layout

  def get_panel(self, data) -> Panel:
    message = Table.grid(padding=1, expand=True)
    message.add_column(no_wrap=True)

    if data != None:
      message.add_row(
        "Timestamp     : %s" % data["timestamp"])
      message.add_row(
        "File Modified : %s" % data["file"])
      message.add_row(self.generate_table(data))

    panel = Panel(message, title=self.filepath)
    return panel

  # Websocket related
  async def __monitor_localfile(self):
    async for changes in awatch(self.filepath):
      self.xlsx = os.path.join(self.filepath, self.filename)
      for change in changes:
        if change[1] == self.xlsx:
          print(change[0])
          print(change[1])

          event_data = self._pack_data(self.xlsx)
          self._dump_data(event_data)

          websockets.broadcast(
            self.connections, json.dumps(event_data))

  async def __monitor_webclient(self, websocket):
    while True:
      message = await websocket.recv()
      self.xlsx = os.path.join(self.filepath, self.filename)

      event_data = self._pack_data(self.xlsx)
      self._dump_data(event_data)
      await websocket.send(
        json.dumps(event_data))

      await self.__send_data(self.xlsx)

  # Websocket handler
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
