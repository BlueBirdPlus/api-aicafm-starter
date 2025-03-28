@app.post("/gpt/ask")
def gpt_ask(data: dict):
    prompt = data.get("prompt")
    # Simulate response for now
    return {"answer": f"Simulated response to: {prompt}"}
