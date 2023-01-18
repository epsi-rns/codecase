import asyncio

from watchfiles import awatch

from rich.live   import Live
from rich.table  import Table
from rich.panel  import Panel
from rich.layout import Layout

# Dual Rich Panel Watchfiles Class Example
class DualWatch:
  filepath_cut   = '/home/epsi/awatch/'
  filepath_right = '/home/epsi/awatch/code-01-base'
  filepath_left  = '/home/epsi/awatch/code-02-enh'

  def make_layout(self):
    # Define the layout.
    self.layout = Layout(name="root")
    self.layout.split_row(
      Layout(name="left"),
      Layout(name="right"),
    )

  def generate_table(self, changes) -> Table:
    # Make a new table
    table = Table(expand=True)
    table.add_column("Type")
    table.add_column("File")

    if changes != None:
      for change in changes:
        short = change[1].replace(
          self.filepath_cut, '')
        table.add_row(
          *[str(change[0]), short])

    return table

  def get_panel(self, changes) -> Panel:
    dataTable = self.generate_table(changes)
    panel = Panel(
      dataTable, title="A Panel",
      subtitle="A [yellow]Thank you")
    return panel

  def get_layout(self, layout_name, changes) -> Layout:
    if layout_name == None:
      self.layout['left'].update(
        self.get_panel(None))
      self.layout['right'].update(
        self.get_panel(None))
    else:
      self.layout[layout_name].update(
        self.get_panel(changes))
    return self.layout

  async def do_left(self):
    with self.live:
      watchloop = awatch(
        self.filepath_left, recursive=True)

      async for changes in watchloop:
        self.live.update(
          self.get_layout('left', changes))

  async def do_right(self):
    with self.live:
      watchloop = awatch(
        self.filepath_right, recursive=True)

      async for changes in watchloop:
        self.live.update(
          self.get_layout('right', changes))

  async def main(self):
    self.make_layout()
    self.live = Live(self.get_layout(None, None))

    task_left = asyncio.create_task(
      self.do_left())
    task_right = asyncio.create_task(
      self.do_right())

    await(task_left)
    await(task_right)

# Program Entry Point
dual = DualWatch()
asyncio.run(dual.main())
