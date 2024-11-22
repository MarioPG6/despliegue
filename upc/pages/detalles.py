import reflex as rx

from ..template.template import template
from ..backend.state import State
   


@rx.page(route="/detalles/[id]",title="Detalles de trabajadores",on_load=State.get_trabajador_by_id)
@template
def detalles() -> rx.Component:
    return rx.hstack(
        rx.heading("Detalles del trabajador"),
        rx.cond(State.trabajadores,
            rx.hstack(
            rx.icon('user-round'),
            rx.heading(State.trabajadores[0]['nombre_trabajador']),
            rx.cond((State.user_id == State.login_id) & (State.user_email == State.trabajadores[0].login.correo),
            rx.dialog.root(
            rx.dialog.trigger(rx.button("Editar Perfil", size="2")),
            rx.dialog.content(
                rx.dialog.title("Editar Perfil"),
                rx.dialog.description(
            "Edite su perfil",
            size="2",
            margin_bottom="16px",
        ),        
        rx.flex(
        rx.foreach(
            State.trabajadores,
            lambda trabajador: rx.vstack(
                rx.text(
                    "Nombre:"
                ),
                rx.input(
                   default_value=trabajador.nombre_trabajador,
                   name="nombre_trabajador", 
                ),
                rx.text(
                    "Teléfono:"
                ),
                rx.input(
                   default_value=trabajador.telefono_trabajador,
                   name="telefono_trabajador",
                   on_change=State.set_user_entered_telefono, 
                ),
                rx.text(
                    "Localidad:"
                ),
                rx.select(
                    ["Antonio Nariño","Barrios Unidos","Bosa", "Chapinero","Ciudad Bolívar","Engativá","Fontibon","Kennedy","La Candelaria","Los Mártires","Puente Aranda"
                    "Rafael Uribe Uribe","San Cristóbal","Santa Fe","Suba","Sumapaz","Teusaquillo","Tunjuelito","Usaquén","Usme"
                    ],placeholder="Seleccione su localidad",name="localidad_trabajador",value=State.user_entered_localidad,on_change=State.select_localidad
                ),
                rx.text(
                    "Dirección:"
                ),  
                rx.input(
                   default_value=trabajador.direccion,
                   name="direccion",
                   on_change=State.set_user_entered_direccion, 
                ),
                rx.text(
                    "Servicios:"
                ),  
                rx.text_area(
                   value=trabajador.descripcion,
                   name="descripcion",
                   on_change=State.set_user_entered_descripcion, 
                ),                   
                rx.flex(
                   rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            color_scheme="gray",
                            variant="soft",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button("Guardar"),
                        on_click=State.actualizar_perfil_trabajador,
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
                                        
            ),
        ),                 
    ),
  )  
), )
            ),
        ),            
        rx.cond(
            State.trabajadores,            
            rx.card(
                rx.cond((State.authenticated) & (State.user_id != State.login_id) & (State.role_user != "trabajador"), 
                    rx.hstack(                   
                        rx.button("Contactar",on_click=State.contactar_trabajador(State.trabajadores[0].login.correo,State.trabajadores[0]['nombre_trabajador'],State.user_name,State.telefono_usuario,State.direccion_usuario,State.login_id,State.user_id)),
                                       
                    ),
                    rx.cond((State.user_id != State.login_id) & (State.role_user != "trabajador"),
                        rx.link(rx.text("Debe registrarse para poder contactar al trabajador y hacer comentarios",color="red"),href="/login"),
                    ),    
                ),               
                rx.hstack(
                    rx.text.strong('Localidad:'),
                    rx.text(State.trabajadores[0]['localidad_trabajador']),
                ),
                rx.hstack(
                    rx.text.strong('Especialidad:'),
                    rx.text(State.trabajadores[0]['categoria']),
                ),                
                rx.hstack(
                    rx.text.strong('Descripción:'),
                    rx.text(State.trabajadores[0]['descripcion']),
                ),
                rx.cond((State.authenticated) & (State.user_id != State.login_id) & (State.role_user != "trabajador"),
                    rx.hstack(
                    rx.icon("thumbs-up",on_click=State.calificar_servicio_up),
                    rx.text(State.trabajadores[0]['thumbs_up']),
                    rx.icon("thumbs-down",on_click=State.calificar_servicio_down),
                    rx.text(State.trabajadores[0]['thumbs_down']),          
                    ),
                ),                          
                rx.cond((State.authenticated) & (State.user_id != State.login_id) & (State.role_user != "trabajador"), 
                    rx.form(
                        rx.text_area(placeholder="Deja tu comentario aquí...", value=State.texto_comentario, on_change=State.set_texto_comentario),
                        rx.button("Enviar", on_click=lambda: State.handle_comentario),
                    ),
                ),
                rx.vstack(
                    rx.foreach(
                        State.comentarios,
                        lambda comentario: rx.hstack(
                            rx.vstack(
                                rx.icon('message-circle-more'),  
                                rx.text(comentario.nombre_usuario, font_weight="bold"),
                                rx.text(comentario.fecha_creacion, size="1"),
                                rx.text(comentario.texto_comentario),
                                rx.divider(),
                            ),                           
                        ),
                    ), 
                ),                 
                 style={
                    "max-height": "500px",  
                    "overflow-y": "auto",   
                    "padding": "10px",      
                    "border": "1px solid #ccc",  
                    "border-radius": "5px"   
                },                            
            ),            
            rx.text("Cargando detalles del trabajador...")
        ),
        width="100%",
        height="100%",
        direction="column",
        align_items="stretch",
        
    )