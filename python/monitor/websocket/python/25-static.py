import logging
from aiohttp import web

async def root_handler(request):
    return web.HTTPFound('/23-show.html')

def main():
  logging.basicConfig(level=logging.DEBUG)

  app = web.Application()

  app.router.add_route('*', '/', root_handler)
  app.router.add_static('/', '../site')

  web.run_app(app)

main()
