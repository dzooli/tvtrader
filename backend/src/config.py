from sanic.config import Config
from os import getenv


class AppConfig(Config):
    # User configurable values
    DEV = getenv("TVTRADER_DEV", "True") == "True"
    VERBOSE = getenv("TVTRADER_VERBOSE", "True") == "True"
    GR_TIMEOUT = int(getenv("TVTRADER_ALERT_TIMEOUT", 15))
    GR_ENABLED = getenv("TVTRADER_GRAFANA_SEND", "True") == "True"
    TIMEZONE = getenv("TVTRADER_TIMEZONE", "Europe/Budapest")
    # Internal configuration
    APPNAME = "TradingView Trader"
    PORT = 8089
    API_TITLE = "TvTrader API"
    API_VERSION = '1.0.0'
    API_DESCRIPTION = "TradingView alert helper API"
    API_CONTACT_EMAIL = "zoltan.dzooli.fabian@gmail.com"
    OAS_IGNORE_OPTIONS = True
    CORS = True
    CORS_ORIGINS = "http://localhost:8080,https://www.tradingview.com"
    CORS_METHODS = "GET,POST,OPTIONS"
    CORS_AUTOMATIC_OPTIONS = True
    SWAGGER_UI_CONFIGURATION = {
        "apisSorter": "alpha",
        "jsonEditor": "false",
        "tryItOutEnabled": "false",
        "operationsSorter": "alpha",
    }
    WS_URL = "ws://localhost:" + str(PORT) + "/alerts"
    CARBON_HOST = "localhost"
    CARBON_PORT = 2003
    CARBON_SELL_VALUE: int = -35
    CARBON_BUY_VALUE: int = 35
