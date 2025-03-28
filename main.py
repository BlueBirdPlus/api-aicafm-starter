
from fastapi import FastAPI, Query
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/gpt/ask")
def gpt_ask(data: Prompt):
    prompt = data.prompt.lower()
    conn = sqlite3.connect("equipment.db")
    cursor = conn.cursor()

    response = "Sorry, I didn't understand the request. Try asking about status or asset search."

    if "name" in prompt or "search" in prompt or "asset" in prompt:
        cursor.execute("SELECT asset_code, asset_description FROM raw_assets LIMIT 5")
        rows = cursor.fetchall()
        response = "Search results:\n" + "\n".join([f"{r[0]} - {r[1]}" for r in rows])
    elif "status" in prompt:
        cursor.execute("SELECT asset_code, asset_description FROM raw_assets LIMIT 3")
        rows = cursor.fetchall()
        response = "Current asset status:\n" + "\n".join([f"{r[0]} - {r[1]}" for r in rows])

    conn.close()
    return {"answer": response}

@app.get("/assets/search")
def search_assets(name: str = Query(..., description="Asset name (partial or full)")):
    conn = sqlite3.connect("equipment.db")
    cursor = conn.cursor()
    cursor.execute("SELECT asset_code, asset_description FROM raw_assets WHERE asset_description LIKE ?", ('%' + name + '%',))
    rows = cursor.fetchall()
    conn.close()
    return [{"code": r[0], "description": r[1]} for r in rows]
