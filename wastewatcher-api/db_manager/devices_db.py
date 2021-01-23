from typing import Union
from models.device import DeviceIn, DeviceOut
from sqlalchemy.schema import CreateTable
from .schemas import devices

from .db_connector import db

async def create_devices_table() -> None:
    sql_statement = str(CreateTable(devices))
    await db.execute(sql_statement)

async def insert_one_device(device: DeviceIn) -> int:
    query = devices.insert()
    last_record_id = await db.execute(query=query, values=device.dict())
    return int(last_record_id)

async def get_device_by_id(device_id: int) -> Union[DeviceOut, None]:
  query = str(devices.select().where(devices.c.id == 'id_1'))
  values = {
      'id_1': device_id
  }
  row = await db.fetch_one(query=str(query), values=values)
  if row == None:
      return None
  device_out = DeviceOut(
      id=int(row[0]),
      user_id=int(row[1])
  )
  return device_out
  
