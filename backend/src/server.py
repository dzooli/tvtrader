from sanic import Sanic

from config import AppConfig
from views.Home import HomeView

app = Sanic("TvTrader", config=AppConfig())
app.add_route(HomeView.as_view(), "/")

if __name__ == '__main__':
    app.run(host="127.0.0.1",
            port=app.config.PORT,
            dev=app.config.DEV,
            fast=not app.config.DEV,
            access_log=app.config.DEV)
