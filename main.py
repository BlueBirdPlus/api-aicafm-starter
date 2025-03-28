from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Existing command/send API
class Command(BaseModel):
    equipment_id: int
    command: str

@app.post("/command/send")
def send_command(data: Command):
    return {
        "status": "received",
        "equipment_id": data.equipment_id,
        "command": data.command
    }

# ✅ New model for /gpt/ask
class Prompt(BaseModel):
    prompt: str

@app.post("/gpt/ask")
def gpt_ask(data: Prompt):
    prompt = data.prompt
    # Simulated response for now
    return {
        "answer": f"You asked: '{prompt}'. This is a placeholder response."
    }
