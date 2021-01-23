from models.user import UserIn, UserOut
from sqlalchemy.schema import CreateTable
from .schemas import users

from .db_connector import db

async def create_users_table() -> None:
    sql_statement = str(CreateTable(users))
    await db.execute(sql_statement)

async def insert_one_user(user: UserIn) -> int:
    query = users.insert()
    last_record_id = await db.execute(query=query, values=user.dict())
    return int(last_record_id)

async def get_user_by_id(user_id: int) -> UserOut:
  query = str(users.select().where(users.c.id == 'id_1'))
  values = {
      'id_1': user_id
  }
  row = await db.fetch_one(query=str(query), values=values)
  user_out = UserOut(
      id=int(row[0]),
      name=str(row[1])
  )
  return user_out

