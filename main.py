import asyncio
import json

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket

app = FastAPI()


reactions_arr = []
websockets: list[WebSocket] = []
websockets2: list[WebSocket] = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket('/reactions')
async def reactions(websocket: WebSocket):
    await websocket.accept()

    websockets.append(websocket)

    try:
        while True:
            await asyncio.sleep(1)

    except Exception:
        websockets.remove(websocket)
        await websocket.close()


@app.websocket('/emoji')
async def reactions(websocket: WebSocket):
    await websocket.accept()

    websockets2.append(websocket)

    try:
        while True:
            await asyncio.sleep(1)

    except Exception:
        websockets2.remove(websocket)
        await websocket.close()


class Data(BaseModel):
    text: str


@app.post('/reaction')
async def reaction(data: Data):
    reactions_arr.append(data.text)

    for ws in websockets:
        try:
            await ws.send_text(data.text)

        except Exception as e:
            print(e)
            print('No websocket')


@app.post('/emoji')
async def emoji(data: Data):
    reactions_arr.append(data.text)

    for ws in websockets2:
        try:
            await ws.send_text(data.text)

        except Exception as e:
            print(e)
            print('No websocket')
