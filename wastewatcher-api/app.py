from dotenv import load_dotenv
DEBUG = True
if DEBUG:
    load_dotenv()

from starlette.responses import JSONResponse
from db_manager.users_db import create_users_table
from db_manager.dishes_db import create_dishes_table, get_dishes_by_user_id, insert_one_dish
from db_manager.devices_db import create_devices_table, get_device_by_id, insert_one_device
from models.device import DeviceIn, DeviceOut
from typing import List
import os

from fastapi import FastAPI

from db_manager.db_connector import db
from models.dish import DishIn, DishOut, DishRequestBody

app = FastAPI()

@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()

@app.get('/')
async def root():
    return {
        'message': 'connected',
    }

@app.get('/create-tables/{admin_password}')
async def create_all_tables(admin_password: str):
    if admin_password == os.getenv('ADMIN_PASSWORD'):
        try:
            await create_users_table()
            await create_devices_table()
            await create_dishes_table()
        except Exception as e:
            print(f'error in application: {e}')
            return {
                'message': 'error in creating tables',
            }
        return {
            'message': 'tables succesfully created',
        }
    else:
        return JSONResponse(content={
            'message': 'password is incorrect'
        }, status_code=403)

@app.post('/devices', response_model=DeviceOut)
async def add_device(device: DeviceIn) -> dict:
    last_record_id = int(await insert_one_device(device))
    return {**device.dict(), 'id': last_record_id}

@app.get('/dishes/{device_id}', response_model=List[DishOut])
async def get_dishes(device_id: int):
    device = await get_device_by_id(device_id)
    if device == None:
        return {
            'message': 'device not found'
        }
    dishes = await get_dishes_by_user_id(device.user_id)
    return dishes

@app.post('/dishes', response_model=DishOut)
async def add_dish(dish_body: DishRequestBody) -> dict:
    device = await get_device_by_id(dish_body.device_id)
    if device == None:
        return {
            'message': 'device not found'
        }
    dish_input = DishIn(
        user_id=int(device.user_id),
        device_id=int(dish_body.device_id),
        name=str(dish_body.name),
        ingredients=list(dish_body.ingredients),
        quantity=float(dish_body.quantity),
    )
    last_record_id = await insert_one_dish(dish_input)
    return {**dish_input.dict(), 'id': last_record_id}
