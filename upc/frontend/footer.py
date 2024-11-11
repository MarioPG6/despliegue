import reflex as rx


def footer_item(text: str, href: str) -> rx.Component:
    return rx.link(rx.text(text, size="3"), href=href)


def footer_items() -> rx.Component:
    return rx.flex(
        rx.heading(
            "Sobre nosotros", size="4", weight="bold", as_="h3"
        ),
        footer_item("Conoce el equipo", "/#"),
        footer_item("Historia", "/historia"),        
        spacing="4",
        text_align=["center", "center", "start"],
        flex_direction="column",
    )



def social_link(icon: str, href: str) -> rx.Component:
    return rx.link(rx.icon(icon), href=href)


def socials() -> rx.Component:
    return rx.flex(
        social_link("instagram", "http://www.instagram.com"),
        social_link("twitter", "http://www.x.com"),
        social_link("facebook", "http://www.facebook.com"),
        social_link("linkedin", "http://www.linkedin.com"),
        spacing="3",
        justify_content=["center", "center", "end"],
        width="100%",
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.divider(),
        rx.vstack(            
            rx.flex(
                footer_items()     
            ),
            rx.divider(),
            rx.flex(
                rx.hstack(
                    rx.image(
                        src="/upc.png",
                        width="3em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.text(
                        "© 2024 Universidad Piloto de Colombia",
                        size="3",
                        white_space="nowrap",
                        weight="medium",
                    ),
                    spacing="2",
                    align="center",
                    justify_content=[
                        "center",
                        "center",
                        "start",
                    ],
                    width="100%",
                ),
                socials(),
                spacing="4",
                flex_direction=["column", "column", "row"],
                width="100%",
            ),
            spacing="5",
            width="100%",
        ),
        width="100%",
    )