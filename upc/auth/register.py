# auth/register.py
import reflex as rx
import jwt
import datetime
import smtplib

from ..backend.models import Usuario, Trabajador, Login
from email.message import EmailMessage
from werkzeug.security import generate_password_hash

SECRET_KEY = "e85a85be384f74c22bbe0b93ba3404fe3ad75e2346c061c38ba4f77ea6971d35"
GMAIL_KEY = "ycrp jrgi ekuw gpdo"

def register_user(form_data: dict):
    nombre_usuario = form_data.get('nombre_usuario')
    correo_usuario = form_data.get('correo_usuario')
    password_usuario = form_data.get('password_usuario')
    localidad_usuario = form_data.get('localidad_usuario')   
    is_trabajador = form_data.get('is_trabajador', False)
    nombre_trabajador = form_data.get('nombre_trabajador')
    localidad_trabajador = form_data.get('localidad_trabajador')
    telefono_trabajador = form_data.get('telefono_trabajador')
    categoria = form_data.get('categoria')
    direccion = form_data.get('direccion')
    descripcion = form_data.get('descripcion')



    hashed_password = generate_password_hash(password_usuario)

    with rx.session() as session:
        if is_trabajador:
            # Crear un nuevo objeto Trabajador
            new_worker = Trabajador(
                nombre_trabajador=nombre_trabajador,
                localidad_trabajador=localidad_trabajador,
                telefono_trabajador=telefono_trabajador,
                categoria=categoria,
                direccion=direccion,
                descripcion=descripcion,
                # Añadir campos adicionales necesarios para Trabajador
            )
            session.add(new_worker)
            session.commit()
            session.refresh(new_worker)

            # Crear un nuevo Login asociado al Trabajador
            new_login = Login(correo=correo_usuario, password=hashed_password, worker_id=new_worker.id,role="trabajador")
        else:
            # Crear un nuevo objeto Usuario
            new_user = Usuario(nombre_usuario=nombre_usuario, localidad_usuario=localidad_usuario)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            # Crear un nuevo Login asociado al Usuario
            new_login = Login(correo=correo_usuario, password=hashed_password, user_id=new_user.id)

        session.add(new_login)
        session.commit()

        #user_id = new_login.user_id if not is_trabajador else new_login.worker_id
        # Generar un token de verificación
        token = jwt.encode({
            'user_id': new_login.id,
            'user_type': 'trabajador' if is_trabajador else 'usuario',
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24),
        }, SECRET_KEY, algorithm="HS256")
        
        # Enviar el correo de verificación
        send_verification_email(correo_usuario, token)  

def send_verification_email(email, token):
    verification_link = f"http://localhost:3000/verify/{token}"
    msg = EmailMessage()
    msg.set_content(f"Haga clic para verificar su cuenta: {verification_link}")
    msg['Subject'] = "[alavueltadeunclic - Verificación de cuenta]"
    msg['From'] = "santurron2004@gmail.com"
    msg['To'] = email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("santurron2004@gmail.com", GMAIL_KEY)
        server.send_message(msg)
