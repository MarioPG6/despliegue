import reflex as rx

class Customer(rx.Model, table=True):
    """The customer model."""
    first_name: str | None = None
    last_name: str | None = None