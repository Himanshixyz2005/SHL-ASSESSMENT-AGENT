# SHL Assessment Agent

An AI-powered conversational assistant that recommends SHL assessments based on recruiter requirements using Retrieval-Augmented Generation (RAG).

## Features

- AI-powered assessment recommendations
- Multi-turn conversation support
- Context-aware refinement
- Assessment comparison
- Prompt injection protection
- Off-topic guardrails
- FastAPI REST API
- Automated API tests
- Public deployment on Render

---

## Tech Stack

- FastAPI
- Python
- Groq Llama 3.3 70B Versatile
- Custom Retrieval Engine
- Pytest
- Render

---

## Project Structure

```
app/
    agent.py
    retrieval.py
    compare.py
    guardrails.py
    llm.py
    main.py

data/
    catalog.json

tests/
    test_api.py

eval/
    run_eval.py
```

---

## API

### Health

```
GET /health
```

Response

```json
{
  "status":"ok"
}
```

---

### Chat

```
POST /chat
```

Example Request

```json
{
    "messages":[
        {
            "role":"user",
            "content":"Recommend Java assessments."
        }
    ]
}
```

Example Response

```json
{
    "reply":"...",
    "recommendations":[...],
    "end_of_conversation":true
}
```

---

## Supported Capabilities

- Recommend assessments
- Clarify vague queries
- Refine recommendations
- Compare assessments
- Reject off-topic requests
- Resist prompt injection

---

## Testing

Run API tests

```bash
pytest tests/test_api.py -v
```

Current Result

```
12 Passed
```

---

## Deployment

Render

```
https://shl-assessment-agent-cw99.onrender.com
```

---

## Author

Himanshi Goyal
