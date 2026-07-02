import os

from dotenv import load_dotenv

from groq import Groq

from vectorstore import search_chunks

from memory import (get_summary, update_summary)


load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


def ask_rag(question, selected_documents=None, chat_history=None):

    context, sources = search_chunks(
        question,
        selected_documents
    )
    
    conversation_context = ""

    existing_summary = get_summary()

    if chat_history:

        recent_messages = chat_history[-5:]

        for chat in recent_messages:

            conversation_context += (
                f"User: {chat['question']}\n"
                f"Assistant: {chat['answer']}\n\n"
            )
        
        existing_summary = get_summary()

    prompt = f"""
    You are an enterprise knowledge-base assistant.

    Rules:

    1. Answer ONLY using information found in the Knowledge Base Context.

    2. If the answer is not present in the context, say:

    "I could not find that information in the uploaded documents."

    3. Do not make assumptions.

    4. Do not invent facts.

    5. Keep answers concise and factual.

    6. Use bullet points when appropriate.

    Conversation Summary:
    {existing_summary}
    
    Conversation History:
    {conversation_context}

    Knowledge Base Context:
    {context}

    Current Question:
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
    selected_documents=None,
    chat_history=None
):

    context, sources = search_chunks(
        question,
        selected_documents
    )
    
    conversation_context = ""

    existing_summary = get_summary()

    if chat_history:

        recent_messages = chat_history[-5:]

        for chat in recent_messages:

            conversation_context += (
                f"User: {chat['question']}\n"
                f"Assistant: {chat['answer']}\n\n"
            )
        
        existing_summary = get_summary()

    prompt = f"""
    You are an enterprise knowledge-base assistant.

    Rules:

    1. Answer ONLY using information found in the Knowledge Base Context.

    2. If the answer is not present in the context, say:

    "I could not find that information in the uploaded documents."

    3. Do not make assumptions.

    4. Do not invent facts.

    5. Keep answers concise and factual.

    6. Use bullet points when appropriate.

    
    Conversation Summary:
    {existing_summary}
    
    Conversation History:
    {conversation_context}

    Knowledge Base Context:
    {context}

    Current Question:
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

    full_answer = ""
    
    for chunk in response:

        if (
            chunk.choices
            and chunk.choices[0].delta.content
        ):

            text = chunk.choices[0].delta.content
            full_answer += text

            yield text
    
    new_summary = f"""
    User: {question}

    Assistant: {full_answer}
    """

    update_summary(
        get_summary()
        + "\n"
        + new_summary
    )

    yield "\n[SOURCES]\n"

    for source in sources:

        yield source + "\n"