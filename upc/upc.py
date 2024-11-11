import reflex as rx
from .backend.state import State

from .frontend.navbar import navbar
from .frontend.sidebar import sidebar
from .frontend.footer import footer


@rx.page(title="A la vuelta de un Click!")
def index() -> rx.Component:

    return rx.vstack(
        navbar(),         
        rx.hstack(
            sidebar(),
            rx.box(                
                rx.cond(State.authenticated,
                    rx.hstack(
                        rx.text("Bienvenido"),
                        rx.text.strong(State.user_name),
                        rx.icon("smile"),
                    )
                ),        
                rx.hstack(
                    rx.image(src="logo.jpeg", width="300px", height="auto",ismap=True),
                    rx.card(rx.text("Esta en en lugar correcto para buscar y encontar profesionales en su localidad!. Solo debes seguir estos sencillos pasos:"),
                     rx.accordion.root(
                        rx.accordion.item(
                            header="Regístrate!",
                            content="Te puedes registrar como usuario si deseas buscar y contratar profesionales en tu localidad, o como trabajador si quieres ofrecer tus servicios profesionales",
                        ),
                        rx.accordion.item(
                            header="Busca por categoría o localidad",
                            content="Te ofrecemos varias opciones para que puedas buscar cualquier servicio directamente en tu localidad, o puedes también buscar por las diferentes categorías que tenemos",
                        ),
                        rx.accordion.item(
                            header="Ponte en contacto con los trabajadores",
                            content="Una vez registrado, tendrás acceso al catálogo completo de trabajadores y podrás ponerte en contacto con ellos a través de teléfono, correo o viendo la dirección a dirigirte al sitio para el caso de estbalecimientos",
                        ),
                        width="300px",
                        variant="soft",
                    )
                    
                    ),                                       
                    ),                    
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
