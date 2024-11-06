import reflex as rx

from ..template.template import template
from ..backend.state import State
#from ..backend import auth
#from requests import request
#from ..auth.register import register_user
#from ..auth.verify import verify_account
import jwt
#from ..backend.models import Usuario, Trabajador
#import ast
from ..backend.state import State


@rx.page(route="/verify/[jwt_token]",on_load=State.handle_verificacion)
@template
def verify():
    usuario_verificado = State.verified
    return rx.cond(
        usuario_verificado,
        rx.text("Usuario registrado con éxito"),
        rx.text("Error al registrar usuario"),
    )
 
