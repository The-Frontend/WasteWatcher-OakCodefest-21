from typing import List
from pydantic import BaseModel

class DishIn(BaseModel):
    user_id: int
    device_id: int
    dish_name: str
    ingredients: List[str]
    quantity: float

class DishOut(BaseModel):
    id: int
    user_id: int
    device_id: int
    dish_name: str
    ingredients: List[str]
    quantity: float

class DishRequestBody(BaseModel):
    device_id: int
    dish_name: str
    ingredients: List[str]
    quantity: float
