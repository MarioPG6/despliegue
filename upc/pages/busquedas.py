import reflex as rx
from ..backend.state import State
from ..backend.models import Trabajador
from ..template.template import template

class Busqueda(rx.State):
    trabajadores: list[Trabajador] = []
    filtro_nombre: str = ""
    filtro_localidad: str = ""
    filtro_categoria: str = ""
    datos_cargados: bool = False

    def on_load(self):
        self.trabajadores = self.get_trabajadores()
        self.datos_cargados = True

    def get_trabajadores(self):
        with rx.session() as session:
            query = Trabajador.select()
            if self.filtro_nombre:
                query = query.where(Trabajador.nombre_trabajador.contains(self.filtro_nombre))
            if self.filtro_localidad:
                query = query.where(Trabajador.localidad_trabajador.contains(self.filtro_localidad))
            if self.filtro_categoria:
                query = query.where(Trabajador.categoria.contains(self.filtro_categoria))
            return session.exec(query).all() or []

    def actualizar_filtro(self, nombre: str, localidad: str, categoria: str):
        self.filtro_nombre = nombre
        self.filtro_localidad = localidad
        self.filtro_categoria = categoria
        self.trabajadores = self.get_trabajadores()

    def reset_filtros(self):
        self.filtro_nombre = ""
        self.filtro_localidad = ""
        self.filtro_categoria = ""
        self.trabajadores = self.get_trabajadores()  # Vuelve a cargar todos los trabajadores

def table_trabajadores_busqueda(trabajadores: list[Trabajador]) -> rx.Component:
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Nombre"),
                    rx.table.column_header_cell("Localidad"),
                    rx.table.column_header_cell("Categoría"),
                    rx.table.column_header_cell("Detalles"),
                )
            ),
            rx.table.body(
                rx.cond(
                    trabajadores,
                    rx.foreach(trabajadores, row_busqueda),
                    rx.box("No se encontraron trabajadores")
                )
            ),
            style={"width": "100%", "table-layout": "fixed"}
        ),
        style={"max-height": "300px", "overflow-y": "auto", "width": "100%"}
    )

def row_busqueda(trabajador: Trabajador) -> rx.Component:
    return rx.table.row(
        rx.table.cell(trabajador.nombre_trabajador, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.localidad_trabajador, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.categoria, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(
            rx.button("Detalles", on_click=lambda: rx.redirect(f"/detalles/{trabajador.id}"))
        )
    )

@rx.page(route="/busquedas", on_load=Busqueda.on_load)
@template
def busqueda() -> rx.Component:
    return rx.vstack(
        rx.heading("Búsqueda de Trabajadores", font_size="24px"),
        rx.hstack(
            rx.input(
                placeholder="Buscar por nombre",
                on_change=lambda nombre: Busqueda.actualizar_filtro(nombre, Busqueda.filtro_localidad, Busqueda.filtro_categoria),  
                width="200px"
            ),
            rx.select(
                ["Antonio Nariño", "Barrios Unidos", "Bosa", "Chapinero", "Ciudad Bolívar", "Engativá", "Fontibon", "Kennedy", "La Candelaria", "Los Mártires", 
                 "Puente Aranda", "Rafael Uribe Uribe", "San Cristóbal", "Santa Fe", "Suba", "Sumapaz", "Teusaquillo", "Tunjuelito", "Usaquén", "Usme"],
                placeholder="Seleccionar localidad",
                on_change=lambda localidad: Busqueda.actualizar_filtro(Busqueda.filtro_nombre, localidad, Busqueda.filtro_categoria),
                width="200px"
            ),
            rx.select(
                ["Cerrajería", "Pintura", "Obras"],
                placeholder="Seleccionar categoría",
                on_change=lambda categoria: Busqueda.actualizar_filtro(Busqueda.filtro_nombre, Busqueda.filtro_localidad, categoria),
                width="200px"
            ),
            rx.button("Buscar", on_click=lambda: Busqueda.actualizar_filtro(Busqueda.filtro_nombre, Busqueda.filtro_localidad, Busqueda.filtro_categoria)),
            rx.button("Borrar filtros", on_click=lambda: Busqueda.reset_filtros()),  # Botón para borrar los filtros
            spacing="10px",
        ),
        rx.cond(
            Busqueda.datos_cargados,
            table_trabajadores_busqueda(Busqueda.trabajadores),
            rx.spinner()
        ),
        spacing="30px",
        align="start",
    )