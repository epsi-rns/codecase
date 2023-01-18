import asyncio, datetime

from watchfiles import awatch

from rich.live   import Live
from rich.table  import Table
from rich.panel  import Panel
from rich.layout import Layout

class SingleWatch:
  def __init__(self, 
      ref_live, ref_layout, layout_name, filepath):
    self.live   = ref_live
    self.layout = ref_layout
    self.layout_name = layout_name
    self.filepath    = filepath

  def format_table(self, dataTable):
    c = dataTable.columns

    c[0].header_style = "bold blue"
    c[1].header_style = "bold green"

    c[0].style = "blue"
    c[1].style = "green"

  def generate_table(self, changes) -> Table:
    # Make a new table
    table = Table(expand=True)
    table.add_column("Type")
    table.add_column("File")

    self.format_table(table)

    if changes != None:
      for change in changes:
        short = change[1].replace(
          self.filepath, '')
        table.add_row(
          *[str(change[0]), short])

    return table

  def get_panel(self, changes) -> Panel:
    dataTable = self.generate_table(changes)

    message = Table.grid(padding=1, expand=True)
    message.add_column(no_wrap=True)
    cts = datetime.datetime.now()
    message.add_row(
      "Time Received: [yellow]" + str(cts))
    message.add_row(dataTable)

    panel = Panel(message, title=self.filepath)
    return panel

  def get_layout(self, changes) -> Layout:
    self.layout[self.layout_name].update(
      self.get_panel(changes))
    return self.layout

  async def do_task(self):
    with self.live:
      watchloop = awatch(
        self.filepath, recursive=True)

      async for changes in watchloop:
        self.live.update(
          self.get_layout(changes))

# Dual Rich Panel Watchfiles Class Example
class DualPanel:
  def make_layout(self):
    # Define the layout.
    self.layout = Layout(name="root")
    self.layout.split_row(
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
    self.live = Live(None)

    self.watch_left = SingleWatch(
      self.live, self.layout, 'left',
      '/home/epsi/awatch/code-01-base/')

    self.watch_right = SingleWatch(
      self.live, self.layout, 'right',
      '/home/epsi/awatch/code-02-enh/')

    self.live.update(self.get_layout_empty())

    task_left = asyncio.create_task(
      self.watch_left.do_task())
    task_right = asyncio.create_task(
      self.watch_right.do_task())

    await(task_left)
    await(task_right)

# Program Entry Point
dual = DualPanel()
try:
  asyncio.run(dual.main())
except KeyboardInterrupt:
  print('Goodbye!')