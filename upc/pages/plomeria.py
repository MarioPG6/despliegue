import reflex as rx

from ..template.template import template
from ..backend.state import State
from ..backend.models import Trabajador

class Plomeria(rx.State):
    users: list['Trabajador'] = []

def table(list_users: list[Trabajador] = []) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Correo"),
                rx.table.column_header_cell("Teléfono"),
                rx.table.column_header_cell("Localidad"),
                rx.table.column_header_cell("Dirección")
            )
        ),
        rx.table.body(
            rx.foreach(list_users, row_table)
        )
    )

def row_table(user: Trabajador) -> rx.Component:
    return rx.table.row(
        rx.table.cell(user.nombre_trabajador),
        rx.table.cell(user.correo_trabajador),
        rx.table.cell(user.telefono_trabajador),
        rx.table.cell(user.localidad_trabajador),
        rx.table.cell(user.direccion),
        rx.table.cell(rx.hstack(rx.button(rx.icon("pencil")), on_click=rx.redirect(f"/detalles/{user.id}"))),
    )

@rx.page(route="/plomeria", title="Plomería", on_load=State.get_users_plomeria)
@template
def plomeria() -> rx.Component:
    return rx.hstack(
        rx.heading("Plomería"),
        table(State.users),
        direction="column",
    )
