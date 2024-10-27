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