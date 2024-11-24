import reflex as rx
import asyncio
import jwt
import re
import smtplib
import datetime
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone, timedelta
from email.message import EmailMessage
from sqlmodel import select
from sqlalchemy.orm import selectinload
from collections import Counter




from .models import Trabajador
from .models import Usuario
from .models import Login
from .models import Contacto
from .models import Comentario
from .models import Servicio
from .models import Calificacion

    

class State(rx.State): 
    trabajadores: list[Trabajador]  = [] 
    usuarios: list[Usuario]  = [] 
    comentarios: list[Comentario] = []
    servicios: list[Servicio]  = [] 
    form_data: dict = {}    
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
    login_id: str
    user_entered_username: str
    user_entered_email: str
    user_entered_password: str
    user_entered_password2: str
    user_entered_telefono: str
    user_entered_direccion: str
    user_entered_descripcion: str
    user_entered_localidad = ""
    user_entered_categoria = ""
    texto_comentario = ""    
    comentarios_cargados: bool = False
    nombre_usuario = ""
    telefono_usuario = ""
    direccion_usuario = ""
    loged_in: bool = False
    loader: bool = False
    registro: bool = False
    mensaje_registro: str
    estado_servicio: str
    estado_count: int
    data_for_chart: list = []
   
  

   

    SECRET_KEY = "e85a85be384f74c22bbe0b93ba3404fe3ad75e2346c061c38ba4f77ea6971d35"
    GMAIL_KEY = "ycrp jrgi ekuw gpdo"

    
            
    def select_localidad(self, value):
        self.user_entered_localidad = value

    @rx.var
    def is_localidad_empty(self) -> bool:
        return self.user_entered_localidad == ""

    def select_categoria(self, value):
        self.user_entered_categoria = value

    @rx.var
    def is_categoria_empty(self) -> bool:
        return self.user_entered_categoria == ""      
   

    #Variable para obtener id de usuario de la url /detalles
    @rx.var
    def user_id(self):
        return self.router.page.params.get("id", "")
        
    #Variable para obtener el token de la url /verify
    @rx.var
    def get_token(self):
        return self.router.page.params.get("jwt_token", "") 
    

    @rx.var
    def invalid_email(self) -> bool:        
           
        return not re.match(
            r"[^@]+@[^@]+\.[^@]+", self.user_entered_email
        )
         
     
    @rx.var
    def password_empty(self) -> bool:
        return not self.user_entered_password.strip()
    
    @rx.var
    def password2_empty(self) -> bool:
        return not self.user_entered_password2.strip()
    
    @rx.var
    def email_empty(self) -> bool:
        return not self.user_entered_email.strip()
    
    @rx.var
    def username_empty(self) -> bool:
        return not self.user_entered_username.strip()
    
    @rx.var
    def username_telefono(self) -> bool:
        return not self.user_entered_telefono.strip()
    
    @rx.var
    def username_direccion(self) -> bool:
        return not self.user_entered_direccion.strip()
    
    @rx.var
    def username_descripcion(self) -> bool:
        return not self.user_entered_descripcion.strip()
    
    
    @rx.var
    def password_verify(self) -> bool:        
        return self.user_entered_password != self.user_entered_password2
    
    @rx.var
    def input_invalid(self) -> bool:
        return (
            self.invalid_email
            or self.email_empty
            or self.password_empty
           
        )
    
    @rx.var
    def input_invalid_usuarios(self) -> bool:
        return (
            self.invalid_email
            or self.email_empty
            or self.password_empty
            or self.password2_empty
            or self.password_verify
            or self.email_exists
            or self.username_empty
            or self.is_localidad_empty
        )
    
    @rx.var
    def input_invalid_trabajadores(self) -> bool:
        return (
            self.invalid_email
            or self.email_empty
            or self.password_empty
            or self.password2_empty
            or self.password_verify
            or self.email_exists
            or self.username_empty
            or self.username_telefono
            or self.username_direccion
            or self.username_descripcion
            or self.is_localidad_empty
            or self.is_categoria_empty
        )
    
    @rx.var
    def email_exists(self) -> bool:
        
        if self.user_entered_email:
            with rx.session() as session:
                query = Login.select().where(Login.correo == self.user_entered_email)
                return session.exec(query).first() is not None                
        return False


    def loader_status(self):
        self.loader = True 

    ######METODO PARA GENERAR TOKEN JWT######
    '''
    Este método recibe como parámetro los valores que se deben poner en el token
    luego genera el token y lo almacena en la variable de estado 'token' y llama
    al final llama método decode_token para inciar la decodificación del mismo.
    '''
    def generate_token(self, user_id, name, email, role, login_id):

        print("Inicia proceso generación de token")

        user_id = str(user_id)
        user_name = str(name)
        email = str(email)
        role = str(role)
        login_id = str(login_id)

        token = jwt.encode({
            'user_id': user_id,
            'email': email,
            'role': role,
            'nombre': user_name,
            'login_id': login_id,
            'exp': datetime.now(timezone.utc) + timedelta(hours=24),
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
            self.login_id = decoded_data['login_id']
            self.authenticated = True

            print(f"ID decodificado: {self.id_user}")
            print(f"role decodificado: {self.role_user}")
            print(f"nombre decodificado: {self.user_name}")
            print(f"correo decodificado: {self.user_email}")
            print(f"login id: {self.login_id}")
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
                    self.generate_token(login_record.id, user.nombre_usuario, login_record.correo, "usuario", login_record.user_id)
                    self.telefono_usuario = user.telefono_usuario
                    self.direccion_usuario = user.direccion_usuario
                    print(f"Nuevo Token generado para usuario: {self.token}")
                    
                       
                elif login_record.worker_id:
                    # Manejar el inicio de sesión de Trabajador                    
                    worker = session.get(Trabajador, login_record.worker_id)                   
                    self.generate_token(login_record.id, worker.nombre_trabajador, login_record.correo, "trabajador", login_record.worker_id)
                    print(f"Nuevo Token generado para trabajador: {self.token}")
                    
                self.loged_in = True         
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
            self.user_name = "" # Limpiar el usuario
            self.authenticated = False # Pasara autenticado a False  
            self.loader = False # Pasar loader a False
            self.mensaje_error_contraseña = ""
            self.mensaje_registro = ""
            self.login_id = ""
            self.servicios = [] 
                 
       
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

        # Crear un diccionario limpiando los valores vacíos o None
        data = {k: v for k, v in form_data.items() if v not in ("", None)}

        #Guarda todos los datos que vienen del formulario en la tabla 'Contacto' de la base de datos
        with rx.session() as session:
            db_entry = Contacto(
                **data
            )
        session.add(db_entry)
        session.commit()
        yield rx.toast.success("Gracias por enviar sus comentarios!") 
    ######FIN METODO CONTACTO######        
    


    ######METODO REGISTRO USUARIO######
    '''
    Este módulo es el manejador de evento del formulario /registro_usuario
    toma todos los datos del formulario y los envia al método register_user 
    '''
    async def handle_registro_usuario(self, form_data: dict):

        self.form_data = form_data
        
        # Crear un diccionario limpiando los valores vacíos o None
        data = {k: v for k, v in form_data.items() if v not in ("", None)}
        
        # Verifica que el campo `is_trabajador` sea un booleano
        data['is_trabajador'] = form_data.get('is_trabajador', 'false').lower() == 'true'
        
        # Llama a register_user con el diccionario completo
        self.register_user(data)        
    ######FIN METODO REGISTRO USUARIO######    

    
    ######METODO MANEJADRO EVENTO LOGIN######
    '''
    Este módulo es el manejador de evento del formulario /login
    toma el usuario y contraseña y los envia al método login_user 
    '''   
    async def handle_login(self, form_data: dict):        
        
        self.form_data = form_data         
        
                
        #self.did_submit = True
        
        # Filtrar los datos del formulario para eliminar valores vacíos
        data = {k: v for k, v in form_data.items() if v not in ("", None)}

        #Variables para almacenar usuario y contraseña puestos en el formulario
        correo_usuario = data.get('correo_usuario')
        password_usuario = data.get('password_usuario')

        #self.validar_credenciales(correo_usuario,password_usuario)

        print("Inicia proceso de validación de credenciales")        
        
        with rx.session() as session:
        # Busca el registro de inicio de sesión por correo electrónico
            login_record = session.exec(
              Login.select().where(Login.correo == correo_usuario)
            ).first()
        print(login_record)    

        with rx.session() as session:
            query = (
                select(Trabajador)
                .join(Login, Trabajador.id == Login.worker_id)
                .options(selectinload(Trabajador.login))
                .where(Login.correo == correo_usuario) 
            )   
            trabajador = session.exec(query).first()
            print(trabajador)

        with rx.session() as session:
            query = (
                select(Usuario)
                .join(Login, Usuario.id == Login.user_id)
                .options(selectinload(Usuario.login))
                .where(Login.correo == correo_usuario) 
            )   
            usuario = session.exec(query).first()
            print(usuario)    
         

        
        if login_record is not None:
            
            print("Registro encontrado.")
            if check_password_hash(login_record.password, password_usuario):
                print("Contraseña correcta.")
                if login_record.is_verified and login_record.role == "usuario":
                    print("Cuenta verificada.")
                    self.login(correo_usuario, password_usuario)
                    self.error_credenciales = False
                    return rx.redirect('/')
                elif login_record.is_verified and login_record.role == "trabajador":
                    if trabajador.is_verified == 1:
                        print("Cuenta verificada y validada para trabajador.")
                        self.login(correo_usuario, password_usuario)
                        self.error_credenciales = False
                        return rx.redirect('/')
                    else:
                        print("Cuenta verificada pero aún se encuentra en proceso de validación.")
                        self.error_credenciales = True
                        self.mensaje_error_contraseña = "Cuenta verificada pero aún se encuentra en proceso de validación"                                   
                else:
                    print("Cuenta no verificada.")
                    self.error_credenciales = True
                    self.mensaje_error_contraseña = "Cuenta no verificada"
                                        
            else:
                print("Contraseña incorrecta.")
                self.error_credenciales = True
                self.mensaje_error_contraseña = "Contraseña incorrecta"               
                
        else:
            print("Usuario no registrado.")
            self.error_credenciales = True
            self.mensaje_error_contraseña = "Usuario no registrado"         
     
        self.loader = False      
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
            
        with rx.session() as session:
           query = select(Comentario).where(Comentario.trabajador_id == self.user_id).order_by(Comentario.fecha_creacion.desc())
           self.comentarios = session.exec(query).all()
           self.comentarios_cargados = True         
    ######FIN CONSULTA PARA OBTENER TRABAJADORES POR ID###### 



    ######CONSULTA PARA OBTENER USUARIOS POR ID######
    '''
    Este método busca en la base de datos el usuario cuyo id
    sea el que se pasa como parámetro en la ruta del perfil
    '''
    def get_usuario_by_id(self):
        with rx.session() as session:
            query = (
                select(Usuario)
                .join(Login, Usuario.id == Login.user_id)
                .options(selectinload(Usuario.login))  
            )
            query = query.where(Login.correo == self.user_email)
            self.usuarios = session.exec(query).all() or []    
    ######FIN CONSULTA PARA OBTENER USUARIOS POR ID######    
       
                                  
      
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
                Trabajador.categoria == categoria, Trabajador.is_verified == 1
            )
            ).all()
            self.trabajadores = query                 
    ######FIN CONSULTAS PARA OBTENER TRABAJADORES POR CATEGORÍAS######


     ######CONSULTA PARA OBTENER TODOS LOS TRABAJADORES######
    '''
    Este método busca en la base de datos todos los trabajadores    
    '''
    def get_all_trabajadores(self):
        with rx.session() as session:
            query = session.exec(
            Trabajador.select()
            ).all()

            self.trabajadores = query                 
    ######FIN CONSULTAS PARA OBTENER TRABAJADORES POR CATEGORÍAS######



    ######METODO PARA REGISTRO DE USUARIOS###############
    '''
    Este método sirve para registrar los usuarios nuevos en la base de datos
    genera el token jwt e invoca el método para enviar el link de validación
    '''
    def register_user(self, form_data: dict):

        nombre_usuario = form_data.get('nombre_usuario')
        correo_usuario = form_data.get('correo_usuario')
        password_usuario = form_data.get('password_usuario')
        localidad_usuario = form_data.get('localidad_usuario')   
        is_trabajador = form_data.get('is_trabajador', False)
        nombre_trabajador = form_data.get('nombre_trabajador')
        localidad_trabajador = form_data.get('localidad_trabajador')
        telefono_trabajador = form_data.get('telefono_trabajador')
        telefono_usuario = form_data.get('telefono_usuario')
        categoria = form_data.get('categoria')
        direccion = form_data.get('direccion')
        direccion_usuario = form_data.get('direccion_usuario')
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
                self.registro = True
                self.mensaje_registro = f"Registro trabajador correcto, por favor verifique su registro en el enlace que le enviamos a: {correo_usuario}"
            else:
                # Crear un nuevo objeto Usuario
                new_user = Usuario(nombre_usuario=nombre_usuario, localidad_usuario=localidad_usuario,telefono_usuario=telefono_usuario,direccion_usuario=direccion_usuario)
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
                self.registro = True
                self.mensaje_registro = f"Registro usuario correcto, por favor verifique su registro en el enlace que le enviamos a: {correo_usuario}"
          

            # Generar un token de verificación
            token = jwt.encode({
                'user_id': user_id,
                'user_type': user_type,
                'exp':  datetime.now(timezone.utc) + timedelta(hours=24),
            }, self.SECRET_KEY, algorithm="HS256")
            
            # Enviar el correo de verificación
            self.send_verification_email(correo_usuario, token)
            self.loader = False
    ######FIN METODO PARA REGISTRO DE USUARIOS###############          


    ######METODO PARA ENVIO DE EMAIL DE REGISTRO###############
    '''
    Este método sirve para enviar correo al usuario el link de verificación
    '''
    def send_verification_email(self, email, token):
        verification_link = f"http://alavueltadeunclick.com:3000/verify/{token}"
        msg = EmailMessage()
        msg.set_content(f"Haga clic para verificar su cuenta: {verification_link}")
        msg['Subject'] = "[alavueltadeunclic - Verificación de cuenta]"
        msg['From'] = "santurron2004@gmail.com"
        msg['To'] = email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("santurron2004@gmail.com", self.GMAIL_KEY)
            server.send_message(msg)
    ######FIN METODO PARA ENVIO DE EMAIL DE REGISTRO###############

   
    ######METODO PARA MANEJO DE COMENTARIOS###############
    '''
    Este método sirve para guardar los comentarios sobre los trabajadores
    '''     
    async def handle_comentario(self):       

        with rx.session() as session:
            nuevo_comentario = Comentario(
                nombre_usuario=self.user_name,
                texto_comentario=self.texto_comentario,
                trabajador_id=self.user_id,
                fecha_creacion = datetime.now(timezone.utc) - timedelta(hours=5)
            )            
            session.add(nuevo_comentario)
            session.commit()
            yield rx.toast.success("Comentario enviado!")
            self.get_trabajador_by_id()
        
        # Reiniciar los campos del formulario
        self.nombre_usuario = ""
        self.texto_comentario = ""
    ######FIN METODO PARA MANEJO DE COMENTARIOS###############    

    
    
    ######METODO PARA ACTUALIZAR PERFIL TRABAJADOR###############
    '''
    Este método sirve para actualizar el perfil del trabajador
    '''   
    async def actualizar_perfil_trabajador(self):       

        with rx.session() as session:
            trabajador = session.exec(select(Trabajador).where(Trabajador.id == self.user_id)).first()
            if trabajador:
                if self.user_entered_telefono: trabajador.telefono_trabajador = self.user_entered_telefono
                if self.user_entered_direccion: trabajador.direccion = self.user_entered_direccion
                if self.user_entered_localidad: trabajador.localidad_trabajador = self.user_entered_localidad
                if self.user_entered_descripcion: trabajador.descripcion = self.user_entered_descripcion                
                print(trabajador)                
                session.commit()
                yield rx.toast.success("Perfil actualizado con éxito!")
                self.get_trabajador_by_id()
    ######FIN METODO PARA ACTUALIZAR PERFIL TRABAJADOR###############            

    
    
    ######METODO PARA ACTUALIZAR PERFIL USUARIOS###############
    '''
    Este método sirve para actualizar el perfil del usuario
    '''  
    async def actualizar_perfil_usuario(self):       

        with rx.session() as session:
            usuario = session.exec(select(Usuario).where(Usuario.id == self.user_id)).first()

            if usuario:               
                if self.user_entered_localidad: usuario.localidad_usuario = self.user_entered_localidad
                if self.user_entered_telefono: usuario.telefono_usuario = self.user_entered_telefono
                if self.user_entered_direccion: usuario.direccion_usuario = self.user_entered_direccion
                print(usuario)                
                session.commit()
                yield rx.toast.success("Perfil actualizado con éxito!")
                self.get_usuario_by_id()
    ######FIN METODO PARA ACTUALIZAR PERFIL USUARIOS###############            


    ######METODO PARA CONTACTAR AL TRABAJADOR###############
    '''
    Este método sirve para contactar al trabajador
    '''               
    
    def contactar_trabajador(self, email, trabajador, usuario, telefono, direccion, usuario_id, trabajador_id ):
        
        nuevo_servicio = Servicio(usuario_id=usuario_id, trabajador_id=trabajador_id)
        self.estado_servicio = "abierto"
        with rx.session() as session:
            session.add(nuevo_servicio)
            session.commit()

        msg = EmailMessage()
        msg.set_content(f"""Hola {trabajador}
                         El usuario {usuario} está interesado en contratar tus servicios.
                         A continuación, te dejemos los datos para que puedas establecer contacto
                         recuerda iniciar el servicio desde tu perfil una vez te encuentres en el
                         domicilio del usuario.
                         Usuario: {usuario}
                         Teléfono: {telefono}
                         Dirección: {direccion}

                         Att. El equipo de A la vuleta de un Click
                                                
                        """
                        )
        msg['Subject'] = "[alavueltadeunclick] - Un usuario está interesado en tus servicios!"
        msg['From'] = "santurron2004@gmail.com"
        msg['To'] = email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("santurron2004@gmail.com", self.GMAIL_KEY)
            server.send_message(msg)
            yield rx.toast.success(f"Se enviaron sus datos de contacto a {trabajador}, se pondrá en contacto con usted en breve.")
    ######FIN METODO PARA CONTACTAR AL TRABAJADOR###############        

    
    
    ######METODO PARA CREAR LISTA DE ESTADOS###############
    '''
    Este método sirve para alimentar la gráfica del módulo de gerencia con
    los estados y la cantidad de los mismos
    '''  
    def get_estado_servicios(self):
        
         self.get_servicios()
         with rx.session() as session:
            resultados = session.exec(select(Servicio)).all()
            estados = [servicio.estado for servicio in resultados]
            estado_count = dict(Counter(estados))

            self.data_for_chart = [{'estado': estado, 'cantidad': cantidad} for estado, cantidad in estado_count.items()]
            
    ######METODO PARA CREAR LISTA DE ESTADOS###############          

       
    ######METODO PARA TRAER DATOS DE USUARIOS/TRABAJADORES/SERVICIOS###############
    '''
    Este método sirve para alimentar la tabla del módulo de gerencia con
    los trabajadores, usuarios y estados.
    '''  
    def get_servicios(self):

        with rx.session() as session:
            
            statement = (
                select(Servicio)                
                .options(
                 selectinload(Servicio.trabajador),
                 selectinload(Servicio.usuario)
                )        
            )
            
            self.servicios = session.exec(statement).all()                       
         

            if not self.servicios:
                print("No se encontraron servicios")
                self.servicios = []  
            else:
                print(f"Se encontraron {len(self.servicios)} servicios")

            self.estado_count = len(self.servicios)
    ######FIN METODO PARA TRAER DATOS DE USUARIOS/TRABAJADORES/SERVICIOS###############        



    ######METODO PARA CARGAR SERVICIOS POR USUARIO###############
    '''
    Este método sirve para generar la lista de servicios por cada usuario
    '''  
    def get_servicios_by_user(self):
        print("entró a obtener servicios por usuario")
        with rx.session() as session:
            statement = (
                select(Servicio)
                .where(Servicio.usuario_id == self.login_id).order_by(Servicio.fecha_creacion.desc())
                .options(selectinload(Servicio.trabajador))  # Asegura que la relación se cargue
            )
                        
            self.servicios = session.exec(statement).all()

            if not self.servicios:
                print("No se encontraron servicios para el usuario con ID:", self.login_id)
                self.servicios = []  
            else:
                print(f"Se encontraron {len(self.servicios)} servicios para el usuario con ID: {self.login_id}")
     ######FIN METODO PARA CARGAR SERVICIOS POR USUARIO###############       
   


    ######METODO PARA CARGAR SERVICIOS POR TRABAJADOR###############
    '''
    Este método sirve para generar la lista de servicios por cada usuario
    '''  
    def get_servicios_by_trabajador(self):
        print("entró a obtener servicios por trabajador")
        with rx.session() as session:
            statement = (
                select(Servicio)
                .where(Servicio.trabajador_id == self.login_id).order_by(Servicio.fecha_creacion.desc())
                .options(selectinload(Servicio.usuario))  # Asegura que la relación se cargue
            )
            
            self.servicios = session.exec(statement).all()

            if not self.servicios:
                print("No se encontraron servicios para el trabajador con ID:", self.login_id)
                self.servicios = []  
            else:   
                print(f"Se encontraron {len(self.servicios)} servicios para el trabajador con ID: {self.login_id}")
    ######METODO PARA CARGAR SERVICIOS POR TRABAJADOR###############      
    
    
    ######METODO PARA CERRAR SERVICIOS###############
    '''
    Este método sirve para cerrar un servicio
    '''  
    def cerrar_servicio(self, id: int):       
       
        with rx.session() as session:
            servicio = session.get(Servicio, id)
            if servicio:
                servicio.estado = "cerrado"
                servicio.fecha_cierre = datetime.now(timezone.utc) - timedelta(hours=5)
                session.commit()
                yield rx.toast.success(f"Se ha cerrado el servicio correctamente")
        
                self.get_servicios_by_trabajador()
                self.get_servicios_by_user()
    ######FIN METODO PARA CERRAR SERVICIOS###############   
             

    ######METODO PARA CANCELAR SERVICIOS###############
    '''
    Este método sirve para cancelar un servicio
    '''  
    def cancelar_servicio(self, id: int):       
       
        with rx.session() as session:
            servicio = session.get(Servicio, id)
            if servicio:
                servicio.estado = "cancelado"
                servicio.fecha_cierre = datetime.now(timezone.utc) - timedelta(hours=5)
                session.commit()
                yield rx.toast.success(f"Se ha cancelado el servicio correctamente")

                self.get_servicios_by_trabajador()
                self.get_servicios_by_user()
    ######FIN METODO PARA CANCELAR SERVICIOS###############
            

    ######METODO PARA INICIAR SERVICIOS###############
    '''
    Este método sirve para cancelar un servicio
    '''  
    def iniciar_servicio(self, id: int):       
       
        with rx.session() as session:
            servicio = session.get(Servicio, id)
            if servicio:
                servicio.estado = "iniciado"
                servicio.fecha_inicio = datetime.now(timezone.utc) - timedelta(hours=5)
                session.commit()
                yield rx.toast.success(f"Se ha iniciado el servicio correctamente")
                
                self.get_servicios_by_trabajador()
    ######FIN METODO PARA INICIAR SERVICIOS###############            

    
    ######METODO PARA CALIFICAR SERVICIOS BIEN###############
    '''
    Este método sirve para calificar un servicio bien
    '''  
    def calificar_servicio_up(self):

        with rx.session() as session:
            trabajador = session.get(Trabajador, self.user_id)
            if trabajador:
                calificacion_existente = session.exec(
                select(Calificacion).where(
                    Calificacion.usuario_id == self.login_id,  
                    Calificacion.trabajador_id == self.user_id
                )
                ).first()
                
                if calificacion_existente:
                    yield rx.toast.warning("Ya has calificado a este trabajador.")
                else:
                    trabajador.thumbs_up = trabajador.thumbs_up + 1
                    session.add(Calificacion(usuario_id=self.login_id, trabajador_id=self.user_id))                
                    session.commit()
                    yield rx.toast.success(f"Gracias por su calificación")
                    self.get_trabajador_by_id()
    ######FIN METODO PARA CALIFICAR SERVICIOS###############        

    
    ######METODO PARA CALIFICAR SERVICIOS MAL###############
    '''
    Este método sirve para calificar un servicio mal
    '''  
    def calificar_servicio_down(self):        
                
         with rx.session() as session:
            trabajador = session.get(Trabajador, self.user_id)
            if trabajador:
                calificacion_existente = session.exec(
                select(Calificacion).where(
                    Calificacion.usuario_id == self.login_id,  
                    Calificacion.trabajador_id == self.user_id
                )
                ).first()
                
                if calificacion_existente:
                    yield rx.toast.warning("Ya has calificado a este trabajador.")
                else:
                    trabajador.thumbs_down = trabajador.thumbs_down + 1
                    session.add(Calificacion(usuario_id=self.login_id, trabajador_id=self.user_id))                
                    session.commit()
                    yield rx.toast.success(f"Gracias por su calificación")
                    self.get_trabajador_by_id()
    ######FIN METODO PARA CALIFICAR SERVICIOS MAL###############               
                      
                                               