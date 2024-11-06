import reflex as rx
import asyncio
import jwt
import datetime
import time
import re
import threading
import smtplib
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from email.message import EmailMessage
from sqlmodel import select
from sqlalchemy.orm import selectinload



from .models import Trabajador
from .models import Usuario
from .models import Login
from .models import Contacto
    

class State(rx.State): 
    trabajadores: list['Trabajador']  = []  
    form_data: dict = {}
    did_submit: bool = False
    submit_msg: str
    token: str = ""
    verified: bool = False
    authenticated: bool = False
    usuario_invalido: bool = False
    password_vacio: bool = False
    mensaje_error_contraseña: str
    error_credenciales: bool = False
    id_user: str
    user_name: str
    role_user: str
    password: str
    user_email: str
    SECRET_KEY = "e85a85be384f74c22bbe0b93ba3404fe3ad75e2346c061c38ba4f77ea6971d35"
    GMAIL_KEY = "ycrp jrgi ekuw gpdo"
   

    #Variable para obtener id de usuario de la url /detalles
    @rx.var
    def user_id(self):
        return self.router.page.params.get("id", "")
        
    #Variable para obtener el token de la url /verify
    @rx.var
    def get_token(self):
        return self.router.page.params.get("jwt_token", "")    
    
    # @rx.var
    # def usuario_invalido(self) -> bool:
    #     return not (re.match (r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$", self.user_name))
    
    # @rx.var
    # def usuario_vacio(self) -> bool:
    #     return not self.user_name.strip()
    
    # @rx.var
    # def password_vacio(self) -> bool:
    #     return not self.password.strip()
    
    @rx.var
    def validar_campos(self) -> bool:
        return (
            self.usuario_invalido
            #or self.usuario_vacio
            or self.password_vacio
        )
       

    ######METODO PARA GENERAR TOKEN JWT######
    '''
    Este método recibe como parámetro los valores que se deben poner en el token
    luego genera el token y lo almacena en la variable de estado 'token' y llama
    al final llama método decode_token para inciar la decodificación del mismo.
    '''
    def generate_token(self, user_id, name, email, role):

        print("Inicia proceso generación de token")

        user_id = str(user_id)
        user_name = str(name)
        email = str(email)
        role = str(role)

        token = jwt.encode({
            'user_id': user_id,
            'email': email,
            'role': role,
            'nombre': user_name,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24),
        }, self.SECRET_KEY, algorithm="HS256")
        
        self.token = token
        print(f"Nuevo token generado: {self.token}")

        self.decode_token() #Llama método para iniciar decodificación de token
     ######FIN METODO PARA GENERAR TOKEN JWT######    


    
    ######METODO PARA DECODIFICAR TOKEN JWT######
    '''
    Este método toma el token almacenado en la variable de estado 'token' y lo decodifica
    para obtener los datos que contiene y ponerlos en variables, los datos que se obtienen
    del token son: user_id, nombre, email y role,
    '''
    def decode_token(self):

        print("Inicia proceso de decodificación de token")
        

        if not self.token:
            print("No se ha generado ningún token")
            return None

        try:
            decoded_data = jwt.decode(self.token, self.SECRET_KEY, algorithms=["HS256"])

            self.id_user = decoded_data['user_id']
            self.role_user = decoded_data['role']
            self.user_name = decoded_data['nombre']
            self.user_email = decoded_data['email']
            self.authenticated = True

            print(f"ID decodificado: {self.id_user}")
            print(f"role decodificado: {self.role_user}")
            print(f"nombre decodificado: {self.user_name}")
            print(f"correo decodificado: {self.user_email}")
            print(f"Autenticado: {self.authenticated}")

            return decoded_data
        
        except jwt.ExpiredSignatureError:
            print("El token ha expirado")

        except jwt.InvalidTokenError:
            print("Token inválido")
    ######FIN METODO PARA DECODIFICAR TOKEN JWT######        

    
    ######METODO INICIO DE SESION(LOGIN)######
    '''
    Este módulo es el manejador de evento de la ruta /login
    recibe las credenciales del manejador de eventos handle_login y las verifica en la base de datos
    si encuentra la cuenta y está verificada llama al método generate_token para crear un nuevo token jwt
    de inicio de sesión para el usuario
    '''
    def login(self, email: str, password: str):

        print("Inicia proceso de Login")        
        
        with rx.session() as session:
        # Busca el registro de inicio de sesión por correo electrónico
            login_record = session.exec(
              Login.select().where(Login.correo == email)
            ).first()

        if login_record and check_password_hash(login_record.password, password):
            if login_record.is_verified:
                if login_record.user_id:
                    # Manejar el inicio de sesión de Usuario
                    user = session.get(Usuario, login_record.user_id)
                    self.generate_token(login_record.id, user.nombre_usuario, login_record.correo, "usuario")
                    print(f"Nuevo Token generado para usuario: {self.token}")
                       
                elif login_record.worker_id:
                    # Manejar el inicio de sesión de Trabajador
                    worker = session.get(Trabajador, login_record.worker_id)
                    self.generate_token(login_record.id, worker.nombre_trabajador, login_record.correo, "trabajador")
                    print(f"Nuevo Token generado para trabajador: {self.token}")
                         
            else:
                print("Usuario o trabajador no verificado")
        else:
            print("Credenciales incorrectas")
           
    ######FIN METODO INICIO DE SESION(LOGIN)######        

    
    ######METODO CIERRE DE SESION(LOGOUT)######
    '''
    Este módulo cierra la sesión de usuario, limpiando todas las variables
    de estado de la sesión.
    '''
    def logout(self):
        print("Inicio proceso de logout")
        if self.token:           
            self.token = ""  # Limpiar el token de la variable de estado
            self.id_user = ""  # Limpiar el ID de usuario
            self.authenticated = False # Pasara autenticado a False          
       
        print("Logout realizado")
    ######FIN METODO CIERRE DE SESION(LOGOUT)######    
     

        
    ######METODO MANEJADOR DE VERIFICACION######
    '''
    Este módulo es el manejador de evento de la ruta /verify
    cuando el usuario recibe el correo con el token jwt, se invoca
    este método que revisa el token y marca el usuario o trabajador como activo: is_verified
    en la base de datos
    '''
    def handle_verificacion(self):

        print("Inicia proceso de verificación de token recibido en /verify")            
        
        #Obtiene el token de la URL /verify/[jwt_token]
        client_token = self.router.page.params.get("jwt_token", "")

        #Verifica si el token es una cadena, de lo contrario lo convierte
        if not isinstance(client_token, str):
            client_token = str(client_token)  # Convertir a cadena si no lo es

        #Proceso para leer el token en la variable client_token y decodificarlo
        try:
            payload = jwt.decode(client_token, self.SECRET_KEY, algorithms=["HS256"])
            
            print(f"payload: {payload}")
            user_id = payload['user_id']
            user_type = payload['user_type']

            with rx.session() as session:
                if user_type == 'usuario':
                    # Buscar el registro de Login usando user_id
                    query = select(Login).where(Login.user_id == user_id)
                    result = session.exec(query)
                    login_record = result.one_or_none()                   

                    print(login_record)

                    if login_record is not None:
                        # Marcar el correo como verificado
                        login_record.is_verified = True
                        session.add(login_record)
                        session.commit()
                        print("Correo de usuario verificado correctamente")
                    else:
                        print("Error: No se encontró el registro de inicio de sesión para el usuario.")

                elif user_type == 'trabajador':
                    # Buscar el registro de Login usando worker_id
                     query = select(Login).where(Login.worker_id == user_id)
                     result = session.exec(query)
                     login_record = result.one_or_none() 

                     if login_record is not None:
                        # Marcar el correo como verificado
                        login_record.is_verified = True
                        session.add(login_record)
                        session.commit()
                        print("Correo de trabajador verificado correctamente")
                     else:
                        print("Error: No se encontró el registro de inicio de sesión para el trabajador.")

                # Verificar si el usuario o trabajador está registrado como verificado
                verified_record = session.exec(
                    select(Login).where(Login.is_verified == True, Login.user_id == user_id if user_type == 'usuario' else Login.worker_id == user_id)
                ).one_or_none()

                if verified_record:
                    self.verified = True
                    print("Cuenta registrada correctamente")
                else:
                    self.verified = False
                    print("Error al registrar cuenta")

        except jwt.ExpiredSignatureError:
            print("El token ha expirado.")

        except jwt.InvalidTokenError:
            print("Token no válido.")
    ######FIN METODO VERIFICACION######  
     
          

    ######METODO CONTACTO######
    '''
    Este módulo es el manejador de evento del formulario /contacto
    toma todos los datos del formulario y los envia al método register_user 
    '''
    async def handle_contacto(self, form_data: dict):

        self.form_data = form_data
        self.did_submit = True

        # Crear un diccionario limpiando los valores vacíos o None
        data = {k: v for k, v in form_data.items() if v not in ("", None)}

        #Guarda todos los datos que vienen del formulario en la tabla 'Contacto' de la base de datos
        with rx.session() as session:
            db_entry = Contacto(
                **data
            )
        session.add(db_entry)
        session.commit() 

        yield # Liberar el control temporalmente
        await asyncio.sleep(2)
        self.did_submit = False
        yield # Finalizar el proceso
    ######FIN METODO CONTACTO######        
    


    ######METODO REGISTRO USUARIO######
    '''
    Este módulo es el manejador de evento del formulario /registro_usuario
    toma todos los datos del formulario y los envia al método register_user 
    '''
    async def handle_registro_usuario(self, form_data: dict):

        self.form_data = form_data
        self.did_submit = True
        
        # Crear un diccionario limpiando los valores vacíos o None
        data = {k: v for k, v in form_data.items() if v not in ("", None)}
        
        # Verifica que el campo `is_trabajador` sea un booleano
        data['is_trabajador'] = form_data.get('is_trabajador', 'false').lower() == 'true'
        
        # Llama a register_user con el diccionario completo
        self.register_user(data)
        
        yield # Liberar el control temporalmente
        await asyncio.sleep(2)
        self.did_submit = False
        yield  # Finalizar el proceso
    ######FIN METODO REGISTRO USUARIO######    

    
    ######METODO MANEJADRO EVENTO LOGIN######
    '''
    Este módulo es el manejador de evento del formulario /login
    toma el usuario y contraseña y los envia al método login_user 
    '''

    async def handle_login(self, form_data: dict):        
        
        self.form_data = form_data
        self.did_submit = True
        
        # Filtrar los datos del formulario para eliminar valores vacíos
        data = {k: v for k, v in form_data.items() if v not in ("", None)}

        #Variables para almacenar usuario y contraseña puestos en el formulario
        correo_usuario = data.get('correo_usuario')
        password_usuario = data.get('password_usuario')

        self.validar_credenciales(correo_usuario,password_usuario)
        

        if self.error_credenciales == True:
            print("Nombre de usuario o contraseña incorrectos")
        else:
            #correo_usuario and password_usuario:
            # Llamar al método para autenticar
            self.login(correo_usuario, password_usuario)
        
        yield  # Liberar el control temporalmente
        await asyncio.sleep(2)        
        self.did_submit = False
        yield  # Finalizar el proceso
    ######FIN METODO LOGIN######  


    ######CONSULTA PARA OBTENER TRABAJADORES POR ID######
    '''
    Este método busca en la base de datos el trabajador cuyo id
    sea el que se pasa como parámetro en la ruta /detalles
    '''
    def get_trabajador_by_id(self):
        with rx.session() as session:
            query = (
                select(Trabajador)
                .options(selectinload(Trabajador.login))
                .where(Trabajador.id == self.user_id)
            )            
            trabajador = session.exec(query).first()
            self.trabajadores = [trabajador] if trabajador else []
    ######FIN CONSULTA PARA OBTENER TRABAJADORES POR ID######    
                                  
      
    ######CONSULTA PARA OBTENER TRABAJADORES POR CATEGORIA######
    '''
    Este método busca en la base de datos los trabajadores
    de la categoría que se pase como parámetro, se usa principamente
    para cargar los datos de las secciones de la parte lateral del sitio (sidebar)
    '''
    def get_trabajadores_by_categoria(self, categoria: str):
        with rx.session() as session:
            query = session.exec(
            Trabajador.select().where(
                Trabajador.categoria == categoria
            )
            ).all()
            self.trabajadores = query      
    ######FIN CONSULTAS PARA OBTENER TRABAJADORES POR CATEGORÍAS######

    ######METODO PARA REGISTRO DE USUARIOS###############

    def register_user(self, form_data: dict):

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
                session.add(new_login)
                session.commit()

                # Obtener el ID del trabajador para el token
                user_id = new_worker.id
                user_type = 'trabajador'
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

                # Obtener el ID del usuario para el token
                user_id = new_user.id
                user_type = 'usuario'           

            # Generar un token de verificación
            token = jwt.encode({
                'user_id': user_id,
                'user_type': user_type,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24),
            }, self.SECRET_KEY, algorithm="HS256")
            
            # Enviar el correo de verificación
            self.send_verification_email(correo_usuario, token)  


    def send_verification_email(self, email, token):
        verification_link = f"http://localhost:3000/verify/{token}"
        msg = EmailMessage()
        msg.set_content(f"Haga clic para verificar su cuenta: {verification_link}")
        msg['Subject'] = "[alavueltadeunclic - Verificación de cuenta]"
        msg['From'] = "santurron2004@gmail.com"
        msg['To'] = email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("santurron2004@gmail.com", self.GMAIL_KEY)
            server.send_message(msg)


    
    def validacion_usuario(self, usuario: str):

        verificacion = not (re.match(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$", usuario))
        self.usuario_invalido = verificacion

    def validacion_password(self, password: str):

        verificacion = not password.strip()
        self.password_vacio = verificacion 


    def validar_credenciales(self, email: str, password: str):

        print("Inicia proceso de validación de credenciales")        
        
        with rx.session() as session:
        # Busca el registro de inicio de sesión por correo electrónico
            login_record = session.exec(
              Login.select().where(Login.correo == email)
            ).first()

        if login_record and check_password_hash(login_record.password, password) == False:
        #if check_password_hash(login_record.password, password) == False:
            if login_record.is_verified:
               self.error_credenciales = True
               self.mensaje_error_contraseña = "Contraseña incorrecta"                                   
       
        elif  login_record and check_password_hash(login_record.password, password):
               self.mensaje_error_contraseña = "Contraseña correcta" 
               self.error_credenciales = False
        else:
               self.mensaje_error_contraseña = "Usuario no registrado"              

        # if check_password_hash(login_record.password, password) == False: 
        #     self.error_credenciales = True
        #     self.mensaje_error_contraseña = "Contraseña incorrecta"
    
    def ocultar_mensaje_error(self):
        time.sleep(3)
        self.mensaje_error_contraseña = ""
        # Asegúrate de notificar al sistema de la actualización del estado
        threading.Thread(target=self.ocultar_mensaje_error).start()
        