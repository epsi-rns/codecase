import logging, sys
import jinja2, aiohttp_jinja2

from aiohttp import web
from rich.logging import RichHandler

@aiohttp_jinja2.template("index.jinja")
class HomeHandler(web.View):

  async def get(self):
    return {}

def main():
  FORMAT = "%(message)s"
  logging.basicConfig(
    level=logging.DEBUG, format=FORMAT,
    datefmt="[%X]", handlers=[RichHandler()])

  app = web.Application()

  # setup jinja2 
  aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('../templates'))

  app.router.add_get('/', HomeHandler, name="index")
  app.router.add_static('/', '../site')

  web.run_app(app)

main()