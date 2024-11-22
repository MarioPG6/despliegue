import reflex as rx

from ..template.template import template
from ..backend.state import State




@rx.page(route="/registro_trabajador",title="Registro Trabajador")
@template
def registro_trabajador() -> rx.Component:

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
                                name="nombre_trabajador",
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
                    name="nombre_trabajador",
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
                                "Trabajador ya se encuentra registrado", 
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
                        rx.form.label("Localidad: "),
                        rx.select(
                                 ["Antonio Nariño","Barrios Unidos","Bosa", "Chapinero","Ciudad Bolívar","Engativá","Fontibon","Kennedy","La Candelaria","Los Mártires","Puente Aranda"
                                 "Rafael Uribe Uribe","San Cristóbal","Santa Fe","Suba","Sumapaz","Teusaquillo","Tunjuelito","Usaquén","Usme"
                                 ],placeholder="Seleccione su localidad",name="localidad_trabajador",value=State.user_entered_localidad,on_change=State.select_localidad
                        )                                           
                    )                        
                ),
                rx.form.field(
                    rx.flex(
                        rx.form.label("Categoría: "),
                        rx.select(
                                 ["Cerrajería","Pintura","Obras"],
                                  placeholder="Seleccione su categoría",name="categoria", value=State.user_entered_categoria,on_change=State.select_categoria
                        )                                           
                    )                        
                ),              
                rx.input(
                    placeholder="Digite su teléfono",
                    name="telefono_trabajador",
                    required=True,
                    on_change=State.set_user_entered_telefono,
                ),
                rx.input(
                    placeholder="Digite su dirección",
                    name="direccion",
                    required=True,
                    on_change=State.set_user_entered_direccion,
                ),
                rx.input(
                    name="is_trabajador",
                    type="hidden",
                    value="true"
                ),                    
                rx.text_area(
                    placeholder="Describa sus servicios",
                    name="descripcion",
                    width="100%", 
                    required=True,
                    on_change=State.set_user_entered_descripcion,           
                ),                
                rx.form.submit(
                    rx.cond((State.loader),                    
                    rx.button(
                        rx.spinner(loading=True), "Enviar", disabled=True
                    ),
                    rx.button("Enviar", type="submit", disabled=State.input_invalid_trabajadores,on_click=State.loader_status),                    
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