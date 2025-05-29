from fasthtml.common import *
from monsterui.all import *
from fh_plotly import plotly_headers
import uvicorn

from pages.home import home_routes
from pages.crypto import crypto_routes
from pages.analysis import analysis_routes
from pages.ai import ai_route
from pages.backtesting import backtest_routes

theme = Theme.gray.headers(mode='light',font=ThemeFont.sm,
                             highlightjs=False, daisy=True)
app, rt = fast_app(
    db_file='data/cryptos.db',

    hdrs=(
        theme,
        plotly_headers,
        Script(src='https://cdn.plot.ly/plotly-2.32.0.min.js'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Meta(name='description', content=' My Website'),

    )
)

# Register route modules
home_routes(rt)
crypto_routes(rt)
analysis_routes(rt)
ai_route(rt)
backtest_routes(rt)

if __name__ == '__main__': serve(host='0.0.0.0', port=8000, reload=False)