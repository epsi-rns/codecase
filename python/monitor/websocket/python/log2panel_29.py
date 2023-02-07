import logging, asyncio
from io import StringIO

from rich.console import Console
from rich.text    import Text
from rich.table   import Table
from rich.panel   import Panel
from rich.layout  import Layout
from rich.live    import Live

class Log2Panel:
  MAXLINE = 40

  def __init__(self,
      ref_live, ref_layout, layout_name):
    # rich: required in descendent class
    self.live   = ref_live
    self.layout = ref_layout
    self.layout_name = layout_name

    # log related
    self.console = Console()
    self.log_stream = StringIO()
    self.last_msg = None
    self.lines    = None

    logging.basicConfig(
      stream=self.log_stream,
      level=logging.INFO)

  def __get_lines(self):
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
  def __capture(self, message):
    with self.console.capture() as capture:
      self.console.print(message)
    str_text = capture.get()
    str_text = Text.from_ansi(str_text)

    return str_text

  def __split(self, line):
    pos1 = line.find(':', 0)
    pos2 = line.find(':', pos1+1)
    col1 = line[:pos1]
    col2 = line[pos1+1:pos2]
    col3 = self.__capture(line[pos2+1:])

    return [col1, col3]

  def __get_panel(self) -> Panel:
    table = Table.grid(padding=0, expand=True)
    table.add_column(no_wrap=True,
      min_width=8, overflow="fold", style="blue")
    table.add_column()
    
    for i, line in enumerate(self.lines[::-1]):
      table.add_row(*self.__split(line))

    panel = Panel(table,
      title="[b]Web [yellow]Logs")
    return panel

  def __get_layout(self) -> Layout:
    self.layout[self.layout_name].update(
      self.__get_panel())
    return self.layout

  async def do_log(self):
    with self.live:
      while True:
        self.lines = self.__get_lines()

        last_msg = self.lines[-1:]
        if last_msg != self.last_msg:
          self.live.update(
            self.__get_layout())
          self.last_msg = last_msg

        await asyncio.sleep(1)


