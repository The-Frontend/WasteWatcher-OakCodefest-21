from pydantic import BaseModel

class UserIn(BaseModel):
    name: str

class UserOut(BaseModel):
    id: int
    name: str
    mass_wasted: int
