from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

# Rich's Layout, Class Example
class LayoutExample:
  def make_layout(self):
    # Define the layout
    self.layout = Layout(name="root")

    self.layout.split(
      Layout(name="header", size=3),
      Layout(name="body", ratio=1))

  def update_layout(self):
    self.layout["header"].update(Panel(
      "Hello, [blue]World!",
      title="Welcome",
      subtitle="[yellow]Thank you"))
    self.layout["body"].update(Panel(
      "Hello, [red]World!",
      title="Welcome",
      subtitle="Thank you"))

  def main(self):
    self.make_layout()
    self.update_layout()
    console = Console()
    console.print(self.layout)

# Program Entry Point
example = LayoutExample()
example.main()
