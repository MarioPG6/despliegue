import reflex as rx

from ..template.template import template
from ..backend.state import State
from ..backend.models import Trabajador

   
class Detalles(rx.State):
    trabajadores: list['Trabajador']  = [] 


@rx.page(route="/detalles/[id]",title="Detalles de trabajadores",on_load=State.get_trabajador_by_id)
@template
def detalles() -> rx.Component:
    return rx.vstack(
        rx.heading("Detalles del trabajador"),
        rx.icon('user-round'),
        rx.cond(
            State.trabajadores,
            rx.card(
                rx.hstack(
                    rx.text('Nombre:'),
                    rx.text(State.trabajadores[0]['nombre_trabajador']),
                ),
                rx.hstack(
                    rx.text('Correo:'),
                    rx.text(State.trabajadores[0].login.correo),
                ),
                rx.hstack(
                    rx.text('Teléfono:'),
                    rx.text(State.trabajadores[0]['telefono_trabajador']),
                ),
                rx.hstack(
                    rx.text('Localidad:'),
                    rx.text(State.trabajadores[0]['localidad_trabajador']),
                ),
                rx.hstack(
                    rx.text('Especialidad:'),
                    rx.text(State.trabajadores[0]['categoria']),
                ),
                rx.hstack(
                    rx.text('Dirección:'),
                    rx.text(State.trabajadores[0]['direccion']),
                ),
                rx.hstack(
                    rx.text('Descripción:'),
                    rx.text(State.trabajadores[0]['descripcion']),
                ),
            ),
            rx.text("Cargando detalles del trabajador...")
        ),
        width="100%",
        height="100%",
        direction="column",
        align_items="stretch",
    )