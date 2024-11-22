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
                    rx.image(src="banner.jpg", width="500px", height="auto"),    
                    rx.vstack(
                        rx.text("A la vuelta de un Click! aquí encontrará los mejores pintores, cerrajeros y maestros para sus obras!"),
                        rx.text("Estás en en lugar correcto para buscar y encontar trabajadores en tu localidad!."),
                        rx.text(""),
                    ),
                ),                        
                rx.hstack(                    
                    rx.vstack(
                        rx.text(""),
                        rx.image(src="obras.jpg", width="250px", height="auto"),                    
                        rx.image(src="pintor.jpg",width="250px", height="auto"),
                    ),                                        
                    rx.vstack(
                        rx.text(""),
                        rx.card(
                        rx.hstack(                            
                            rx.text.strong("1. Regístrate"),
                            rx.icon("user-plus"),
                        ),    
                        rx.text("Te puedes registrar como usuario si deseas buscar y contratar trabajadores en tu localidad, o como trabajador si quieres ofrecer tus servicios profesionales"),
                        ),
                        rx.card(
                        rx.hstack(
                            rx.text.strong("2. Busca por categoría o localidad"),
                            rx.icon("map-pin"),
                        ),    
                        rx.text("Te ofrecemos varias opciones para que puedas buscar cualquier servicio directamente en tu localidad, o puedes también buscar por las diferentes categorías que tenemos"),
                        ),
                        rx.card(
                        rx.hstack(                            
                            rx.text.strong("3. Ponte en contacto con un trabajador!"),
                            rx.icon("phone"),
                        ),    
                        rx.text("Una vez registrado, tendrás acceso al catálogo completo de trabajadores y podrás ponerte en contacto con ellos solamente haciendo 'Click' en un botón"),
                        ),
                        rx.card(
                            rx.text.strong("Política de calidad"),
                            rx.icon("award",size=32,color="yellow"),
                            rx.text("Nuestros trabajadores son directamente seleccionados por nosotros para garantizar un estándar de calidad, se hace un delicado y cuidadoso proceso de aprobación, el cual inicluye verificación de datos de contacto, experiencia y conocimiento del servicio a prestar."),
                        ),
                        rx.card(
                            rx.text.strong("Pagos"),
                            rx.icon("circle-dollar-sign",size=32,color="yellow"),
                            rx.text("Como trabajador solo debes pagar una sucripción mensual de 10.000 COP, y nuestros usuarios podrán contactarte a la vuelta de un Click!"),
                            rx.text("A continuación puedes ver nuestros métodos de pago:"),
                            rx.image(src="daviplata-nequi.jpg",width="160px", height="auto"),
                            

                        ),                          
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
