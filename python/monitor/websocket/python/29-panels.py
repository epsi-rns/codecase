import asyncio
import xl2web_25c, xl2web_25d
import log2panel_29, aioweb_29

from rich.live   import Live
from rich.panel  import Panel
from rich.layout import Layout

# Multi Rich Panel Class Example
class MultiPanels:
  def __make_layout(self):
    # Define the layout.
    self.layout = Layout(name="root")

    self.layout.split(
      Layout(name="top"),
      Layout(name="bottom"),
    )

    self.layout['top'].split_row(
      Layout(name="left"),
      Layout(name="right"),
    )

  def __get_layout_empty(self) -> Layout:
    self.layout['left'].update(
      self.watch_left.get_panel(None))
    self.layout['right'].update(
      self.watch_right.get_panel(None))
    return self.layout

  def __prepare_watcher(self):
    self.live = Live()

    self.watch_left = xl2web_25c.Xl2Web_c(
      'sheetGlobal', self.live, self.layout, 'left')

    self.watch_right = xl2web_25d.Xl2Web_d(
      'sheetDaily', self.live, self.layout, 'right')

    self.watch_log = log2panel_29.Log2Panel(
      self.live, self.layout, 'bottom')

  async def main(self):
    self.__make_layout()
    self.__prepare_watcher()

    with self.live:
      self.live.update(self.__get_layout_empty())

      task_web = aioweb_29.AIOWeb().task_web
      task_left = asyncio.create_task(
        self.watch_left.main())
      task_right = asyncio.create_task(
        self.watch_right.main())
      task_log = asyncio.create_task(
        self.watch_log.do_log())

      await(task_web())
      await(task_left)
      await(task_right)
      await(task_log)

# Program Entry Point
multi = MultiPanels()
try:
  asyncio.run(multi.main())
except KeyboardInterrupt:
  print('Goodbye!')