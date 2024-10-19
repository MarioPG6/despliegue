import reflex as rx
from ..frontend.navbar import navbar
from ..frontend.sidebar import sidebar
from ..frontend.footer import footer
from ..backend.backend import FormState


def contact() -> rx.Component:

    return rx.vstack(        
        navbar(),         
        rx.hstack(
            sidebar(),
            rx.box(
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="First Name",
                            name="first_name",
                            required=True,
                            width="50%",    
                        ),
                        rx.input(
                            placeholder="Last Name",
                            name="last_name",
                            width="50%",
                        ),                        
                        rx.button("Submit", type="submit"),
                        rx.cond(FormState.did_submit, rx.text("Enviado")),
                    ),
                    on_submit=FormState.handle_submit,
                    reset_on_submit=True,                    
                ),
                bg=rx.color("accent", 1),
                width="100vw",
                padding="2em",
                align_items="center",
            ),           
            align="stretch",
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





