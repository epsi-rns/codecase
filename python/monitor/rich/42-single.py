import asyncio

from watchfiles import awatch

from rich.live import Live
from rich.table import Table
from rich.panel import Panel

# Single Rich Panel Watchfiles Class Example
class SingleWatch:
  filepath = '/home/epsi/awatch/code-02-enh'

  def generate_table(self, changes) -> Table:
    # Make a new table
    table = Table(expand=True)
    table.add_column("Type")
    table.add_column("File")

    if changes != None:
      for change in changes:
        table.add_row(
          *[str(change[0]),change[1]])

    return table

  def get_panel(self, changes) -> Panel:
    dataTable = self.generate_table(changes)
    panel = Panel(
      dataTable, title="A Single Panel",
      subtitle="A single [yellow]Thank you")
    return panel

  async def main(self):
    with Live(
        self.get_panel(None),
        refresh_per_second=4
      ) as live:
        watchloop = awatch(
          self.filepath, recursive=True)
        async for changes in watchloop:
          live.update(self.get_panel(changes))

# Program Entry Point
single = SingleWatch()
asyncio.run(single.main())
