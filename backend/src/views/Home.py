from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.log import logger
from responses.JsonResponse import JsonSuccessResponse


class HomeView(HTTPMethodView):
    def __init__(self):
        return None

    async def get(self, request):
        app = Sanic.get_app()
        return JsonSuccessResponse.create("Health OK from " + app.config.APPNAME)

    async def post(self, request):
        logger.info("POST received: " + str(request.body))
        return JsonSuccessResponse.create("OK")
