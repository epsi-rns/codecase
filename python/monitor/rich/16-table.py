import month_15

from rich.console import Console
from rich.layout import Layout
from rich.padding import Padding
from rich.table import Table

# Rich's Layout, Class Example
class LayoutExample:
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

  def get_left_table(self) -> Table:
    dataTable = Table(
      "Month", "Budget", "Actual", "Gap",
      title="Left Table", expand=True)

    self.format_table(dataTable)

    month_data = month_15.MonthData(1300)
    rows = month_data.get_strings()

    for row in rows.values():
      dataTable.add_row(*row)
    
    return dataTable

  def get_right_table(self) -> Table:
    dataTable = Table(
      "Month", "Budget", "Actual", "Gap",
      title="Left Table", expand=True)

    self.format_table(dataTable)

    month_data = month_15.MonthData(1700)
    rows = month_data.get_strings()

    for row in rows.values():
      dataTable.add_row(*row)
    
    return dataTable

  def update_layout(self):
    self.layout["left"].update(
      Padding(self.get_left_table(), (1, 2)))
    self.layout["right"].update(
      Padding(self.get_right_table(), (1, 2)))

  def main(self):
    self.make_layout()
    self.update_layout()
    console = Console()
    console.print(self.layout)

# Program Entry Point
example = LayoutExample()
example.main()
