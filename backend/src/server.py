from sanic import Sanic
from sanic.response import text

from config import AppConfig

app = Sanic("TvTrader", config=AppConfig())

@app.get("/")
async def homepage(request):
    app = Sanic.get_app()
    return text("Hello, I am " + app.config.APPNAME)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=app.config.PORT, dev=app.config.DEV, fast=not app.config.DEV)

