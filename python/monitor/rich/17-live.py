import month_15
import time

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

# Rich's Layout, Class Example
class LayoutExample:
  def __init__(self):
    # init month data
    self.month_data_left  = month_15.MonthData(1300)
    self.month_data_right = month_15.MonthData(1700)

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
      title="Left Table", expand=True)

    self.format_table(dataTable)

    self.month_data_left.update()
    rows = self.month_data_left.get_strings()
    for row in rows.values():
      dataTable.add_row(*row)
    
    panel = Panel(
      dataTable, title="Left Panel",
      subtitle="Left [yellow]Thank you")
    return panel

  def get_right_panel(self) -> Panel:
    dataTable = Table(
      "Month", "Budget", "Actual", "Gap",
      title="Right Table", expand=True)

    self.format_table(dataTable)

    self.month_data_right.update()
    rows = self.month_data_right.get_strings()
    for row in rows.values():
      dataTable.add_row(*row)
    
    panel = Panel(
      dataTable, title="Right Panel",
      subtitle="Right [blue]Thank you")
    return panel

  def update_layout(self):
    self.layout["left"].update(
      self.get_left_panel())
    self.layout["right"].update(
      self.get_right_panel())

  def main(self):
    self.make_layout()

    with Live(self.layout, transient=True):
       while True:
         self.update_layout()
         time.sleep(1)

# Program Entry Point
example = LayoutExample()
example.main()
