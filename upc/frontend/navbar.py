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
                        "A la vuelta de un clic", size="6", weight="bold"                                            
                     ),                   
                    align_items="center",
                ),
                rx.hstack(
                    navbar_icons_item("Home", "home", "/#"),
                    navbar_icons_item(
                        "Buscar", "search", "/#"
                    ),
                    rx.cond(
                        (State.role_user == 'usuario'),
                        navbar_icons_item("Regisístrate", "user-round-plus", "/registro"), 
                    ),    
                    navbar_icons_item(
                        "Contáctanos", "mail", "/contacto"
                    ),       
                    rx.cond(
                        State.authenticated,                                           
                        rx.button("Logout", on_click=State.logout),                            
                        rx.button("Login", on_click=rx.redirect('/login')),
                    ),
                    # rx.cond(
                    #     (auth.AuthState.user_details['email'] == 'herradacesar@hotmail.com') |
                    #     (auth.AuthState.user_details['email'] == 'santurron2004@gmail.com'),                                          
                    #     rx.button(rx.icon('user-round-cog'), on_click=rx.redirect("/admin")),                  
                    # ),                    
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
                            "Buscar", "search", "/#"
                        ),
                        navbar_icons_menu_item(
                            "Regístrate", "user-round-plus", "/#"
                        ),
                        navbar_icons_menu_item(
                            "Contáctanos", "mail", "/#"
                        ),
                        rx.cond(
                        State.authenticated,                                           
                        rx.button("Logout", on_click=State.logout),                            
                        rx.button("Login", on_click=rx.redirect('/login')),
                        ),
                        #     rx.cond(
                        #     (auth.AuthState.user_details['email'] == 'mariostteven@gmail.com') |
                        #     (auth.AuthState.user_details['email'] == 'santurron2004@gmail.com'),                                          
                        #     rx.button(rx.icon('user-round-cog'), on_click=rx.redirect("/admin")),                  
                        # ),  
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