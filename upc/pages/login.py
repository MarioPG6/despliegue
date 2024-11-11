import reflex as rx
import reflex.components.radix.primitives as rdxp

from ..template.template import template
from ..backend.state import State


@rx.page(route="/login")
@template
def login():

    return rx.card(
        rx.form.root(
            rx.box(
                rx.text("Bienvenido! Por favor Inicia sesión"),
            ),
            rx.flex(
                rx.form.field(
                    rx.flex(
                        rx.form.label("Correo"),
                        rx.form.control(
                            rx.input(
                                placeholder="Digite su correo",
                                on_change=State.set_user_entered_email,
                                name="correo_usuario",
                            ),
                            as_child=True,
                        ),
                        rx.cond(
                            State.invalid_email,
                            rx.form.message(
                                "Dirección de correo no válida",
                                color="var(--red-11)",
                            ),
                        ),
                        direction="column",
                        spacing="2",
                        align="stretch",
                    ),
                    name="correo_usuario",
                    server_invalid=State.invalid_email,
                ),
                rx.form.field(
                    rx.flex(
                        rx.form.label("Password"),
                        rx.form.control(
                            rx.input(
                                placeholder="Digite su contraseña",
                                on_change=State.set_user_entered_password,
                                type="password",
                                name="password_usuario",
                            ),
                            as_child=True,
                        ),
                        rx.form.message(
                            "Password no debe estar vacío",
                            match="valueMissing",
                            force_match=State.password_empty,
                            color="var(--red-11)",
                        ),
                        direction="column",
                        spacing="2",
                        align="stretch",
                    ),
                    name="password_usuario",
                    server_invalid=State.password_empty,
                ),
                rx.form.submit(
                    rx.cond((State.loader),                    
                    rx.button(
                        rx.spinner(loading=True), "Enviar", disabled=True
                    ),
                    rx.button("Enviar", type="submit", disabled=State.input_invalid,on_click=State.loader_status),                    
                    ),
                    as_child=True,
                    width="10em",
                ),
                 rx.box(
                    rx.text("Aún no te has registrado?"),
                 ),  
                 rx.hstack(
                    rx.icon('user-round'),
                    rx.link("Regístrate como usuario",href="/registro_usuario"),
                 ),
                 rx.hstack(
                    rx.icon('user-round'),
                    rx.link("Regístrate como trabajador",href="/registro_trabajador"),
                 ),  
                rx.cond(State.error_credenciales,
                    rx.callout.root(
                    rx.callout.icon(rx.icon(tag="info")),
                    rx.callout.text(
                        State.mensaje_error_contraseña
                    ),
                    color_scheme="red",
                    role="alert",
                    )            
                ),                       
                direction="column",
                spacing="4",
                width="25em",
            ),
            on_submit=State.handle_login,
            reset_on_submit=True,
             
     ),
      width="30em",     
      
    ) 
   
    
    
