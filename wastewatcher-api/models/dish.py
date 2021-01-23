from typing import List
from pydantic import BaseModel

class DishIn(BaseModel):
    user_id: int
    device_id: int
    dish_name: str
    ingredients: List[str]
    quantity: float
    created_timestamp: str

class DishOut(BaseModel):
    id: int
    user_id: int
    device_id: int
    dish_name: str
    ingredients: List[str]
    quantity: float
    created_timestamp: str

class DishRequestBody(BaseModel):
    device_id: int
    dish_name: str
    ingredients: List[str]
    quantity: float
