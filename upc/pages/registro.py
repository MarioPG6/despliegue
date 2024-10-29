import reflex as rx

from ..template.template import template
from ..backend.state import State



@rx.page(route="/registro",title="Registro")
@template
def registro() -> rx.Component:

 return rx.card(  
    rx.form(
        rx.vstack(
        rx.text("Regístrate."),    
        rx.input(
            placeholder="Digite su nombre",
            name="nombre_trabajador",
            required=True,
            width="50%",    
        ),
        rx.input(
            placeholder="Digite su correo",
            name="correo_trabajador",
            width="50%",
        ),
        rx.input(
            placeholder="Digite su teléfono",
            name="telefono_trabajador",
            width="50%",
        ),
        rx.select(
            ["Antonio Nariño","Barrios Unidos","Bosa", "Chapinero","Ciudad Bolívar","Engativá","Fontibon","Kennedy","La Candelaria","Los Mártires","Puente Aranda"
             "Rafael Uribe Uribe","San Cristóbal","Santa Fe","Suba","Sumapaz","Teusaquillo","Tunjuelito","Usaquén","Usme"
            ],
            placeholder="Seleccione su localidad",
            name="localidad_trabajador",
            width="50%",          
        ),
        rx.select(
            ["Reparaciones","Cerrajería","Instalaciones", "Pintura"," Ciudad Bolívar","Obras","Belleza y Peluquería","Clases","Electricistas","Aseo","Plomería"],
            placeholder="Seleccione una categoría",
            name="categoria",
            width="50%",          
        ),
        rx.input(
            placeholder="Digite su dirección",
            name="direccion",
            width="50%",
        ),
        rx.text_area(
            placeholder="Describa sus servicios",
            name="descripcion",
            width="50%",            
        ),                               
            rx.button("Enviar", type="submit"),
            rx.cond(State.did_submit, rx.text("Gracias por su registro")),
            ),
        on_submit=State.handle_registro,
        reset_on_submit=True,                    
    ),
    width="70%",  
  )