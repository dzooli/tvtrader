from os import getenv
from sanic.config import Config


class AppConfig(Config):
    # User configurable values
    DEV = getenv("TVTRADER_DEV", "True") == "True"
    VERBOSE = getenv("TVTRADER_VERBOSE", "True") == "True"
    GR_TIMEOUT = int(getenv("TVTRADER_ALERT_TIMEOUT", "15"))
    GR_ENABLED = getenv("TVTRADER_GRAFANA_SEND", "True") == "True"
    TIMEZONE = getenv("TVTRADER_TIMEZONE", "Europe/Budapest")
    # Internal configuration
    APPNAME = "TradingView Trader"
    PORT = 8089
    KEEP_ALIVE_TIMEOUT = 60
    ERROR_FORMAT = 'json'
    API_TITLE = "TvTrader API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "TradingView alert helper API"
    API_CONTACT_EMAIL = "zoltan.dzooli.fabian@gmail.com"
    API_SECURITY = [{"BasicAuth": [], "ApiKeyAuth": []}]
    API_SECURITY_DEFINITIONS = {
        "BasicAuth": {"type": "basic"},
        "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-API-KEY"},
    }
    OAS_IGNORE_OPTIONS = True
    CORS_ORIGINS = "http://localhost:8080"
    CORS_AUTOMATIC_OPTIONS = True
    CORS_METHODS = ["GET", "POST", "OPTIONS"]
    SWAGGER_UI_CONFIGURATION = {
        "apisSorter": "alpha",
        "jsonEditor": "false",
        "tryItOutEnabled": "false",
        "operationsSorter": "alpha",
        "docExpansion": "list",
        "displayRequestDuration": True,
    }
    WS_URL = "ws://localhost:" + str(PORT) + "/alerts"
    CARBON_HOST = "localhost"
    CARBON_PORT = 2003
    CARBON_SELL_VALUE: int = 15
    CARBON_BUY_VALUE: int = 85
