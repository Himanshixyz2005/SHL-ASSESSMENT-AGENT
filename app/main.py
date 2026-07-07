from fastapi import FastAPI
import json
from pydantic import BaseModel
from typing import List, Dict
from app.agent import get_agent_response

app = FastAPI()


class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]


with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):

    response = get_agent_response(request.messages, catalog)

    # Ensure evaluator always gets a URL field
    for rec in response.get("recommendations", []):

        if "url" not in rec and "link" in rec:
            rec["url"] = rec["link"]

        rec.setdefault("url", "")
        rec.setdefault("name", "")
        rec.setdefault("test_type", "")

    response.setdefault("reply", "")
    response.setdefault("recommendations", [])
    response.setdefault("end_of_conversation", False)

    return response