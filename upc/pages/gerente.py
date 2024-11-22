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
                    rx.table.column_header_cell("Trabajador"),
                    rx.table.column_header_cell("Estado"),
                    rx.table.column_header_cell("Fecha creación"),
                    rx.table.column_header_cell("Fecha Inicio"),
                    rx.table.column_header_cell("Fecha cierre"),                                   
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
        rx.table.cell(servicio.trabajador['nombre_trabajador'], style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(servicio.estado, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(servicio.fecha_creacion, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(servicio.fecha_inicio, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(servicio.fecha_cierre, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
    )

def bar_features(servicio: Servicio):
    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="cantidad",
            fill=rx.color("accent", 8),
            stroke=rx.color("accent", 9),
        ),
        rx.recharts.x_axis(data_key="estado"),
        rx.recharts.y_axis(),
        data=servicio,
        bar_category_gap="15%",
        bar_gap=6,
        bar_size=100,
        max_bar_size=40,
        width="100%",
        height=200,
    )



@rx.page(route="/gerente", on_load=State.get_estado_servicios())
@template
def gerente() -> rx.Component:   
    return rx.cond( ((State.user_email == 'mariostteven@gmail.com') | (State.user_email == 'santurron2004@gmail.com') | (State.user_email == 'dylan-lozano@upc.edu.co')) &  (State.authenticated), 
            rx.vstack(
            rx.heading("Gerencia de Servicios", font_size="24px"),
            rx.text("En este módulo puede revisar el estado de los servicios a nivel general, recuerde prestar especial atención a servicios abiertos e iniciados:", font_size="14px"),            
            rx.hstack(
                rx.text.strong("Total Servicios:"),
                rx.text(State.estado_count),
            ),    
            rx.text("Gráfico estados:", font_size="18px"),
            bar_features(State.data_for_chart),
            rx.text("Relación usuario/trabajador y estado:", font_size="18px"),
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
            ),
             # Si no está autorizado, mostrar un mensaje de acceso denegado
            rx.callout.root(
                rx.callout.icon(rx.icon(tag="info")),
                rx.callout.text(
                    "Acceso restringido, solo los gerentes tienen acceso a esta sección"
                ),
                color_scheme="red",
                role="alert",
            ),            
    )    