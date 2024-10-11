from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: str

class ItemUpdate(BaseModel):
    name: Optional[str]
    item_name: Optional[str]
    quantity: Optional[int]
    expiry_date: Optional[str]
