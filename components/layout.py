from fasthtml.common import *
from monsterui.all import *
from datetime import datetime



def crypto_card(symbol, last_price, change, change_pct, ask, bid):
    """Reusable stock card components"""
    color = "green" if change >= 0 else "red"
    return CardContainer(
        DivFullySpaced(
        CardTitle(H3(symbol, cls=TextPresets.bold_lg)),
        P(f"Last Price: ${last_price:.2f}", cls=TextPresets.bold_sm),
        P(f"ASK: ${ask:.2f}", cls=TextPresets.bold_sm),
        P(f"BID: ${bid:.2f}", cls=TextPresets.bold_sm),
        
        P(f"{change:+.2f} ({change_pct:+.1f}%)", style=f"color: {color}"),
        cls=CardT.hover
    ))


def page_layout(title, *content):
    """Main page layout with navigation"""
    nav = Header(
        Div(
            A("Crypto Dashboard", href="/", cls=AT.classic),
            Div(
            Button('Pages 👇🏽', cls=ButtonT.primary),
            DropDownNavContainer(
                Li(A("Home", href="/", cls=AT.primary)),
                Li(A("Crypto", href="/crypto", cls=AT.primary)),
                Li(A("Analysis", href="/analysis", cls=AT.primary)),
                Li(A("AI", href="/ai", cls=AT.primary)),
                Li(A("BackTest", href="/backtest", cls=AT.primary)),
                
                

                ),

        ),
        cls = 'container mx-auto flex items-center justify-between px-4 py-3'
        ),
    cls='bg-green-100 shadow-md'
    )

    footer = Footer(
        Div(
            Div(
                P(f"© {datetime.now().year} Crypto Tracker. All rights reserved.",
                  cls='text-gray-700'),

                cls = 'mb-4'
            ),

            Div(
                A('Privacy Policy', href='#', cls=AT.classic),
                A('Terms of Service', href='#', cls=AT.classic),

                cls = 'text-sm'
            ),

            cls = 'container mx-auto px-4 py-6 text-center'
        ),

        cls = 'bg-green-100 mt-9'
    )

    body = Body(
            nav,
            Main(
                Div(*content, cls="container mx-auto px-4 py-8"),
                cls='min-h-screen'
            ))

    return Title(title), body, footer
