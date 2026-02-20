from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def contract_chatbot(contract_text, user_query):

    contract_text = contract_text[:4000]

    prompt = f"""
You are a car lease advisor.

Contract:
{contract_text}

User question:
{user_query}

Answer clearly and practically.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    return response.choices[0].message.content