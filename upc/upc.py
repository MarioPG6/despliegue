import reflex as rx

from rxconfig import config
from .backend.backend import State
from .frontend.navbar import navbar
from .frontend.sidebar import sidebar
from .frontend.footer import footer
from .pages import *


def index() -> rx.Component:
    return rx.vstack(        
        navbar(),         
        rx.hstack(
            sidebar(),
            rx.box(
                rx.text("Aquí va el contenido."),
                bg=rx.color("accent", 1),
                width="100%",
                height="100%",
                padding="2em",
            ),
            width="100%",
            height="100%",
            align_items="stretch",
        ),
        rx.box( 
            footer(),
            width="100%",
            bg=rx.color("black", 1), 
        ),             
        height="100vh",        
        spacing="0",
        bg=rx.color("accent", 1),
        width="100%",     
    )
    
   

app = rx.App()
app.add_page(index)
app.add_page(page1, route='/page1')
app.add_page(contact, route='/contact')