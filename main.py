from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
