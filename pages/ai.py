from fasthtml.common import *
from monsterui.all import *
from mistletoe import markdown, HTMLRenderer

from components.layout import page_layout
from lib.graph import graph

import logging
from typing import Literal


logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)

# Components
def chat_message(msg: str, user: Literal['user', 'trader']) -> Div:
    """Renders a chat message button with the given message and user."""

    chat_class = 'chat-end '

    match user:
        case 'user':
            bubble_class = 'chat-bubble-primary'
            chat_header = 'You'

        case _:
            bubble_class = 'chat-bubble-secondary w-full'
            chat_header = 'trader'
            chat_class = 'chat-start'

    return Div(cls=f'chat {chat_class}')(
        Div(chat_header, cls='chat-header'),
        Div(msg, cls=f'chat-bubble {bubble_class}'),
    )

def chat_input() -> LabelInput:
    """Renders the chat input field."""
    return LabelInput('Add $ymbol 🪙',
        name='msg',
        id='msg-input',
        # cls='input input-bordered w-full ',
        hx_swap_oob='true',
    )

def ai_route(rt):
    
    @rt('/ai')
    def get():
        chat_history = Div(id='chatlist', cls='h-screen overflow-y-auto pb-24 px-4')
    
        input_area = Form(
            Div(cls='flex space-x-2')(
                Group(chat_input(), 
                      Br(),
                      Button('Send', cls=ButtonT.primary, hx_indicator='#loading'))
            ),
            Loading(LoadingT.bars, htmx_indicator=True, id="loading"),
            hx_post='/ai/result',
            hx_target='#chatlist',
            hx_swap='beforeend',
            # cls='absolute bottom-0 left-0 right-0 p-4',
        )
        page = Div(cls='h-full relative')(chat_history, input_area)

        return page_layout('💸 Trader Agent 🤖', *page)
    
    
    @rt('/ai/result')
    def post(msg: str):
        initial_state = {"question": msg, "facts": [], "conclusion": ""}
        result = graph.invoke(initial_state)
        
        for fact in result['facts']:
            show_fact = chat_message(Safe(apply_classes(markdown(fact, renderer=HTMLRenderer))), 'facts')
        show_con = chat_message(Safe(apply_classes(markdown(result['conclusion'], renderer=HTMLRenderer))), 'trader')
            

        logging.info(fact)

        return (
            chat_message(msg, 'user'),
            show_fact,
            show_con,
            chat_input(),
        )