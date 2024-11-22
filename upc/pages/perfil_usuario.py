import reflex as rx

from ..template.template import template
from ..backend.state import State


  

@rx.page(route="/perfil_usuario/[id]",title="Perfil del usuario",on_load=State.get_usuario_by_id)
@template
def perfil_usuario() -> rx.Component:

      
 return  rx.cond(State.usuarios,
   rx.cond((State.user_id == State.login_id) & (State.usuarios[0].login.correo == State.user_email),   
            
   rx.vstack(    
    rx.icon('user-round',size=60),
    rx.text("Bienvenido"),
    rx.text.strong(State.user_name),
    rx.vstack(
        rx.text("Bienvenido a su perfil de usuario, desde aquí puede actualizar sus datos de contacto."),   
    ),      
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
            State.usuarios,
            lambda usuario: rx.vstack(                
                rx.text(
                    "Localidad:"
                ),
                rx.select(
                    ["Antonio Nariño","Barrios Unidos","Bosa", "Chapinero","Ciudad Bolívar","Engativá","Fontibon","Kennedy","La Candelaria","Los Mártires","Puente Aranda"
                    "Rafael Uribe Uribe","San Cristóbal","Santa Fe","Suba","Sumapaz","Teusaquillo","Tunjuelito","Usaquén","Usme"
                    ],placeholder="Seleccione su localidad",name="localidad_usuario",value=State.user_entered_localidad,on_change=State.select_localidad
                ),
                rx.text(
                    "Teléfono:"
                ),
                rx.input(
                   default_value=usuario.telefono_usuario,
                   name="telefono_usuario",
                   on_change=State.set_user_entered_telefono, 
                ),
                rx.text(
                    "Dirección:"
                ),  
                rx.input(
                   default_value=usuario.direccion_usuario,
                   name="direccion_usuario",
                   on_change=State.set_user_entered_direccion, 
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
                        on_click=lambda: State.actualizar_perfil_usuario,
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
                                        
            ),
        ),                 
    ),
  )
 )
),
rx.callout.root(
    rx.callout.icon(rx.icon(tag="info")),
    rx.callout.text(
        "Acceso restringido, solo usuarios registrados y con los permisos necesarios pueden ver esta sección."
    ),
    color_scheme="red",
    role="alert",
    ),          
 )
)
