from fasthtml.common import *
from monsterui.all import *

from components.layout import page_layout, crypto_card
from lib.dataframe import get_market_overview

def home_routes(rt):

    @rt('/')
    def get():
        overview = get_market_overview()

        cards =[
            crypto_card(crypto['symbol'], crypto['last_price'],
                       crypto['change'], crypto['pct_change'],
                       crypto['ask'], crypto['bid'])
            for crypto in overview
            ]

        content = [
            H1("Crypto Market Dashboard"),

            P("Welcome to your crypto analysis platform",
              cls=TextPresets.bold_lg),

            Br(),

            Div(*cards),
            Br(),
            A(Button("View All Crypto's", cls=ButtonT.primary),
              href="/crypto", cls=AT.primary)
        ]

        return page_layout(
            "Crypto Market Dashboard",
            *content
        )