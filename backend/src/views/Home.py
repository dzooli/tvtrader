from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.log import logger
from sanic_ext import openapi

from responses.JsonResponse import JsonSuccessResponse


class HomeView(HTTPMethodView):
    def __init__(self):
        return None

    @openapi.summary("Healthcheck endpoint")
    async def get(self, request):
        app = Sanic.get_app()
        return JsonSuccessResponse.create("Health OK from " + app.config.APPNAME)

    @openapi.summary("Alert POST endpoint. This is the endpoint for the Chrome extension.")
    async def post(self, request):
        logger.info("POST received: " + str(request.body))
        return JsonSuccessResponse.create("OK")
