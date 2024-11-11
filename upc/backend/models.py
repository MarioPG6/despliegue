import reflex as rx
import sqlmodel
from datetime import datetime,  timezone
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

class Usuario(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)    
    nombre_usuario: str | None = None    
    localidad_usuario: str | None = None

    login: Optional[Login] = sqlmodel.Relationship(back_populates="user")

class Comentario(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    texto_comentario: str
    nombre_usuario: str
    fecha_creacion = sqlmodel.Field(default=datetime.now(timezone.utc)) 
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

    login: Optional[Login] = sqlmodel.Relationship(back_populates="worker")
    comentarios: List[Comentario] = sqlmodel.Relationship(back_populates="trabajador")


class Contacto(rx.Model, table=True):    
    nombre: str | None = None
    correo: str | None = None
    comentario: str | None = None

