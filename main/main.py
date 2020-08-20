import asyncio
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
from collector import collect
from schemas import Route
from database import db, get_database



app = FastAPI()
collector = collect


script_location = Path(__file__).absolute().parent
file_location = script_location / 'index.html'
f = file_location.open()
page = f.read()
f.close()


async def connect_to_mongo():
    db.client = AsyncIOMotorClient('127.0.0.1', 27017)


async def close_mongo_connection():
    db.client.close()


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


@app.get("/", response_class=HTMLResponse)
async def index():
    return page


async def get_collection(params, collection):
    cursor = collection.find(params)
    for document in await cursor.to_list(length=1):
        document.pop('_id')
        return document


@app.get('/{route}')
async def root(route: str):
    client = await get_database()
    db = client['flight_routes_project']
    collection = db['flight_routes']
    if route == 'collector_run':
        async for i in collector():
            data = Route(route=i['route'], dates=i['dates'])
            await collection.delete_many({'route':i['route']})
            await collection.insert_one(data.dict())
        return data.dict()
    else:
        params = {'route': route}
        data = await get_collection(params, collection)
        return data



if __name__== '__main__':
    uvicorn.run(app,host="0.0.0.0",port="8000")
