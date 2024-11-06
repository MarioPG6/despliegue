import reflex as rx
from ..template.template import template
from ..backend.state import State
from ..backend.models import Trabajador

class Reparaciones(rx.State):
    trabajadores: list['Trabajador'] = []

def user_card(user: Trabajador) -> rx.Component:
    """Define una tarjeta cuadrada para cada usuario de la categoría Reparaciones."""
    return rx.card(
        rx.vstack(
            rx.icon("wrench", size=40, color="gray"), 
            rx.text(user.nombre_trabajador, font_size="20px", font_weight="bold"),
            rx.text(user.descripcion, font_size="16px", color="gray"),
            rx.button("Ver detalles", on_click=rx.redirect(f"/detalles/{user.id}")),
            spacing="10px",
            align="center",
        ),
        padding="20px",
        border="1px solid #ddd",
        border_radius="10px",
        width="200px",
        height="250px",
        shadow="lg",
    )


@rx.page(route="/obras", on_load=State.get_trabajadores_by_categoria("Obras"))
@template
def obras() -> rx.Component:
    """Página principal de obras con tarjetas para cada usuario."""
    return rx.vstack(
        rx.heading("obras", icon="wrench"),  
        rx.hstack(
            rx.foreach(State.trabajadores, user_card), 
            spacing="20px",
            wrap="wrap", 
        ),
        align="start",
        spacing="30px",
    )