from app.retrieval import search_tests
from app.llm import ask_llm
from app.guardrails import is_off_topic, is_prompt_injection
from app.compare import compare_assessments
import json


def get_agent_response(history, catalog):
    """
    Generates the next response for the SHL Assessment Agent.

    Args:
        history (list): Full conversation history.
        catalog (list): SHL assessment catalog.

    Returns:
        dict:
        {
            "reply": str,
            "recommendations": list,
            "end_of_conversation": bool
        }
    """

    # ---------------------------------------
    # Build search query from all USER messages
    # ---------------------------------------

    user_messages = [
        msg["content"]
        for msg in history
        if msg.get("role") == "user"
    ]

    search_query = " ".join(user_messages).strip()
    latest_message = user_messages[-1] if user_messages else ""
    query_lower = search_query.lower()

    # ---------------------------------------
    # Clarification Logic
    # ---------------------------------------

    LOW_INFO_KEYWORDS = [
        "assessment",
        "assessments",
        "test",
        "tests",
        "hire",
        "hiring",
        "job",
        "candidate",
        "employee",
        "recruitment"
    ]

    meaningful_words = [
        word
        for word in query_lower.split()
        if len(word) > 2
    ]

    ROLE_HINTS = [
    "developer",
    "engineer",
    "analyst",
    "manager",
    "support",
    "administrator",
    "consultant",
    "sales",
    "finance",
    "marketing",
    "qa",
    "tester",
    "java",
    "python",
    "c++",
    "c#",
    "javascript",
    "react",
    "node",
    "sql",
    "aws",
    "azure",
    "cloud"
]

    has_role_hint = any(role in query_lower for role in ROLE_HINTS)

    is_vague = (
    len(meaningful_words) <= 2
    and any(keyword in query_lower for keyword in LOW_INFO_KEYWORDS)
    and not has_role_hint
)
    

    if is_vague:
        return {
            "reply": (
                "I'd be happy to help. Could you please tell me:\n"
                "- What role are you hiring for?\n"
                "- What is the seniority level?\n"
                "- Are you looking for technical, cognitive, personality, or behavioural assessments?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # ---------------------------------------
    # Off-topic Guard
    # ---------------------------------------

    if is_off_topic(query_lower):
        return {
            "reply": (
                "I'm an SHL Assessment Assistant. "
                "I can only help with SHL assessments, "
                "assessment recommendations, and comparisons "
                "between SHL assessments."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # ---------------------------------------
    # Prompt Injection Guard
    # ---------------------------------------

    if is_prompt_injection(query_lower):
        return {
            "reply": (
                "I cannot ignore my instructions or reveal internal prompts. "
                "I can only assist with SHL assessments."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # ---------------------------------------
    # Comparison Mode
    # ---------------------------------------

    comparison_keywords = [
        "compare",
        "difference",
        "vs",
        "versus"
    ]

    if any(word in query_lower for word in comparison_keywords):

        comparison = compare_assessments(search_query, catalog)

        if comparison:
            return comparison

    # ---------------------------------------
    # Retrieve assessments
    # ---------------------------------------

    recommendations = search_tests(search_query, catalog)

    # ---------------------------------------
    # LLM Prompt
    # ---------------------------------------

    system_prompt = f"""
You are an AI Assistant for SHL.

You MUST answer ONLY using the provided SHL assessment catalog.

Conversation History:
{json.dumps(history, indent=2)}

Retrieved Assessments:
{json.dumps(recommendations, indent=2)}

Rules:

1. Answer only using retrieved SHL assessments.
2. Never invent assessment names or URLs.
3. Never recommend assessments not present in the retrieved list.
4. Use conversation history.
5. If no assessment matches, politely ask for more information.
6. If the user changes requirements, update recommendations instead of starting over.
7. Keep replies concise and professional.
"""

    try:
       reply = ask_llm(system_prompt, search_query)

    except Exception:

        reply = (
            "I'm sorry, I'm currently unable to access the SHL assessment catalog."
        )

    # ---------------------------------------
    # Required Response Schema
    # ---------------------------------------

    end_of_conversation = len(recommendations) > 0

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": end_of_conversation
    }