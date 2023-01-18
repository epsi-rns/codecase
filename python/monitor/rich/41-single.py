import asyncio

from watchfiles import awatch

from rich.live import Live
from rich.table import Table

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

  async def main(self):
    with Live(None, refresh_per_second=4) as live:
      watchloop = awatch(
        self.filepath, recursive=True)
      async for changes in watchloop:
        live.update(self.generate_table(changes))

# Program Entry Point
single = SingleWatch()
asyncio.run(single.main())