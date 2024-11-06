import reflex as rx
from ..template.template import template

@rx.page(route="/tipo_usuario",title="Tipo de Usuario")
@template
def tipo_usuario() -> rx.Component:

    return rx.vstack(
        rx.text("Seleccione su tipo de usuario para continuar:"),
        rx.vstack(
            rx.text.strong("Trabajador",size=24),
            rx.alert_dialog.root(
                rx.alert_dialog.trigger(
                    rx.icon('user-round-check',size=64),
                ),
                rx.alert_dialog.content(
                    rx.alert_dialog.title("Registrarse como trabajador"),
                    rx.alert_dialog.description(
                        "Registrate como usuario si deseas ofrcer tus servicios en tu localidad. ¿Deseas continuar?",
                    ),
                    rx.flex(
                        rx.alert_dialog.cancel(
                            rx.button("Cancelar"),
                        ),
                        rx.alert_dialog.action(
                            rx.button("Continuar",on_click=rx.redirect('/registro')),
                        ),
                        spacing="3",
                    ),
                ),
            ) 
        ),

        rx.vstack(
            rx.text.strong("Usuario",size=24),
            rx.alert_dialog.root(
                rx.alert_dialog.trigger(
                    rx.icon('user-round',size=64),
                ),
                rx.alert_dialog.content(
                    rx.alert_dialog.title("Registrarse como usuario"),
                    rx.alert_dialog.description(
                        "Registrate como usuario si deseas contratar trabajadores en tu localidad. ¿Deseas continuar?",
                    ),
                    rx.flex(
                        rx.alert_dialog.cancel(
                            rx.button("Cancelar"),
                        ),
                        rx.alert_dialog.action(
                            rx.button("Continuar",on_click=rx.redirect('/registro_usuario')),
                        ),
                        spacing="3",
                    ),
                ),
            ) 
        ),
    )