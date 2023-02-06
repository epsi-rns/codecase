import asyncio
import xl2web_25c, xl2web_25d, log2panel_29

from rich.live   import Live
from rich.panel  import Panel
from rich.layout import Layout

# Dual Rich Panel Watchfiles Class Example
class MultiPanels:
  def make_layout(self):
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

  def get_layout_empty(self) -> Layout:
    self.layout['left'].update(
      self.watch_left.get_panel(None))
    self.layout['right'].update(
      self.watch_right.get_panel(None))
    return self.layout

  async def main(self):
    self.make_layout()
    self.live = Live()

    self.watch_left = xl2web_25c.Xl2Web_c(
      'sheetGlobal', self.live, self.layout, 'left')

    self.watch_right = xl2web_25d.Xl2Web_d(
      'sheetDaily', self.live, self.layout, 'right')

    self.watch_page = log2panel_29.Log2Panel(
      self.live, self.layout, 'bottom')

    with self.live:
      self.live.update(self.get_layout_empty())

      task_left = asyncio.create_task(
        self.watch_left.main())
      task_right = asyncio.create_task(
        self.watch_right.main())

      task_log = asyncio.create_task(
        self.watch_page.do_log())

      await(self.watch_page.task_web())

      await(task_left)
      await(task_right)
      await(task_log)

# Program Entry Point
multi = MultiPanels()
try:
  asyncio.run(multi.main())
except KeyboardInterrupt:
  print('Goodbye!')