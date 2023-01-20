import logging, asyncio
import jinja2, aiohttp_jinja2

from aiohttp import web
from io import StringIO

from rich.console import Console
from rich.text    import Text
from rich.table   import Table
from rich.panel   import Panel
from rich.layout  import Layout
from rich.live    import Live

@aiohttp_jinja2.template("index.jinja")
class HomeHandler(web.View):

  async def get(self):
    return {}

class LayoutExample:
  MAXLINE = 40

  def __init__(self):
    self.console = Console()
    self.log_stream = StringIO()
    self.last_msg = None
    self.lines    = None

    self.make_layout()

  def make_layout(self):
    # Define the layout
    self.layout = Layout(name="root")

  def get_lines(self):
    log_str = self.log_stream.getvalue()
    lines   = log_str.splitlines()

    if len(lines) > self.MAXLINE:
      lines = lines[- self.MAXLINE:]

      # self.log_stream = StringIO()  
      self.log_stream.truncate(0)
      self.log_stream.seek(0)
      self.log_stream.write("\n".join(lines)+"\n")
    
    return lines

  # https://stackoverflow.com/questions/73512663/
  def capture(self, message):
    with self.console.capture() as capture:
      self.console.print(message)
    str_text = capture.get()
    str_text = Text.from_ansi(str_text)

    return str_text

  def split(self, line):
    pos1 = line.find(':', 0)
    pos2 = line.find(':', pos1+1)
    col1 = line[:pos1]
    col2 = line[pos1+1:pos2]
    col3 = self.capture(line[pos2+1:])

    return [col1, col3]

  def get_panel(self) -> Panel:
    table = Table.grid(padding=0, expand=True)
    table.add_column(no_wrap=True,
      min_width=8, overflow="fold", style="blue")
    table.add_column()
    
    for i, line in enumerate(self.lines[::-1]):
      table.add_row(*self.split(line))

    panel = Panel(table,
      title="[b]Web [yellow]Logs")
    return panel

  def get_layout(self) -> Layout:
    self.layout.update(
      self.get_panel())
    return self.layout

  async def task_web(self):
    logging.basicConfig(
      stream=self.log_stream,
      level=logging.DEBUG)
  
    app = web.Application()

    # setup jinja2 
    aiohttp_jinja2.setup(app,
      loader=jinja2.FileSystemLoader(
        '../templates'))

    app.router.add_get(
        '/', HomeHandler, name="index")
    app.router.add_static('/', '../site')

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

  async def do_log(self):
    with self.live:
      while True:
        self.lines = self.get_lines()

        last_msg = self.lines[-1:]
        if last_msg != self.last_msg:
          self.live.update(
            self.get_layout())
          self.last_msg = last_msg

        await asyncio.sleep(1)

  async def main(self):
    self.live = Live(None)

    task_log = asyncio.create_task(
      self.do_log())

    await(self.task_web())
    await(task_log)

# Program Entry Point
example = LayoutExample()
asyncio.run(example.main())

