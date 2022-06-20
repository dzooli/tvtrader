from sanic.config import Config
from os import getenv


class AppConfig(Config):
    APPNAME = "TradingView Trader"
    TIMEZONE = "Europe/Budapest"
    PORT = 8089
    DEV = getenv("SANIC_DEV", "True") == "True"
    API_TITLE = "TvTrader API"
    API_VERSION = '1.0.0'
    API_DESCRIPTION = "TradingView alert helper API"
    API_CONTACT_EMAIL = "zoltan.dzooli.fabian@gmail.com"
    OAS_IGNORE_OPTIONS = False
    CORS = True
    CORS_ORIGINS = "http://localhost:8080,https://www.tradingview.com"
    CORS_METHODS = "GET,POST,OPTIONS"
    CORS_AUTOMATIC_OPTIONS = True
    SWAGGER_UI_CONFIGURATION = {
        "apisSorter": "alpha",
        "jsonEditor": "true",
        "tryItOutEnabled": "true",
        "operationsSorter": "alpha",
        "docExpansion": "full",
    }
    WS_URL = "ws://localhost:" + str(PORT) + "/alerts"
