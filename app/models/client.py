from datetime import date

from pydantic import BaseModel


class ClientIn(BaseModel):
    name: str
    panel_name: str
    active: bool
    effective_start_at: date
    effective_end_at: date


class Client(ClientIn):
    id: int
