from pydantic import BaseModel
from typing import Optional
class UserCreate(BaseModel):
    name: str
    role: str

class RoleCreate(BaseModel):
    name: str

class UserRead(BaseModel):
    id: int
    name: str
    role_id: int

class RoleRead(BaseModel):
    id: int
    name: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None