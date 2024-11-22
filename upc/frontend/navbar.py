import reflex as rx
from ..backend.state import State


def navbar_icons_item(text: str, icon: str, url: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4", weight="medium"),
        ),
        href=url,
    )


def navbar_icons_menu_item(text: str, icon: str, url: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=16),
            rx.text(text, size="3", weight="medium"),
        ),
        href=url,
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.png",
                        width="5.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                     rx.heading(
                        "A la vuelta de un Click", size="6", weight="bold"                                            
                     ),                   
                    align_items="center",
                ),                    
                rx.hstack(
                    navbar_icons_item("Home", "home", "/#"),
                    navbar_icons_item(
                        "Buscar", "search", "/busquedas"
                    ),
                    rx.cond(
                        ~(State.authenticated),
                        navbar_icons_item("Ingresa", "user-round-plus", "/login"), 
                    ),    
                    navbar_icons_item(
                        "Contáctanos", "mail", "/contacto"
                    ),       
                    rx.cond(
                        (State.authenticated) & (State.role_user == "usuario"),                                  
                    
                        rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(
                                rx.icon("user"),
                                size="2",
                                radius="full",
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item(rx.text(State.user_name)),
                            rx.menu.item("Perfil", on_click=rx.redirect(f"/perfil_usuario/{State.login_id}")),
                            rx.menu.item("Servicios", on_click=rx.redirect(f"/servicios-usuario/")),                                                        
                            rx.menu.separator(),
                            rx.menu.item("Cerrar sesión",on_click=State.logout),
                        ),
                        justify="end",
                    ),
                    ),
                    rx.cond(
                        (State.authenticated) & (State.role_user == "trabajador"),                                  
                    
                        rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(
                                rx.icon("user"),
                                size="2",
                                radius="full",
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item(rx.text(State.user_name)),
                            rx.menu.item("Perfil", on_click=rx.redirect(f"/detalles/{State.login_id}")),
                            rx.menu.item("Servicios", on_click=rx.redirect(f"/servicios-trabajador/")),                                                         
                            rx.menu.separator(),
                            rx.menu.item("Cerrar sesión",on_click=State.logout),
                        ),
                        justify="end",
                    ),
                    ),
                    rx.cond(
                        ( ((State.user_email == 'mariostteven@gmail.com') | (State.user_email == 'santurron2004@gmail.com') | (State.user_email == 'dylan-lozano@upc.edu.co'))) &  (State.authenticated),                                  
                    
                        rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(
                                rx.icon("user-round-cog"),               
                                size="2",
                                radius="full",
                            )
                        ),
                        rx.menu.content(                            
                            rx.menu.item("Validador", on_click=rx.redirect(f"/validador")),
                            rx.menu.separator(), 
                            rx.menu.item("Administración", on_click=rx.redirect(f"/admin")),
                            rx.menu.separator(), 
                            rx.menu.item("Gerencia", on_click=rx.redirect(f"/gerente")),                                                         
                        ),
                        justify="end",
                    ),
                    ),
                    
                    justify="between",
                    align_items="center",                  
                                      
                    spacing="6",
                ),                    
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.png",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "A la vuelta de un clic", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        navbar_icons_menu_item(
                            "Home", "home", "/#"
                        ),
                        navbar_icons_menu_item(
                            "Buscar", "search", "/busquedas"
                        ),
                        rx.cond(
                            ~(State.authenticated),
                            navbar_icons_item("Ingresa", "user-round-plus", "/login"), 
                        ), 
                        navbar_icons_menu_item(
                            "Contáctanos", "mail", "/contacto"
                        ),
                         rx.cond(
                        (State.authenticated) & (State.role_user == "usuario"),                                  
                    
                        rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(
                                rx.icon("user"),
                                size="2",
                                radius="full",
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item(rx.text(State.user_name)),
                            rx.menu.item("Perfil", on_click=rx.redirect(f"/perfil_usuario/{State.login_id}")),
                            rx.menu.item("Servicios", on_click=rx.redirect(f"/servicios-usuario/")),                                                        
                            rx.menu.separator(),
                            rx.menu.item("Cerrar sesión",on_click=State.logout),
                        ),
                        justify="end",
                    ),
                    ),
                    rx.cond(
                        (State.authenticated) & (State.role_user == "trabajador"),                                  
                    
                        rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(
                                rx.icon("user"),
                                size="2",
                                radius="full",
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item(rx.text(State.user_name)),
                            rx.menu.item("Perfil", on_click=rx.redirect(f"/detalles/{State.login_id}")),
                            rx.menu.item("Servicios", on_click=rx.redirect(f"/servicios-trabajador/")),                                                         
                            rx.menu.separator(),
                            rx.menu.item("Cerrar sesión",on_click=State.logout),
                        ),
                        justify="end",
                    ),
                    ),
                    rx.cond(
                        ( ((State.user_email == 'mariostteven@gmail.com') | (State.user_email == 'santurron2004@gmail.com') | (State.user_email == 'dylan-lozano@upc.edu.co'))) &  (State.authenticated),                                  
                    
                        rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(
                                rx.icon("user-round-cog"),               
                                size="2",
                                radius="full",
                            )
                        ),
                        rx.menu.content(                            
                            rx.menu.item("Validador", on_click=rx.redirect(f"/validador")),
                            rx.menu.separator(), 
                            rx.menu.item("Administración", on_click=rx.redirect(f"/admin")),
                            rx.menu.separator(), 
                            rx.menu.item("Gerencia", on_click=rx.redirect(f"/gerente")),                                                         
                        ),
                        justify="end",
                    ),
                    ),
                ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )