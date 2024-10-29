import reflex as rx
import asyncio
from .models import Contacto

from .models import Trabajador

    

class State(rx.State): 
    users: list['Trabajador']  = []  
    form_data: dict = {}
    did_submit: bool = False

    @rx.var
    def user_id(self):
        print(self.router.page.params)
        return self.router.page.params.get("id", "")

    async def handle_contacto(self, form_data: dict):
        self.form_data = form_data
        self.did_submit = True
        data = {}
        for k,v in form_data.items():
            if v == "" or v is None:
                continue
            data[k] = v
        with rx.session() as session:
            db_entry = Contacto(
                **data
            )
        session.add(db_entry)
        session.commit()        
        yield
        await asyncio.sleep(2)
        self.did_submit = False
        yield

    async def handle_registro(self, form_data: dict):
        self.form_data = form_data
        self.did_submit = True
        data = {} 
        for k,v in form_data.items():
            if v == "" or v is None:
                continue
            data[k] = v       
        with rx.session() as session:
            db_entry = Trabajador(
                **data
            )
        session.add(db_entry)
        session.commit()        
        yield
        await asyncio.sleep(2)
        self.did_submit = False
        yield    
    
    def get_users_reparaciones(self):
        with rx.session() as session:
            users = session.exec(
                Trabajador.select().where(
                   Trabajador.categoria == "Reparaciones" 
                )
            ).all()
            self.users = users

    def get_user_by_id(self):
        with rx.session() as session:
            users = session.exec(
                Trabajador.select().where(
                   Trabajador.id == self.user_id
                )
            ).all()
            self.users = users
            
    def get_users_cerrajeria(self):
        with rx.session() as session:
            users = session.exec(
                Trabajador.select().where(
                    Trabajador.categoria == "Cerrajería"
                )
            ).all()
            self.users = users

    def get_users_instalaciones(self):
        with rx.session() as session:
            users = session.exec(
                Trabajador.select().where(
                    Trabajador.categoria == "Instalaciones"
                )
            ).all()
            self.users = users

    def get_users_pintura(self):
        with rx.session() as session:
            users = session.exec(
                Trabajador.select().where(
                    Trabajador.categoria == "Pintura"
                )
            ).all()
            self.users = users

    def get_users_obras(self):
        with rx.session() as session:
            users = session.exec(
                Trabajador.select().where(
                    Trabajador.categoria == "Obras"
                )
            ).all()
            self.users = users

    def get_users_belleza_peluqueria(self):
        with rx.session() as session:
            users = session.exec(
                Trabajador.select().where(
                    Trabajador.categoria == "Belleza y Peluquería"
                )
            ).all()
            self.users = users

    def get_users_clases(self):
        with rx.session() as session:
            users = session.exec(
                Trabajador.select().where(
                    Trabajador.categoria == "Clases"
                )
            ).all()
            self.users = users

    def get_users_electricistas(self):
        with rx.session() as session:
            users = session.exec(
                Trabajador.select().where(
                    Trabajador.categoria == "Electricistas"
                )
            ).all()
            self.users = users

    def get_users_aseo(self):
        with rx.session() as session:
            users = session.exec(
                Trabajador.select().where(
                    Trabajador.categoria == "Aseo"
                )
            ).all()
            self.users = users

    def get_users_plomeria(self):
        with rx.session() as session:
            users = session.exec(
                Trabajador.select().where(
                    Trabajador.categoria == "Plomería"
                )
            ).all()
            self.users = users                