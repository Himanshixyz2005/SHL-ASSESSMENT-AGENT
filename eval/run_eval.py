import sys
import os
import json
import time

# Project root add
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agent import get_agent_response


test_cases = [

    {
        "name": "Clarification Test",
        "messages": [
            {
                "role": "user",
                "content": "I need some assessments."
            }
        ]
    },

    {
        "name": "Recommendation Test",
        "messages": [
            {
                "role": "user",
                "content": "Show me software developer tests for mid-level professionals."
            }
        ]
    },

    {
        "name": "Refinement Test",
        "messages": [
            {
                "role": "user",
                "content": "Show me technical assessments."
            },
            {
                "role": "assistant",
                "content": "Sure."
            },
            {
                "role": "user",
                "content": "Actually only remote ones."
            }
        ]
    },

    {
        "name": "Off Topic Test",
        "messages": [
            {
                "role": "user",
                "content": "What is the weather in Delhi?"
            }
        ]
    }

]


def run_evaluation():

    with open("data/catalog.json", "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print("=" * 70)
    print("SHL AGENT LOCAL EVALUATOR")
    print("=" * 70)

    for test in test_cases:

        print(f"\nRunning : {test['name']}")

        start = time.time()

        response = get_agent_response(
            test["messages"],
            catalog
        )

        elapsed = time.time() - start

        print(f"Time : {elapsed:.2f} sec")
        print(f"Reply : {response['reply']}")

        print("\nRecommendations:")

        if response["recommendations"]:

            for rec in response["recommendations"]:

                print(
                    f"- {rec.get('name','')} | {rec.get('url', rec.get('link',''))}"
                )

        else:

            print("None")

        print(f"\nEnd Conversation : {response['end_of_conversation']}")

        print("-" * 70)


if __name__ == "__main__":
    run_evaluation()