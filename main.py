from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import re
import openai

app = FastAPI()

openai.api_key = "YOUR_OPENAI_API_KEY"

class Prompt(BaseModel):
    prompt: str

# Function to interact with GPT
def query_gpt(prompt, db_data):
    system_prompt = (
        "You are an assistant that answers queries about assets."
        " The provided data from the database is:\n" + db_data
    )

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Function to retrieve relevant data from the database
def get_db_data(prompt):
    conn = sqlite3.connect("equipment.db")
    cursor = conn.cursor()

    db_data = ""
    
    if re.search(r'\bhvac\b', prompt, re.I):
        cursor.execute("SELECT asset_code, asset_description, site_code, build_code FROM raw_assets WHERE asset_family_description LIKE '%HVAC%' LIMIT 10")
        rows = cursor.fetchall()
        db_data += "HVAC Assets:\n" + "\n".join([f"{r[0]} - {r[1]} (Site: {r[2]}, Building: {r[3]})" for r in rows])

    elif re.search(r'\bstatus\b', prompt, re.I):
        cursor.execute("SELECT asset_code, asset_description, status FROM raw_assets LIMIT 10")
        rows = cursor.fetchall()
        db_data += "Asset Status:\n" + "\n".join([f"{r[0]} - {r[1]} (Status: {r[2]})" for r in rows])

    else:
        cursor.execute("SELECT asset_code, asset_description FROM raw_assets LIMIT 5")
        rows = cursor.fetchall()
        db_data += "General Assets:\n" + "\n".join([f"{r[0]} - {r[1]}" for r in rows])

    conn.close()
    return db_data

@app.post("/gpt/ask")
def gpt_ask(data: Prompt):
    prompt = data.prompt

    try:
        # Fetch relevant data based on prompt
        db_data = get_db_data(prompt)

        # Generate GPT-powered smart response
        smart_response = query_gpt(prompt, db_data)

        return {"answer": smart_response}

    except Exception as e:
        return {"answer": f"An error occurred: {str(e)}"}
