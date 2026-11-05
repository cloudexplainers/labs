import asyncio
import time

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Tea(BaseModel):
    name: str
    price: float
    stock: int


teas = [Tea(name="Sencha", price=6.5, stock=40),
        Tea(name="Earl Grey", price=5.0, stock=25)]


@app.get("/teas")
def list_teas():
    return teas


@app.post("/teas")
def add_tea(tea: Tea):
    teas.append(tea)
    return tea


@app.get("/supplier")
async def supplier():
    await asyncio.sleep(1)  # wait for the supplier's site
    return {"ok": True}
