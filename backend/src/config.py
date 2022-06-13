from ssl import ALERT_DESCRIPTION_DECODE_ERROR, ALERT_DESCRIPTION_DECOMPRESSION_FAILURE
from sanic.config import Config


class AppConfig(Config):
    APPNAME = "TradingView Trader"
    PORT = 8089
    DEV = True
    API_TITLE = "TvTrader API"
    API_VERSION = '1.0.0'
    API_DESCRIPTION = "TradingView alert helper API"
    API_CONTACT_EMAIL = "zoltan.dzooli.fabian@gmail.com"
    OAS_IGNORE_OPTIONS = False
    CORS = True
    CORS_ORIGINS = "http://localhost:8080"
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
