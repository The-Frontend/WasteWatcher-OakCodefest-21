from typing import List
from models.dish import DishIn, DishOut
from sqlalchemy.schema import CreateTable
from .db_utilities import build_query
from .schemas import dishes

from .db_connector import db

async def create_dishes_table() -> None:
    sql_statement = str(CreateTable(dishes))
    await db.execute(sql_statement)

async def insert_one_dish(dish: DishIn) -> int:
    query = dishes.insert()
    last_record_id = await db.execute(query=query, values=dish.dict())
    return int(last_record_id)

async def get_dishes_by_user_id(user_id: int) -> List[DishOut]:
    query, values = build_query(dishes, filters={
        "equalTo": {
            "user_id": int(user_id),
        }
    })

    mapped_dishes: List[DishOut] = []

    async for row in db.iterate(query=query, values=values):
        mapped_copypasta = DishOut(
            id=int(row[0]),
            device_id=int(row[1]),
            name=str(row[2]),
            ingredients=str(row[3]).split(';'),
            quantity=float(row[4])
        )
        mapped_dishes.append(mapped_copypasta)
    return mapped_dishes