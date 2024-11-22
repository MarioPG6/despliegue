import reflex as rx
from ..template.template import template
from ..backend.state import State
from ..backend.models import Trabajador, Login
from sqlmodel import select
from sqlalchemy.orm import selectinload
from email.message import EmailMessage
import smtplib



class Validador(rx.State):
    trabajadores_unverified: list[Trabajador] = []
    trabajadores_verified: list[Trabajador] = []
    GMAIL_KEY = "ycrp jrgi ekuw gpdo"


    filtro_email: str = ""  # Filtro para el correo electrónico
    datos_cargados: bool = False  # Indicador para verificar si los datos están cargados

    # Método para cargar los datos con filtro
    def on_load(self):
        self.trabajadores_unverified = self.get_trabajador_by_unverified()
        self.trabajadores_verified = self.get_trabajador_by_verified()
        self.datos_cargados = True


    # Método para actualizar la búsqueda y recargar datos
    def actualizar_filtro(self, email: str):
        self.filtro_email = email
        self.trabajadores_unverified = self.get_trabajador_by_unverified()
        self.trabajadores_verified = self.get_trabajador_by_verified()
        

    def  get_trabajador_by_verified(self):
        with rx.session() as session:
            query = (
                select(Trabajador)
                .join(Login, Trabajador.id == Login.worker_id)
                .options(selectinload(Trabajador.login))
                .where(Trabajador.is_verified == 1) 
            )
            if self.filtro_email:
                query = query.where(Login.correo.contains(self.filtro_email))  
            return session.exec(query).all() or []         
        
    def  get_trabajador_by_unverified(self):
        with rx.session() as session:
            query = (
                select(Trabajador)
                .join(Login, Trabajador.id == Login.worker_id)
                .options(selectinload(Trabajador.login))
                .where(Trabajador.is_verified == 0) 
            )
            if self.filtro_email:
                query = query.where(Login.correo.contains(self.filtro_email))  
            return session.exec(query).all() or []   

    def send_validation_email(self, email, usuario):
        print(f"Ingresó a envio de email de validación a {email} para el usuario {usuario}")
        link = f"http://alavueltadeunclick.com:3000/login"
        msg = EmailMessage()
        msg.set_content(f"""Enhorabuena {usuario}! su cuenta como trabajador ha sido aceptada!, 
                        ahora puede inciar sesión y empezar a usar nuestra plataforma para ofrecer
                        sus servicios: {link}""")
        msg['Subject'] = "[alavueltadeunclic - Cuenta de trabajador aprobada]"
        msg['From'] = "santurron2004@gmail.com"
        msg['To'] = email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("santurron2004@gmail.com", self.GMAIL_KEY)
            server.send_message(msg)    

    def set_trabajador_verified(self, trabajador_id: int):        
       
        with rx.session() as session:
            trabajador = session.exec(select(Trabajador).where(Trabajador.id == trabajador_id)).first()    
            if trabajador:            
               trabajador.is_verified= 1 
               session.add(trabajador)
               session.commit()
               self.send_validation_email(trabajador.login.correo,trabajador.nombre_trabajador)
               self.on_load() 
               yield rx.toast.success("Trabajador validado con éxito!")

    def set_trabajador_unverified(self, trabajador_id: int):        
       
        with rx.session() as session:
            trabajador = session.exec(select(Trabajador).where(Trabajador.id == trabajador_id)).first()    
            if trabajador:            
               trabajador.is_verified= 0 
               session.add(trabajador)
               session.commit()
               self.on_load()                
               yield rx.toast.warning("Trabajador ha sido marcado como no verificado!") 
                                        


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
            style={"width": "100%"}
        ),
        style={"max-height": "160px", "overflow-y": "auto", "width": "100%"}
    )

def row_trabajador(trabajador: Trabajador) -> rx.Component:    
    
    return rx.table.row(
        rx.table.cell(trabajador.nombre_trabajador, style={"max-width": "100px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.login.correo, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.telefono_trabajador, style={"max-width": "100px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.localidad_trabajador, style={"max-width": "100px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.categoria, style={"max-width": "100px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(trabajador.direccion, style={"max-width": "150px", "overflow": "hidden", "text-overflow": "ellipsis"}),
        rx.table.cell(
            rx.alert_dialog.root(
                rx.cond(trabajador.is_verified,
                rx.alert_dialog.trigger(                    
                    rx.icon("user-x"),                    
                ),
                 rx.alert_dialog.trigger(                    
                    rx.icon("user-round-check"),                    
                ),),
                rx.cond(trabajador.is_verified,
                rx.alert_dialog.content(
                    rx.alert_dialog.title("Anular validación"),
                    rx.alert_dialog.description(
                        "¿Desea anular esta validación? El trabajador deberá comenzar el proceso desde cero",
                    ),
                    rx.flex(
                        rx.alert_dialog.cancel(
                            rx.button("Cancelar"),
                        ),
                        rx.alert_dialog.action(
                            rx.button("Anular"),
                            on_click=lambda t_id=trabajador.id: Validador.set_trabajador_unverified(t_id),
                        ),
                        spacing="3",
                    ),
                ),
                rx.alert_dialog.content(
                    rx.alert_dialog.title("Validar usuario"),
                    rx.alert_dialog.description(
                        "¿Desea validar este trabajador?, Recuerde haber finalizado todo el proceso de verificación antes de continuar.",
                    ),
                    rx.flex(
                        rx.alert_dialog.cancel(
                            rx.button("Cancelar"),
                        ),
                        rx.alert_dialog.action(
                            rx.button("Validar"),
                            on_click=lambda t_id=trabajador.id: Validador.set_trabajador_verified(t_id),
                        ),
                        spacing="3",
                    ),
                ),)
            )
        ),   
    )


@rx.page(route="/validador", on_load=Validador.on_load)
@template
def validador() -> rx.Component:   
    return rx.cond(  ((State.user_email == 'mariostteven@gmail.com') | (State.user_email == 'santurron2004@gmail.com') | (State.user_email == 'dylan-lozano@upc.edu.co') | (State.user_email == 'laura-cardenas11@upc.edu.co') | (State.user_email == 'juandavidmurray30@gmail.com')) &  (State.authenticated),  
            rx.vstack(
            rx.heading("Módulo Validador", font_size="24px"),
            rx.text("Este módulo le permite validar trabajadores registrados una vez haya finalizado el proceso de verificación de datos poniéndose en contacto con el trabajador"),
            rx.hstack(
                rx.input(
                    placeholder="Buscar por correo electrónico",
                    on_change=lambda email: Validador.actualizar_filtro(email),  
                    width="300px"
                ),
                rx.button("Buscar", on_click=lambda: Validador.actualizar_filtro(Validador.filtro_email)),
                spacing="10px",
            ),       
            rx.text("Trabajadores por verificar", font_size="18px"),
            rx.cond(
                Validador.datos_cargados,
                table_trabajadores(Validador.trabajadores_unverified),
                rx.spinner()  
            ),
            rx.hstack(
                rx.text.strong("Trabajadores verificados", font_size="18px"),
                rx.icon("award",color="yellow"),
            ),    
            rx.cond(
                Validador.datos_cargados,
                table_trabajadores(Validador.trabajadores_verified),
                rx.spinner() 
            ),               
            spacing="30px",
            align="start",
           ),
           rx.callout.root(
                rx.callout.icon(rx.icon(tag="info")),
                rx.callout.text(
                    "Acceso restringido, solo los validadores tienen acceso a esta sección"
                ),
                color_scheme="red",
                role="alert",
            ),   
    )   