import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(system_prompt, user_message):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # <--- Yahan change karo
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content