from app.retrieval import search_tests
from app.llm import ask_llm
import json

def get_agent_response(history, catalog):
    # 'history' is now a list of all messages (e.g., [{"role": "user", "content": "..."}, ...])
    # Latest message content is the last item
    latest_message = history[-1]["content"]
    
    # 1. Retrieval: Use the latest message to search
    recommendations = search_tests(latest_message, catalog)
    
    # 2. LLM Prompting
    system_prompt = f"""
    You are an AI Assistant for SHL. You must assist users based strictly on the provided assessment catalog.
    
    Conversation History: {json.dumps(history)}
    
    Provided Assessments:
    {json.dumps(recommendations, indent=2)}

    Rules:
    1. Language: Strictly communicate in English only.
    2. Scope: Only recommend assessments from the provided list. 
    3. Tone: Maintain a professional, helpful, and concise recruiter tone.
    4. Formatting: Do not include conversational filler.
    """
    
    try:
        # We pass the prompt + the latest message
        reply = ask_llm(system_prompt, latest_message)
    except Exception as e:
        reply = "I'm sorry, I am currently having trouble accessing my database."
    
    return {
        "reply": reply,
        "recommendations": recommendations
    }