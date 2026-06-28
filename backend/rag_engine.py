import os

from dotenv import load_dotenv

from groq import Groq

from vectorstore import search_chunks


load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


def ask_rag(question):

    context = search_chunks(
        question
    )

    prompt = f"""
You are a helpful assistant.

Answer ONLY from the context below.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content