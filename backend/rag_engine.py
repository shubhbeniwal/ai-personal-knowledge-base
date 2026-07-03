import os

from dotenv import load_dotenv

from groq import Groq

from vectorstore import search_chunks

from memory import (get_summary, update_summary)

from memory_store import (
    clean_memory_text,
    save_memory,
    retrieve_memory,
    should_store_memory
)

from query_rewriter import rewrite_query

load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


def ask_rag(question, selected_documents=None, chat_history=None):

    if should_store_memory(question):

        save_memory(clean_memory_text(question))

        return {
            "answer": "Got it. I'll remember that.",
            "sources": []
        }

    rewritten_question = rewrite_query(
        question,
        chat_history
    )

    context, sources = search_chunks(
        rewritten_question,
        selected_documents
    )
    
    memory_context = retrieve_memory(
        rewritten_question
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
    You are a Personal Knowledge Base Assistant.

    Available Information Sources:

    1. Uploaded Documents
    2. Relevant User Memory
    3. Conversation History
    4. General Knowledge

    Source Priority:

    Uploaded Documents > User Memory > Conversation History > General Knowledge

    Rules:

    - Use Uploaded Documents whenever the answer exists there.
    - Use User Memory only for personal facts previously shared by the user.
    - Use Conversation History to resolve references and maintain context.
    - Use General Knowledge for public concepts, technologies, frameworks, companies, products, programming languages, databases, scientific concepts, and other non-personal information.

    Important:

    User Memory contains personal facts.

    Examples:

    Memory:
    "My favorite color is blue."

    Question:
    "What is my favorite color?"

    Use Memory.

    ---

    Memory:
    "My favorite framework is LangChain."

    Question:
    "Tell me about LangChain."

    Use General Knowledge.

    Do NOT answer:

    "Your favorite framework is LangChain."

    ---

    Question:
    "What did I do at my company?"

    Use Documents + Memory.

    ---

    Question:
    "What is PostgreSQL?"

    Use General Knowledge.

    ---

    Question:
    "What technologies did I use at LTIMindtree?"

    Use Documents + Memory.

    Never confuse:

    - Personal preferences
    - Public knowledge

    Never invent information.

    If information cannot be found in any source, say:

    "I could not find that information in the uploaded documents, memory, conversation history, or general knowledge."
    
    Memory Usage Rules:

    Use memory only when the user asks about:

    - themselves
    - their preferences
    - their history
    - their goals
    - their previously shared information

    Do not use memory to answer general knowledge questions.

    Example:

    Memory:
    "My favorite database is PostgreSQL"

    Question:
    "What is PostgreSQL?"

    Answer:
    Explain PostgreSQL using general knowledge.

    Question:
    "What is my favorite database?"

    Answer:
    Use memory.

    Conversation Summary:
    {existing_summary}

    Conversation History:
    {conversation_context}

    Relevant User Memory:
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

    if should_store_memory(question):

        save_memory(clean_memory_text(question))

        yield "Got it. I'll remember that."

        return

    rewritten_question = rewrite_query(
        question,
        chat_history
    )

    print("\n--- QUERY REWRITE ---")
    print("Original:", question)
    print("Rewritten:", rewritten_question)
    
    context, sources = search_chunks(
        rewritten_question,
        selected_documents
    )
    
    memory_context = retrieve_memory(
        rewritten_question
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
    You are a Personal Knowledge Base Assistant.

    Available Information Sources:

    1. Uploaded Documents
    2. Relevant User Memory
    3. Conversation History
    4. General Knowledge

    Source Priority:

    Uploaded Documents > User Memory > Conversation History > General Knowledge

    Rules:

    - Use Uploaded Documents whenever the answer exists there.
    - Use User Memory only for personal facts previously shared by the user.
    - Use Conversation History to resolve references and maintain context.
    - Use General Knowledge for public concepts, technologies, frameworks, companies, products, programming languages, databases, scientific concepts, and other non-personal information.

    Important:

    User Memory contains personal facts.

    Examples:

    Memory:
    "My favorite color is blue."

    Question:
    "What is my favorite color?"

    Use Memory.

    ---

    Memory:
    "My favorite framework is LangChain."

    Question:
    "Tell me about LangChain."

    Use General Knowledge.

    Do NOT answer:

    "Your favorite framework is LangChain."

    ---

    Question:
    "What did I do at my company?"

    Use Documents + Memory.

    ---

    Question:
    "What is PostgreSQL?"

    Use General Knowledge.

    ---

    Question:
    "What technologies did I use at LTIMindtree?"

    Use Documents + Memory.

    Never confuse:

    - Personal preferences
    - Public knowledge

    Never invent information.

    If information cannot be found in any source, say:

    "I could not find that information in the uploaded documents, memory, conversation history, or general knowledge."
    
    Memory Usage Rules:

    Use memory only when the user asks about:

    - themselves
    - their preferences
    - their history
    - their goals
    - their previously shared information

    Do not use memory to answer general knowledge questions.

    Example:

    Memory:
    "My favorite database is PostgreSQL"

    Question:
    "What is PostgreSQL?"

    Answer:
    Explain PostgreSQL using general knowledge.

    Question:
    "What is my favorite database?"

    Answer:
    Use memory.

    Conversation Summary:
    {existing_summary}

    Conversation History:
    {conversation_context}

    Relevant User Memory:
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