from dotenv import load_dotenv

DEBUG = True
if DEBUG:
    load_dotenv()

import json
import os
from typing import List

import httpx
from fastapi import FastAPI
from starlette.responses import JSONResponse

from db_manager.db_connector import db
from db_manager.devices_db import (create_devices_table, get_device_by_id,
                                   insert_one_device)
from db_manager.dishes_db import (create_dishes_table, get_dishes_by_user_id,
                                  insert_one_dish)
from db_manager.users_db import create_users_table
from models.device import DeviceIn, DeviceOut
from models.dish import DishIn, DishOut, DishRequestBody

EDAMAM_APPLICATION_ID = os.getenv('EDAMAM_APPLICATION_ID')
EDAMAM_APPLICATION_KEY = os.getenv('EDAMAM_APPLICATION_KEY')

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

@app.get('/mass-wasted/{user_id}', response_model=int)
async def get_mass_wasted(user_id: int):
    return 23

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

@app.get('/dishes/{user_id}', response_model=List[DishOut])
async def get_dishes(user_id: int):
    dishes = await get_dishes_by_user_id(user_id)
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


@app.get('/dish-search')
async def search_dish(query: str = ''):
    if query == '':
        return JSONResponse(status_code=400, content={
            'message': "the 'query' query parameter should be provided to this route"
        })
    # edamam_api_url = f'https://api.edamam.com/search?q={query}&app_id={EDAMAM_APPLICATION_ID}&app_key={EDAMAM_APPLICATION_KEY}'
    
    # edamam_api_response = None
    # async with httpx.AsyncClient() as client:
    #     edamam_api_response = await client.get(edamam_api_url)
    # return edamam_api_response.json()
    edamam_chicken_response = None
    with open('./edamam_chicken_response.json', mode='r') as file:
        edamam_chicken_response = json.load(file)
    return edamam_chicken_response
