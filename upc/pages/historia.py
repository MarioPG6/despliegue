import reflex as rx
from ..template.template import template

@rx.page(route="/historia", title="Historia")
@template
def historia_page() -> rx.Component:
    return rx.box(
        # Título "Historia"
        rx.heading("Historia", color="white", font_size="32px", font_weight="bold", margin_bottom="1em", text_align="center"),
        
        # Primer banner
        rx.box(
            rx.text(
                "En una ciudad tan grande y agitada como Bogotá, donde todos vivimos con prisa, encontrar servicios de emergencia, como cerrajería, plomería o electricidad, puede ser complicado y agotador. Es difícil hallar profesionales cercanos que puedan llegar rápidamente a nuestra casa, especialmente considerando los frecuentes trancones en la ciudad, y que además sean calificados, confiables y ofrezcan precios justos. En respuesta a esta necesidad, surge nuestra página web, diseñada para conectar de manera rápida y eficiente a las personas con los profesionales adecuados cuando más lo necesitan.",
                font_size="18px",
                color="black",
                text_align="justify",
            ),
            bg="#E6F1FD",  # Fondo azul claro
            padding="2em",
            border_radius="8px",
            margin_bottom="1em",
            box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
        ),
        
        # Segundo banner
        rx.box(
            rx.heading("Tu servicio ideal, a un solo click de distancia", color="red", font_size="24px", font_weight="bold", text_align="center"),
            bg="#F0F7FE",  # Fondo azul aún más claro
            padding="2em",
            border_radius="8px",
            margin_bottom="1em",
            box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
        ),
        
        # Tercer banner
        rx.box(
            rx.text(
                "Es una página web que conecta a trabajadores independientes o pequeñas empresas con potenciales clientes que necesitan encontrar rápidamente servicios en sus localidades dentro de Bogotá.",
                font_size="18px",
                color="black",
                text_align="justify",
            ),
            bg="#DCEBF7",  # Otro fondo azul claro
            padding="2em",
            border_radius="8px",
            margin_bottom="1em",
            box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
        ),
        
        # Estilos generales de la página
        padding="4",
        width="100%",
        bg="#003366"  # Fondo de toda la página en azul oscuro
    )