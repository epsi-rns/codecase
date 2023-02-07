from aiohttp import web
import jinja2, aiohttp_jinja2

@aiohttp_jinja2.template("index.jinja")
class HomeHandler(web.View):

  async def get(self):
    return {}

class AIOWeb:
  async def task_web(self):
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