import reflex as rx
import asyncio
from ..backend.models import Customer

class State(rx.State):

    first_name: str
    last_name: str
    

class FormState(rx.State):
    form_data: dict = {}
    did_submit: bool = False

    async def handle_submit(self, form_data: dict):
        self.form_data = form_data
        self.did_submit = True
        data = {}
        for k,v in form_data.items():
            if v == "" or v is None:
                continue
            data[k] = v
        with rx.session() as session:
            db_entry = Customer(
                **data
            )
        session.add(db_entry)
        session.commit()        
        yield
        await asyncio.sleep(2)
        self.did_submit = False
        yield