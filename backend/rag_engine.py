import os

from dotenv import load_dotenv

from groq import Groq

from vectorstore import search_chunks

from memory import (get_summary, update_summary)

from memory_store import (
    save_memory,
    retrieve_memory,
    should_store_memory
)


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
    
    memory_context = retrieve_memory(
        question
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

    1. Use BOTH:

    - Relevant Past Memory
    - Knowledge Base Context

    when answering.

    2. Prefer Knowledge Base Context for factual document questions.

    3. Use Relevant Past Memory for conversational facts and previous user information.

    4. If the answer is found in neither Memory nor Knowledge Base Context, say:

    "I could not find that information in the uploaded documents or conversation history."

    5. Do not invent facts.

    Conversation Summary:
    {existing_summary}
    
    Conversation History:
    {conversation_context}

    Relevant Past Memory:
    {memory_context}

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
    
    memory_context = retrieve_memory(
        question
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

    1. Use BOTH:

    - Relevant Past Memory
    - Knowledge Base Context

    when answering.

    2. Prefer Knowledge Base Context for factual document questions.

    3. Use Relevant Past Memory for conversational facts and previous user information.

    4. If the answer is found in neither Memory nor Knowledge Base Context, say:

    "I could not find that information in the uploaded documents or conversation history."

    5. Do not invent facts.

    
    Conversation Summary:
    {existing_summary}
    
    Conversation History:
    {conversation_context}

    Relevant Past Memory:
    {memory_context}

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
    
    if should_store_memory(question):

        save_memory(question)

    yield "\n[SOURCES]\n"

    for source in sources:

        yield source + "\n"