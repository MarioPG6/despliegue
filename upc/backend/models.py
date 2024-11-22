import reflex as rx
import sqlmodel
from datetime import datetime,  timezone, timedelta
from typing import Optional, List



class Login(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)    
    correo: str
    password: str
    role: str = sqlmodel.Field(default="usuario")
    is_verified: bool = sqlmodel.Field(default=False)     
    user_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="usuario.id")
    worker_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="trabajador.id")

    user: Optional["Usuario"] = sqlmodel.Relationship(back_populates="login")
    worker: Optional["Trabajador"] = sqlmodel.Relationship(back_populates="login")

class UsuarioTrabajador(rx.Model, table=True):
    usuario_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="usuario.id", primary_key=True)
    trabajador_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="trabajador.id", primary_key=True)

    usuario: "Usuario" = sqlmodel.Relationship(back_populates="trabajadores_contratados")
    trabajador: "Trabajador" = sqlmodel.Relationship(back_populates="usuarios_contratadores")

class Usuario(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)    
    nombre_usuario: str | None = None    
    localidad_usuario: str | None = None
    telefono_usuario: str | None = None
    direccion_usuario: str | None = None

    login: Optional[Login] = sqlmodel.Relationship(back_populates="user")

    trabajadores_contratados: List[UsuarioTrabajador] = sqlmodel.Relationship(
        back_populates="usuario"
        #link_model=UsuarioTrabajador
    )
    servicios: List["Servicio"] = sqlmodel.Relationship(back_populates="usuario")

class Comentario(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    texto_comentario: str
    nombre_usuario: str
    fecha_creacion = sqlmodel.Field(default=datetime.now(timezone.utc) - timedelta(hours=5)) 
    trabajador_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="trabajador.id")

    trabajador: Optional["Trabajador"] = sqlmodel.Relationship(back_populates="comentarios")


class Trabajador(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)    
    nombre_trabajador: str | None = None
    telefono_trabajador: str | None = None
    localidad_trabajador: str | None = None
    categoria: str | None = None
    direccion: str | None = None
    descripcion: str | None = None
    thumbs_up: int = sqlmodel.Field(default=0)
    thumbs_down: int = sqlmodel.Field(default=0)
    is_verified: bool = sqlmodel.Field(default=False)

    login: Optional[Login] = sqlmodel.Relationship(back_populates="worker")
    comentarios: List[Comentario] = sqlmodel.Relationship(back_populates="trabajador")

    usuarios_contratadores: List[UsuarioTrabajador] = sqlmodel.Relationship(
        back_populates="trabajador"
    )
    servicios: List["Servicio"] = sqlmodel.Relationship(back_populates="trabajador")


class Servicio(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    usuario_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="usuario.id")
    trabajador_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="trabajador.id")
    estado: str = sqlmodel.Field(default="abierto")  # "abierto" o "cerrado"
    fecha_creacion: datetime = sqlmodel.Field(default=datetime.now(timezone.utc) - timedelta(hours=5))
    fecha_cierre: datetime = sqlmodel.Field(default=datetime.now(timezone.utc) - timedelta(hours=5))
    fecha_inicio: datetime = sqlmodel.Field(default=datetime.now(timezone.utc) - timedelta(hours=5))
   

    usuario: "Usuario" = sqlmodel.Relationship(back_populates="servicios")
    trabajador: "Trabajador" = sqlmodel.Relationship(back_populates="servicios")

class Calificacion(rx.Model, table=True):
    id: int = sqlmodel.Field(default=None, primary_key=True)
    usuario_id: int = sqlmodel.Field(foreign_key="usuario.id")
    trabajador_id: int = sqlmodel.Field(foreign_key="trabajador.id")


class Contacto(rx.Model, table=True):    
    nombre: str | None = None
    correo: str | None = None
    comentario: str | None = None

