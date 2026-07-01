from fastapi import FastAPI
import json
from pydantic import BaseModel
from typing import List, Dict
from app.agent import get_agent_response

# 1. Update model to accept full message history
class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]

app = FastAPI()

with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    # Pass the WHOLE list of messages to the agent
    response = get_agent_response(request.messages, catalog) 
    
    # Map "link" to "url" (Hard Eval fix)
    for rec in response.get("recommendations", []):
        if "link" in rec:
            rec["url"] = rec.pop("link")
            
    return response