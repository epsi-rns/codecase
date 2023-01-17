import month_15
import asyncio
import datetime;

from random import randint

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

# Rich's Layout, Class Example
class LayoutExample:
  def __init__(self):
    # init month data
    self.month_data_left  = \
      month_15.MonthData(1000 + randint(0, 1000))
    self.month_data_right = \
      month_15.MonthData(1000 + randint(0, 1000))

  def make_layout(self):
    # Define the layout
    self.layout = Layout(name="root")

    self.layout.split_row(
      Layout(name="left"),
      Layout(name="right"))

  def format_table(self, dataTable):
    c = dataTable.columns

    c[1].header_style = "bold blue"
    c[2].header_style = "bold green"
    c[3].header_style = "bold yellow"  

    c[0].style = "bold"
    c[1].style = "blue"
    c[2].style = "green"
    c[3].style = "yellow"  

  def get_left_panel(self) -> Panel:
    dataTable = Table(
      "Month", "Budget", "Actual", "Gap",
      expand=True)

    self.format_table(dataTable)

    self.month_data_left.update()
    rows = self.month_data_left.get_strings()
    for row in rows.values():
      dataTable.add_row(*row)

    message = Table.grid(padding=1, expand=True)
    message.add_column(no_wrap=True)
    cts = datetime.datetime.now()
    message.add_row(
      "Time Received: [yellow]" + str(cts))
    message.add_row(dataTable)

    panel = Panel(
      message, title="Left Panel",
      subtitle="Left [yellow]Report")
    return panel

  def get_right_panel(self) -> Panel:
    dataTable = Table(
      "Month", "Budget", "Actual", "Gap",
      expand=True)

    self.format_table(dataTable)

    self.month_data_right.update()
    rows = self.month_data_right.get_strings()
    for row in rows.values():
      dataTable.add_row(*row)

    message = Table.grid(padding=1, expand=True)
    message.add_column(no_wrap=True)
    cts = datetime.datetime.now()
    message.add_row(
      "Time Received: [blue]" + str(cts))
    message.add_row(dataTable)

    panel = Panel(
      message, title="Right Panel",
      subtitle="Right [blue]Report")
    return panel

  async def do_left(self):
    while True:
      self.layout["left"].update(
        self.get_left_panel())
      await asyncio.sleep(1.1)

  async def do_right(self):
    while True:
      self.layout["right"].update(
        self.get_right_panel())
      await asyncio.sleep(1.3)

  async def main(self):
    self.make_layout()

    with Live(self.layout, transient=True):
      task_left = asyncio.create_task(
        self.do_left())
      task_right = asyncio.create_task(
        self.do_right())

      await(task_left)
      await(task_right)

# Program Entry Point
example = LayoutExample()
asyncio.run(example.main())
