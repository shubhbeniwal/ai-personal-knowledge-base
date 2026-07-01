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


def ask_rag(question, selected_documents=None):

    context, sources = search_chunks(
        question,
        selected_documents
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
        ],
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }
    
def ask_rag_stream(
    question,
    selected_documents=None
):

    context, sources = search_chunks(
        question,
        selected_documents
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
        ],
        stream=True
    )

    for chunk in response:

        if (
            chunk.choices
            and chunk.choices[0].delta.content
        ):

            text = chunk.choices[0].delta.content

            print(text, end="", flush=True)

            yield text