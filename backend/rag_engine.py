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


def ask_rag(question, selected_documents=None, chat_history=None):

    context, sources = search_chunks(
        question,
        selected_documents
    )
    
    conversation_context = ""

    if chat_history:

        recent_messages = chat_history[-5:]

        for chat in recent_messages:

            conversation_context += (
                f"User: {chat['question']}\n"
                f"Assistant: {chat['answer']}\n\n"
            )

    prompt = f"""
    You are a helpful assistant.

    Use the conversation history when relevant.

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

    if chat_history:

        recent_messages = chat_history[-5:]

        for chat in recent_messages:

            conversation_context += (
                f"User: {chat['question']}\n"
                f"Assistant: {chat['answer']}\n\n"
            )

    prompt = f"""
    You are a helpful assistant.

    Use the conversation history when relevant.

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

    for chunk in response:

        if (
            chunk.choices
            and chunk.choices[0].delta.content
        ):

            text = chunk.choices[0].delta.content

            yield text

    yield "\n[SOURCES]\n"

    for source in sources:

        yield source + "\n"