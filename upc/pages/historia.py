import reflex as rx
from ..template.template import template
from ..backend.state import State
from ..backend.models import Trabajador

@rx.page(route="/historia", title="historia")
@template
def historia_page() -> rx.Component:
    return rx.box(
        # Contenedor del título "Historia" con un banner delgado
        rx.box(
            rx.heading(
                "Historia",
                color="white",
                font_size="32px",
                font_weight="bold",
                text_align="center",
            ),
            bg="#003366",  # Fondo del banner en azul oscuro
            padding="0.5em",  # Hacer el banner más delgado
            border_radius="8px",
            margin_bottom="1em",
            box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
        ),
        # Contenedor de texto e imagen lado a lado
        rx.flex(
            # Sección de texto
            rx.box(
                rx.heading("¿Por qué surgió nuestra página?", color="#2e6fdb", font_size="20px", font_weight="bold", margin_bottom="0.25em"),
                rx.text(
                    "Nuestra página web surge de la idea de conectar de manera rápida y eficiente a las personas con los profesionales adecuados cuando más lo necesitan, en una ciudad como Bogotá, donde encontrar servicios de emergencia puede ser complicado. Nuestro propósito es conectar a las personas con profesionales confiables y cercanos.",
                    font_size="16px",
                    color="black",
                    text_align="justify",
                ),
                padding="0.5em",
                flex="1",
            ),
            
            # Imagen
            rx.image(
                src="/historia.png",  # Ruta a la imagen
                alt="Misión de la empresa",
                width="45%",  # Ajustar el ancho de la imagen
                height="200px", 
                border_radius="8px",
                box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
            ),
            justify_content="space-between",
            align_items="center",
            padding="1em",
            bg="#bfcde5",  # Fondo azul claro
            border_radius="8px",
            margin_bottom="0.5em",
            box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
            direction="row",  # Lado a lado
        ),
        
        # Otros banners de tu página
        
        # Segundo banner con la fuente Tan Songbird
        rx.box(
            rx.heading(
                "¡¡SOMOS TU SERVICIO IDEAL, A SOLO UN CLIC DE DISTANCIA!!",
                color="#ffffff",
                font_size="26px",
                font_weight="bold",
                text_align="center",
                font_family="Trebuchet MS, sans-serif" # Aquí se aplica la fuente Tan Songbird
            ),
            bg="#2a659f",  # Fondo azul aún más claro
            padding="2em",
            border_radius="8px",
            margin_bottom="1em",
            box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
        ),
        
        # Tercer banner con imagen a la izquierda y texto a la derecha
        rx.flex(
            rx.image(
        src="/ala.png",  # Ruta a la imagen
        alt="Conexión con profesionales",
        width="35%",  # Ajustar el ancho de la imagen
        height="200px",  # Reducir la altura de la imagen
        border_radius="8px",
        box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
    ),
    
    # Texto
    rx.box(
        rx.heading("¿Qué lograremos?", color="#0a8985", font_size="20px", font_weight="bold", margin_bottom="0.25em"),
        rx.text(
            "Somos cinco jóvenes comprometidos a dar lo mejor de nosotros. Trabajamos y seguiremos trabajando para cumplir tus expectativas, para que tú seas parte de esta historia al contratar servicios de calidad a través de nuestra página y apoyando a emprendedores y pequeñas empresas, construiremos juntos un futuro más próspero.",
            font_size="18px",
            color="black",
            text_align="justify",
        ),
        padding="1.5em",  # Reducir el padding para hacer el banner más pequeño
        flex="1",  # El texto ocupa el espacio restante
    ),
    justify_content="space-between",
    align_items="center",
    padding="0.75em",  # Reducir padding general para hacer el banner más pequeño
    bg="#DCEBF7",  # Otro fondo azul claro
    border_radius="8px",
    margin_bottom="1em",
    box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
    direction="row",  # Lado a lado
),
        
        # Estilos generales de la página
        padding="4",
        width="100%",
        bg="bfe5d9"  # Fondo de toda la página en blanco
    )