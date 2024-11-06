import reflex as rx

from ..template.template import template
from ..backend.state import State
#from ..backend import auth




@rx.page(route="/registro_usuario",title="Registro Usuario")
@template
def registro_usuario() -> rx.Component:
 
 return rx.card(  
    rx.form(
        rx.vstack(
        rx.text("Regístrate."),    
        rx.input(
            placeholder="Digite su nombre",
            name="nombre_usuario",
            required=True,
            width="50%",    
        ),        
        rx.input(
            placeholder="Digite su correo",
            name="correo_usuario",
            width="50%",        
        ),
        rx.input(
            placeholder="Digite su password",
            name="password_usuario",
            type='password',
            width="50%",        
        ),        
        rx.select(
            ["Antonio Nariño","Barrios Unidos","Bosa", "Chapinero","Ciudad Bolívar","Engativá","Fontibon","Kennedy","La Candelaria","Los Mártires","Puente Aranda"
             "Rafael Uribe Uribe","San Cristóbal","Santa Fe","Suba","Sumapaz","Teusaquillo","Tunjuelito","Usaquén","Usme"
            ],
            placeholder="Seleccione su localidad",
            name="localidad_usuario",
            width="50%",          
        ),
        rx.input(
            name="is_trabajador",
            type="hidden",
            value="false"
        ),                                 
            rx.button("Enviar", type="submit"),
            rx.cond(State.did_submit, rx.text("Gracias por su registro")),
            ),
        on_submit=State.handle_registro_usuario,
        reset_on_submit=True,                    
    ),
    width="70%",  
  )