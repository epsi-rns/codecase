import logging, asyncio
import jinja2, aiohttp_jinja2

from aiohttp import web
from io import StringIO

@aiohttp_jinja2.template("index.jinja")
class HomeHandler(web.View):

  async def get(self):
    return {}

class LayoutExample:
  def __init__(self):
    self.log_stream = StringIO()

  async def task_web(self):
    logging.basicConfig(
      stream=self.log_stream,
      level=logging.DEBUG)
  
    app = web.Application()

    # setup jinja2 
    aiohttp_jinja2.setup(app,
      loader=jinja2.FileSystemLoader('../templates'))

    app.router.add_get('/', HomeHandler, name="index")
    app.router.add_static('/', '../site')

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

  async def do_log(self):
    while True:
      print(self.log_stream.getvalue())
      await asyncio.sleep(1)

  async def main(self):
    task_log = asyncio.create_task(
      self.do_log())

    await(self.task_web())
    await(task_log)

# Program Entry Point
example = LayoutExample()
asyncio.run(example.main())

