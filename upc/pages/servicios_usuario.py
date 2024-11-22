import reflex as rx
from ..template.template import template
from ..backend.state import State
from ..backend.models import Servicio



def table_servicios(servicios: list[Servicio]) -> rx.Component:
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Código"),
                    rx.table.column_header_cell("Trabajador"),
                    rx.table.column_header_cell("Estado"),
                    rx.table.column_header_cell("Fecha creación"),
                    rx.table.column_header_cell("Fecha Inicio"),
                    rx.table.column_header_cell("Fecha cierre"),
                    rx.table.column_header_cell("Cerrar"),
                    rx.table.column_header_cell("Cancelar"),
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
        rx.table.cell(servicio.trabajador['nombre_trabajador'], style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(servicio.estado, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(servicio.fecha_creacion, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.cond((servicio.estado == "iniciado")  | (servicio.estado == "cerrado") | (servicio.estado == "cancelado"),
            rx.table.cell(servicio.fecha_inicio, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
            rx.table.cell(rx.text("Sin iniciar"), style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        ),     
        rx.cond((servicio.estado == "abierto") | (servicio.estado == "iniciado"),
            rx.table.cell(rx.text("Sin cerrar"), style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),    
            rx.table.cell(servicio.fecha_cierre, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        ),    
        rx.cond((servicio.estado == "abierto")  | (servicio.estado == "iniciado"),
            rx.table.cell(
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                            rx.icon_button('file-check'),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Cerrar servicio"),
                        rx.alert_dialog.description(
                            "¿Está seguro de que desea cerrar este servicio?",
                        ),
                        rx.flex(
                            rx.alert_dialog.cancel(
                                rx.button("Cancelar"),
                            ),
                            rx.alert_dialog.action(
                                rx.button("Cerrar"),
                                on_click=lambda: State.cerrar_servicio(servicio.id),
                            ),
                            spacing="3",
                        ),
                    ),
                )
            ),
            rx.table.cell(rx.icon_button('file-check',disabled=True)),
        ),    
        rx.cond((servicio.estado == "abierto")  | (servicio.estado == "iniciado"),
            rx.table.cell(
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(                  
                            rx.icon_button('file-x'),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Cancelar servicio"),
                        rx.alert_dialog.description(
                            "¿Está seguro de que desea cancelar este servicio?",
                        ),
                        rx.flex(
                            rx.alert_dialog.cancel(
                                rx.button("No"),
                            ),
                            rx.alert_dialog.action(
                                rx.button("Si"),
                                on_click=lambda: State.cancelar_servicio(servicio.id),
                            ),
                            spacing="3",
                        ),
                    ),
                )
            ), 
            rx.table.cell(rx.icon_button('file-x',disabled=True)), 
        ),       
    )


@rx.page(route="/servicios-usuario", on_load=State.get_servicios_by_user())
@template
def servicios_usuario() -> rx.Component:   
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