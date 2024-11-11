import reflex as rx

from ..template.template import template
from ..backend.state import State
from ..backend.state import State


@rx.page(route="/verify/[jwt_token]",on_load=State.handle_verificacion)
@template
def verify()-> rx.Component:
    usuario_verificado = State.verified
    return rx.cond(
        usuario_verificado,
        rx.callout.root(
            rx.callout.icon(rx.icon(tag="info")),
            rx.callout.text(
                "Usuario registrado con éxito, ahora puede iniciar sesión",
                rx.link(' AQUI',href="/login")
            ),
            color_scheme="green",
            role="alert",
            ),
        rx.callout.root(
            rx.callout.icon(rx.icon(tag="info")),
            rx.callout.text(
                "Error al verificar su cuenta de usuario"
            ),
            color_scheme="red",
            role="alert",
            ),
    )
 
