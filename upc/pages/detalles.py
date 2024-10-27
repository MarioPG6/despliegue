import reflex as rx

from ..template.template import template
from ..backend.state import State
from ..backend.models import Trabajador

   
class Detalles(rx.State):
    users: list['Trabajador']  = [] 


@rx.page(route="/detalles/[id]",on_load=State.get_user_by_id)
@template
def detalles() -> rx.Component:    

    return rx.vstack(          
           rx.heading("Detalles del trabajador"),
           rx.icon('gamepad-2'),
           rx.card(
             rx.hstack(
                rx.text('Nombre:'),     
                rx.text(State.users[0]['nombre_trabajador']),
             ),
             rx.hstack(
                rx.text('Correo:'),     
                rx.text(State.users[0]['correo_trabajador']), 
             ),
             rx.hstack(
                rx.text('Teléfono:'),     
                rx.text(State.users[0]['telefono_trabajador']), 
             ),
             rx.hstack(
                rx.text('Localidad:'),     
                rx.text(State.users[0]['localidad_trabajador']), 
             ),
             rx.hstack(
                rx.text('Especialidad:'),     
                rx.text(State.users[0]['categoria']), 
             ),
             rx.hstack(
                rx.text('Dirección:'),     
                rx.text(State.users[0]['direccion']), 
             ),
             rx.hstack(
               rx.text('Descripción:'),     
               rx.text(State.users[0]['descripcion']),
             ),              
           ),
               
      width="100%",
      height="100%",
      direction="column",
      align_items="stretch",               
    )

