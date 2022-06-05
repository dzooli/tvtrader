from importlib.metadata import requires
from sanic import Sanic
from sanic.log import logger
from sanic_ext import openapi

from config import AppConfig
from responses.JsonResponse import JsonSuccessResponse


app = Sanic("TvTrader", config=AppConfig())


@app.get("/")
async def homepage(request):
    app = Sanic.get_app()
    return JsonSuccessResponse.create("Health OK from " + app.config.APPNAME)


@app.post("/", strict_slashes=False)
async def post_alert(request):
    logger.info("POST received: " + str(request.body))
    return JsonSuccessResponse.create("OK")

if __name__ == '__main__':
    app.run(host="127.0.0.1",
            port=app.config.PORT,
            dev=app.config.DEV,
            fast=not app.config.DEV,
            access_log=app.config.DEV)
