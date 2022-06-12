from sanic import Sanic
from sanic.response import json
from sanic_ext import openapi
from sanic.log import logger

from config import AppConfig

app = Sanic("TvTrader", config=AppConfig(),
            configure_logging=True, )


@app.get("/")
@openapi.summary("Healthcheck endpoint")
def check(request):
    return json("HEALTHY " + app.config.APPNAME)


@app.post("/")
@openapi.summary("Alert POST endpoint. This is the endpoint for the Chrome extension.")
async def post(request):
    logger.info("POST received: " + str(request.body))
    return json("OK")


if __name__ == '__main__':
    app.run(host="127.0.0.1",
            port=app.config.PORT,
            dev=app.config.DEV,
            fast=not app.config.DEV,
            access_log=app.config.DEV)
