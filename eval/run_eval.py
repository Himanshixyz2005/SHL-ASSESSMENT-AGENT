import sys
import os

# Project path add karo taaki app modules import ho sakein
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agent import get_agent_response
import json

# Test cases (Queries + Expected Behavior)
test_cases = [
    {
        "query": "I need some assessments.",
        "type": "Vague/Clarification"
    },
    {
        "query": "Show me software developer tests for mid-level professionals.",
        "type": "Specific"
    },
    {
        "query": "Actually, only show me the remote ones.",
        "type": "Refinement"
    },
    {
        "query": "What is the weather in Delhi?",
        "type": "Guardrail"
    }
]

def run_evaluation():
    # Load catalog once
    with open("data/catalog.json", "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print("--- Starting Agent Evaluation ---\n")
    for test in test_cases:
        print(f"Testing [{test['type']}]: {test['query']}")
        response = get_agent_response(test['query'], catalog)
        print(f"Agent Reply: {response['reply'][:100]}...") # First 100 chars
        print("-" * 30)

if __name__ == "__main__":
    run_evaluation()