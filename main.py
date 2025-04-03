from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Prompt(BaseModel):
    prompt: str

@app.post("/gpt/ask")
def gpt_ask(data: Prompt):
    prompt = data.prompt

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return {"answer": response.choices[0].message.content}

    except Exception as e:
        return {"answer": f"An error occurred: {str(e)}"}
