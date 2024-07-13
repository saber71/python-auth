import cryptocode
import requests
import uvicorn
from fastapi import FastAPI

from .types import Auth, Base

BASE_URL = "http://localhost:10001"
SECRET_KEY = "secret"

app = FastAPI()


@app.get("/")
async def root():
    return ""


@app.post("/check")
async def check(auth: Auth):
    res = requests.post(
        BASE_URL + "/storage/get",
        data={"name": "auth", "type": auth.storageType, "id": auth.id},
    )
    if res.text != "":
        data = res.json()
        if data["password"] == cryptocode.encrypt(auth.password, SECRET_KEY):
            return "true"
        else:
            return "wrong password"
    else:
        return "not found password"


@app.post("/save")
async def save(auth: Auth):
    res = requests.post(
        BASE_URL + "/storage/save",
        data={
            "name": "auth",
            "type": auth.storageType,
            "value": [
                {
                    "_id": auth.id,
                    "password": cryptocode.encrypt(auth.password, SECRET_KEY),
                }
            ],
        },
    )
    if res.text != "":
        return "true"
    else:
        return "false"


@app.post("/delete")
async def delete(data: Base):
    res = requests.post(
        BASE_URL + "/storage/delete",
        data={
            "name": "auth",
            "type": data.storageType,
            "id": data.id,
            "returnResult": True,
        },
    )
    if res.text != "":
        return "true"
    else:
        return "false"


uvicorn.run(app, host="127.0.0.1", port=10002)
