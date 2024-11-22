import reflex as rx
from ..template.template import template
from ..backend.state import State
from ..backend.models import  Servicio


def table_servicios(servicios: list[Servicio]) -> rx.Component:
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Código"),
                    rx.table.column_header_cell("Usuario"),
                    rx.table.column_header_cell("Estado"),
                    rx.table.column_header_cell("Fecha creación"),
                    rx.table.column_header_cell("Fecha Inicio"),
                    rx.table.column_header_cell("Fecha cierre"),
                    rx.table.column_header_cell("Iniciar"),                   
                )
            ),
            rx.table.body(
                rx.cond(
                    servicios,
                    rx.foreach(servicios, row_servicio),
                    rx.box("No se encontraron servicios")
                )
            ),
            style={"width": "100%"}
        ),
        style={"max-height": "160px", "overflow-y": "auto", "width": "100%"}
    )

def row_servicio(servicio: Servicio) -> rx.Component:    
    
    return rx.table.row(
        rx.table.cell(servicio.id, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(servicio.usuario['nombre_usuario'], style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(servicio.estado, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(servicio.fecha_creacion, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.cond((servicio.estado == "iniciado")  | (servicio.estado == "cerrado")  | (servicio.estado == "cancelado"),
            rx.table.cell(servicio.fecha_inicio, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
            rx.table.cell(rx.text("Sin iniciar"), style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        ),   
        rx.cond((servicio.estado == "abierto") | (servicio.estado == "iniciado"),
            rx.table.cell(rx.text("Sin cerrar"), style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),    
            rx.table.cell(servicio.fecha_cierre, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        ), 
        rx.cond((servicio.estado == "abierto"),
            rx.table.cell(
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.icon_button('file-check'),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Iniciar servicio"),
                        rx.alert_dialog.description(
                            "¿Está seguro de que desea iniciar este servicio?",
                        ),
                        rx.flex(
                            rx.alert_dialog.cancel(
                                rx.button("Cacelar"),
                            ),
                            rx.alert_dialog.action(
                                rx.button("Iniciar"),
                                on_click=lambda: State.iniciar_servicio(servicio.id),
                            ),
                            spacing="3",
                        ),
                    ),
                ),
            ), 
            rx.table.cell(rx.icon_button('file-check',disabled=True)),
        ),                 
    )


@rx.page(route="/servicios-trabajador", on_load=State.get_servicios_by_trabajador())
@template
def servicios_trabajador() -> rx.Component:   
    return rx.vstack(
            rx.heading("Servicios", font_size="24px"),            
            rx.text("Tus servicios:", font_size="18px"),
            rx.cond(
                State.servicios,
                table_servicios(State.servicios),
                 rx.callout.root(
                    rx.callout.icon(rx.icon(tag="info")),
                    rx.callout.text(
                        "No se encontraron servicios"
                    ),
                    color_scheme="green",
                    role="info",
                ),         
            ),                        
            spacing="30px",
            align="start",
        )