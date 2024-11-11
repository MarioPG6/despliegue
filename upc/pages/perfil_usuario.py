import reflex as rx

from ..template.template import template
from ..backend.state import State
from ..backend.models import Usuario
 


@rx.page(route="/perfil_usuario/[id]",title="Perfil del usuario",on_load=State.get_usuario_by_id)
@template
def perfil_usuario() -> rx.Component:

      
 return  rx.cond(State.usuarios,
   rx.cond((State.user_id == State.login_id) & (State.usuarios[0].login.correo),   
            
   rx.vstack(
    rx.icon('user-round',size=60),
    rx.text("Bienvenido"),
    rx.text.strong(State.user_name),
    rx.vstack(
        rx.text("Actualmente los usuarios solo deben proporcionar la localidad en la cual se encuentran, desde aquí puedes cambiarla, más adelante se incluirán en tu perfil los trabajadores que se encuentren en tu zona."),   
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
                        on_click=State.actualizar_perfil_usuario,
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
    )            
 ) 
)