import reflex as rx

from ..template.template import template
from ..backend.state import State


@rx.page(route="/contacto",title="Contáctanos")
@template
def contacto() -> rx.Component:

    return rx.form(
        rx.vstack(
        rx.text("Sus inquietudes son importates para nosotros, por favor dejénos su comentario."),    
        rx.input(
            placeholder="Digite su nombre",
            name="nombre",
            required=True,
            width="50%",    
        ),
        rx.input(
            placeholder="Digite su correo",
            name="correo",
            width="50%",
        ),
        rx.text_area(
            placeholder="Deje su comentario aquí...",
            name="comentario",
            width="50%",            
        ),                            
            rx.button("Enviar", type="submit"),
            rx.cond(State.did_submit, rx.text("Gracias por sus comentarios!")),
            ),
        on_submit=State.handle_contacto,
        reset_on_submit=True,                    
        ),    