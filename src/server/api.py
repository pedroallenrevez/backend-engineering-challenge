import datetime
import json

from db import psql
from fastapi import FastAPI, WebSocket

from calc import SlidingWindow

app = FastAPI()


@app.get("/db_conn_test")
async def test_db():
    try:
        psql.test_insert()
        psql.clear()
        return {"status": 200}
    except Exception as e:
        return {"status": 404, "message": str(e)}


@app.websocket("/ws")
async def websocket_create(websocket: WebSocket):
    window = SlidingWindow(10)
    await websocket.accept()
    try:
        while True:
            # json data
            data = await websocket.receive_json()
            for ts, dur in window.consume(
                (datetime.datetime.fromisoformat(data["timestamp"]), data["duration"])
            ):
                psql.insert(ts, dur)

            await websocket.send_text("200")
    except Exception as e:
        raise e
    finally:
        ts, dur = window.flush()[0]
        psql.insert(ts, dur)
