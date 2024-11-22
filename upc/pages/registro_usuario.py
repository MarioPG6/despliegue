import reflex as rx

from ..template.template import template
from ..backend.state import State




@rx.page(route="/registro_usuario",title="Registro Usuario")
@template
def registro_usuario() -> rx.Component:

    return rx.card(
        rx.form.root(
            rx.flex(
                rx.form.field(
                    rx.flex(
                        rx.form.label("Usuario"),
                        rx.form.control(
                            rx.input(
                                placeholder="Digite su nombre",
                                on_change=State.set_user_entered_username,
                                name="nombre_usuario",
                            ),
                            as_child=True,
                        ),
                        rx.cond(
                            State.username_empty,
                            rx.form.message(
                                "Nombre de usuario no puede estar vacío",
                                color="var(--red-11)",
                            ),
                        ),
                        direction="column",
                        spacing="2",
                        align="stretch",
                    ),
                    name="nombre_usuario",
                    server_invalid=State.username_empty,
                ),
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
                        rx.cond(
                            State.email_exists,
                            rx.form.message(
                                "Usuario ya se encuentra registrado", 
                                match="valueMissing",
                                force_match=State.email_exists,                               
                                color="var(--red-11)",
                            ),
                        ),
                        direction="column",
                        spacing="2",
                        align="stretch",
                    ),
                    name="correo_usuario",
                    server_invalid=State.email_exists,
                ),
                rx.form.field(
                    rx.flex(
                        rx.form.label("Localidad: "),
                        rx.select(
                                 ["Antonio Nariño","Barrios Unidos","Bosa", "Chapinero","Ciudad Bolívar","Engativá","Fontibon","Kennedy","La Candelaria","Los Mártires","Puente Aranda"
                                 "Rafael Uribe Uribe","San Cristóbal","Santa Fe","Suba","Sumapaz","Teusaquillo","Tunjuelito","Usaquén","Usme"
                                 ],placeholder="Seleccione su localidad",name="localidad_usuario", value=State.user_entered_localidad,on_change=State.select_localidad
                        )                                           
                    )                        
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
                rx.form.field(
                    rx.flex(                        
                        rx.form.control(
                            rx.input(
                                placeholder="Repita su contraseña",
                                on_change=State.set_user_entered_password2,
                                type="password",
                                name="password_usuario2",
                            ),
                            as_child=True,
                        ),
                        rx.cond(
                            State.password_verify,
                            rx.form.message(
                            "Las contraseñas digitadas no coinciden",
                            match="valueMissing",
                            force_match=State.password_verify,
                            color="var(--red-11)",
                           ),
                        ),                        
                        direction="column",
                        spacing="2",
                        align="stretch",
                    ),
                    name="password_usuario2",
                    server_invalid=State.password_verify,
                ),
                rx.form.field(
                    rx.flex(
                        rx.form.field(
                            name="is_trabajador",
                            type="hidden",
                            value="false",
                        )
                    )
                ),
                rx.input(
                    placeholder="Digite su teléfono",
                    name="telefono_usuario",
                    required=True,
                    on_change=State.set_user_entered_telefono,
                ),
                rx.input(
                    placeholder="Digite su dirección",
                    name="direccion_usuario",
                    required=True,
                    on_change=State.set_user_entered_direccion,
                ),
                rx.form.submit(
                    rx.cond((State.loader),                    
                    rx.button(
                        rx.spinner(loading=True), "Enviar", disabled=True
                    ),
                    rx.button("Enviar", type="submit", disabled=State.input_invalid_usuarios,on_click=State.loader_status),                    
                    ),                   
                    as_child=True,
                    width="10em",
                ),
                rx.cond(State.registro,
                    rx.callout.root(
                    rx.callout.icon(rx.icon(tag="info")),
                    rx.callout.text(
                        State.mensaje_registro
                    ),
                    color_scheme="green",
                    role="alert",
                    )            
                ),                   
                           
                direction="column",
                spacing="4",
                width="25em",
            ),
            on_submit=State.handle_registro_usuario,
            reset_on_submit=True,
             
     ),
      width="30em",
    )   
 
