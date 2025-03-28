
from fastapi import FastAPI, Query
from pydantic import BaseModel
import sqlite3
import re

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/gpt/ask")
def gpt_ask(data: Prompt):
    prompt = data.prompt.lower()
    conn = sqlite3.connect("equipment.db")
    cursor = conn.cursor()

    response = "Sorry, I didn't understand the request. Try asking about asset count, status, or search."

    try:
        if "hvac" in prompt and "site" in prompt and "building" in prompt:
            site_match = re.search(r"site\s*(\d+)", prompt)
            build_match = re.search(r"building\s*(\d+)", prompt)

            if site_match and build_match:
                site_code = site_match.group(1)
                build_code = build_match.group(1)
                query = f"""
                    SELECT COUNT(*) FROM raw_assets
                    WHERE LOWER(asset_family_description) LIKE '%hvac%'
                    AND site_code LIKE '%{site_code}%'
                    AND build_code LIKE '%{build_code}%'
                """
                cursor.execute(query)
                count = cursor.fetchone()[0]
                response = f"There are {count} HVAC assets in site {site_code}, building {build_code}."

        elif "name" in prompt or "search" in prompt or "asset" in prompt:
            cursor.execute("SELECT asset_code, asset_description FROM raw_assets LIMIT 5")
            rows = cursor.fetchall()
            response = "Search results:\n" + "\n".join([f"{r[0]} - {r[1]}" for r in rows])

        elif "status" in prompt:
            cursor.execute("SELECT asset_code, asset_description FROM raw_assets LIMIT 3")
            rows = cursor.fetchall()
            response = "Current asset status:\n" + "\n".join([f"{r[0]} - {r[1]}" for r in rows])

    except Exception as e:
        response = f"Error occurred: {str(e)}"

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
