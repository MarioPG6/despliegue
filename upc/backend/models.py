import reflex as rx

class Usuario(rx.Model, table=True):    
    nombre_usuario: str | None = None
    correo_usuario: str | None = None
    localidad_usuario: str | None = None


class Trabajador(rx.Model, table=True):    
    nombre_trabajador: str | None = None
    correo_trabajador: str | None = None
    telefono_trabajador: str | None = None
    localidad_trabajador: str | None = None
    categoria: str | None = None
    direccion: str | None = None
    descripcion: str | None = None

class Contacto(rx.Model, table=True):    
    nombre: str | None = None
    correo: str | None = None
    comentario: str | None = None

