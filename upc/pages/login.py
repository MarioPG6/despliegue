import reflex as rx

from ..template.template import template
from ..backend.state import State
from ..backend.state import State



@rx.page(route="/login",on_load=State.ocultar_mensaje_error)
@template
def login():
    
 return rx.card(  
    rx.form(
        rx.vstack(
        rx.text("Inicio de sesión."),    
        rx.input(
            placeholder="Digite su correo",
            name="correo_usuario",
            required=True,
            width="90%",
            on_change=State.validacion_usuario,  
        ),     
        rx.input(
            placeholder="Digite su password",
            name="password_usuario",
            type='password',
            width="90%",
            on_change=State.validacion_password,        
        ),                               
            rx.button("Enviar", type="submit"),
            rx.cond((State.usuario_invalido) | (State.password_vacio),
                    rx.text("correo en formato inválido o campos vacíos.",color_scheme="red")),              
            rx.cond(State.mensaje_error_contraseña,
                    rx.callout.root(
                    rx.callout.icon(rx.icon(tag="info")),
                    rx.callout.text(
                        State.mensaje_error_contraseña
                    ),
                    color_scheme="red",
                    role="alert",
                )            
            ),            
            
        ),                
        on_submit=State.handle_login,
        reset_on_submit=True,                 
    width="70%",       
   ),
    width="70%",     
 )
