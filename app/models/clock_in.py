from pydantic import BaseModel
from typing import Optional

class ClockIn(BaseModel):
    email: str
    location: str

class ClockInUpdate(BaseModel):
    email: Optional[str]
    location: Optional[str]
