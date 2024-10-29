import reflex as rx
from ..backend.state import State
from ..backend.models import Trabajador, Contacto
from ..template.template import template
from ..backend import auth



class Admin(rx.State):
    trabajadores: list[Trabajador] = []
    contactos: list[Contacto] = []
    filtro_email: str = ""  # Filtro para el correo electrónico
    datos_cargados: bool = False  # Indicador para verificar si los datos están cargados

    # Método para cargar los datos con filtro
    def on_load(self):
        self.trabajadores = self.get_trabajadores()
        self.contactos = self.get_contactos()
        self.datos_cargados = True

    # Método para recuperar trabajadores de la base de datos con filtro
    def get_trabajadores(self):
        with rx.session() as session:
            query = Trabajador.select()
            if self.filtro_email:
                query = query.where(Trabajador.correo_trabajador.contains(self.filtro_email))
            return session.exec(query).all() or []

    # Método para recuperar contactos de la base de datos con filtro
    def get_contactos(self):
        with rx.session() as session:
            query = Contacto.select()
            if self.filtro_email:
                query = query.where(Contacto.correo.contains(self.filtro_email))
            return session.exec(query).all() or []

    # Método para actualizar la búsqueda y recargar datos
    def actualizar_filtro(self, email: str):
        self.filtro_email = email
        self.trabajadores = self.get_trabajadores()
        self.contactos = self.get_contactos()

    # Método para eliminar un trabajador
    def delete_trabajador(self, trabajador_id: int):
        with rx.session() as session:
            trabajador = session.exec(Trabajador.select().where(Trabajador.id == trabajador_id)).first()
            if trabajador:
                session.delete(trabajador)
                session.commit()
        self.trabajadores = self.get_trabajadores()

    # Método para eliminar un contacto
    def delete_contacto(self, contacto_id: int):
        with rx.session() as session:
            contacto = session.exec(Contacto.select().where(Contacto.id == contacto_id)).first()
            if contacto:
                session.delete(contacto)
                session.commit()
        self.contactos = self.get_contactos()

def table_trabajadores(trabajadores: list[Trabajador]) -> rx.Component:
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Nombre"),
                    rx.table.column_header_cell("Correo"),
                    rx.table.column_header_cell("Teléfono"),
                    rx.table.column_header_cell("Localidad"),
                    rx.table.column_header_cell("Categoría"),
                    rx.table.column_header_cell("Dirección"),
                    rx.table.column_header_cell("Acciones"),
                )
            ),
            rx.table.body(
                rx.cond(
                    trabajadores,
                    rx.foreach(trabajadores, row_trabajador),
                    rx.box("No se encontraron trabajadores")
                )
            ),
            style={"width": "100%", "table-layout": "fixed"}
        ),
        style={"max-height": "160px", "overflow-y": "auto", "width": "100%"}
    )

def row_trabajador(trabajador: Trabajador) -> rx.Component:
    return rx.table.row(
        rx.table.cell(trabajador.nombre_trabajador, style={"max-width": "100px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.correo_trabajador, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.telefono_trabajador, style={"max-width": "100px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.localidad_trabajador, style={"max-width": "100px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.categoria, style={"max-width": "100px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.direccion, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(
            rx.button(
                rx.icon('trash-2'),
                on_click=lambda t_id=trabajador.id: Admin.delete_trabajador(t_id),
                color="white",
                size="sm"
            )
        )
    )

def table_contactos(contactos: list[Contacto]) -> rx.Component:
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Nombre"),
                    rx.table.column_header_cell("Correo"),
                    rx.table.column_header_cell("Comentario"),
                    rx.table.column_header_cell("Acciones"),
                )
            ),
            rx.table.body(
                rx.cond(
                    contactos,
                    rx.foreach(contactos, row_contacto),
                    rx.box("No se encontraron contactos")
                )
            ),
            style={"width": "100%", "table-layout": "fixed"}
        ),
        style={"max-height": "160px", "overflow-y": "auto", "width": "100%"}
    )

def row_contacto(contacto: Contacto) -> rx.Component:
    return rx.table.row(
        rx.table.cell(contacto.nombre, style={"max-width": "100px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(contacto.correo, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(
            rx.box(
                contacto.comentario,
                style={"max-height": "80px", "overflow-y": "auto", "width": "200px", "white-space": "pre-wrap"}
            )
        ),
        rx.table.cell(
            rx.button(
                rx.icon('trash-2'),
                on_click=lambda c_id=contacto.id: Admin.delete_contacto(c_id),
                color="white",
                size="sm"
            )
        )
    )

@rx.page(route="/admin", on_load=Admin.on_load)
@template
def admin() -> rx.Component:
    return rx.cond(
        # Verificar si está autenticado
        (auth.AuthState.user_details['email'] == 'mariostteven@gmail.com') |
        (auth.AuthState.user_details['email'] == 'santurron2004@gmail.com'), 
        # Si está autorizado, renderizar la página de administración
        rx.vstack(
            rx.heading("Administración", font_size="24px"),        
            rx.hstack(
                rx.input(
                    placeholder="Buscar por correo electrónico",
                    on_change=lambda email: Admin.actualizar_filtro(email),  
                    width="300px"
                ),
                rx.button("Buscar", on_click=lambda: Admin.actualizar_filtro(Admin.filtro_email)),
                spacing="10px",
            ),
            rx.text("Trabajadores", font_size="18px"),
            rx.cond(
                Admin.datos_cargados,
                table_trabajadores(Admin.trabajadores),
                rx.spinner()  # Muestra un indicador de carga hasta que se carguen los datos
            ),
            rx.text("Contactos", font_size="18px"),
            rx.cond(
                Admin.datos_cargados,
                table_contactos(Admin.contactos),
                rx.spinner()  # Muestra un indicador de carga hasta que se carguen los datos
            ),
            spacing="30px",
            align="start",
        ),
        
        # Si no está autorizado, mostrar un mensaje de acceso denegado
        rx.text("Acceso denegado: No tienes permiso para acceder a esta página.", font_size="20px", color="red")
    )