import reflex as rx
from ..frontend.navbar import navbar
from ..frontend.sidebar import sidebar
from ..frontend.footer import footer



def page1() -> rx.Component:

    return rx.vstack(        
        navbar(),         
        rx.hstack(
            sidebar(),
            rx.box(
                rx.text("Welcome to page1."),
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