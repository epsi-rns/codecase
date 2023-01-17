from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

# Rich's Layout, Class Example
class LayoutExample:
  def make_layout(self):
    # Define the layout
    self.layout = Layout(name="root")

    self.layout.split_row(
      Layout(name="left"),
      Layout(name="right"))

  def get_left_panel(self) -> Panel:
    panel = Panel(
      "Hello, [blue]World!",
      title="Welcome",
      subtitle="[yellow]Thank you")
    return panel

  def get_right_panel(self) -> Panel:
    panel = Panel(
      "Hello, [red]World!",
      title="Welcome",
      subtitle="Thank you")
    return panel

  def update_layout(self):
    self.layout["left"] \
      .update(self.get_left_panel())
    self.layout["right"] \
      .update(self.get_right_panel())    

  def main(self):
    self.make_layout()
    self.update_layout()
    console = Console()
    console.print(self.layout)

# Program Entry Point
example = LayoutExample()
example.main()
