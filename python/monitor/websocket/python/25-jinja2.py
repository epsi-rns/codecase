# main.py

import logging
import pathlib
import sys

import jinja2
import aiohttp_jinja2
from aiohttp import web

@aiohttp_jinja2.template("index.jinja")
class HomeHandler(web.View):

  async def get(self):
    return {}

def main():
  logging.basicConfig(level=logging.DEBUG)

  app = web.Application()

  # setup jinja2 
  aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('../templates'))

  app.router.add_get('/', HomeHandler, name="index")
  app.router.add_static('/', '../site')

  web.run_app(app)

main()