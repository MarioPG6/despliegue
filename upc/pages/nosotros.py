import reflex as rx
from ..template.template import template


@rx.page(route="/nosotros", title="Conoce_el_equipo")
@template
def nosotros() -> rx.Component:
    return rx.box(
                rx.vstack(
                    rx.text("A la vuelta de un Click! aquí encontrará los mejores pintores, cerrajeros y maestros para sus obras!"),
                    rx.text("Conoce nuestros Roles y de donde venimos:"),
                    rx.text(""),
                ),                    
                 rx.vstack(                  
                    rx.vstack(
                        rx.card(
                        rx.hstack(
                            rx.text.strong("Santiago Herrada"),
                            rx.icon("user"),
                        ),    
                        rx.text("Universidad Piloto de Colombia"),
                        rx.text("Lider y Backend"),
                        ),
                        rx.card(
                        rx.hstack(
                            rx.text.strong("Laura Cardenas"),
                            rx.icon("user"),
                        ),    
                        rx.text("Universidad Piloto de Colombia"),
                        rx.text("Pruebas y Frontend"),
                        ),
                        rx.card(
                        rx.hstack(                            
                            rx.text.strong("Mario Palencia"),
                            rx.icon("user"),
                        ),    
                        rx.text("Universidad Piloto de Colombia"),
                        rx.text("Backend y base de datos"),
                        ),
                        rx.card(
                        rx.hstack(      
                            rx.text.strong("Juan David Cortes"),
                            rx.icon("user"),
                        ),    
                            rx.text("Universidad Piloto de Colombia"),
                            rx.text("Frontend"),
                        ),
                        rx.card(
                        rx.hstack(    
                            rx.text.strong("Dylan Lozano"),
                            rx.icon("user"),
                        ),    
                            rx.text("Universidad Piloto de Colombia"),
                            rx.text("Frontend"),

                        ),                          
                    ),        
                ),  
    ),