from ssl import ALERT_DESCRIPTION_DECODE_ERROR
from sanic.config import Config

class AppConfig(Config):
    APPNAME="TradingView Trader"
    PORT=8089
    DEV=True
    API_TITLE="TvTrader API",
    OAS_IGNORE_OPTIONS=False,
    CORS=True
    SWAGGER_UI_CONFIGURATION = {
            "apisSorter": "alpha",
            # "jsonEditor": "true",
            # "tryItOutEnabled": "true",
            "operationsSorter": "alpha",
            "docExpansion": "full",
        },

    
