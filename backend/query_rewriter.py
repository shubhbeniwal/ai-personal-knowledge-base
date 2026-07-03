import os

from dotenv import load_dotenv

from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def rewrite_query(
    question,
    chat_history=None
):
    
    memory_prefixes = [

        "remember",

        "store",

        "save"

    ]

    if any(
        question.lower().startswith(prefix)
        for prefix in memory_prefixes
    ):
        return question

    if not chat_history:
        return question

    recent_history = ""

    for chat in chat_history[-5:]:

        recent_history += (
            f"User: {chat['question']}\n"
            f"Assistant: {chat['answer']}\n\n"
        )

    prompt = f"""
    Rewrite the user's question into a standalone question.

    Rules:

    - Do NOT answer.
    - Do NOT explain.
    - Do NOT summarize.
    - Do NOT add information.
    - Do NOT remove information.

    Only resolve references such as:

    - he
    - she
    - they
    - it
    - there
    - this
    - that

    Use conversation history only when necessary.

    Important:

    Do NOT rewrite questions that already refer to:

    - Technologies
    - Databases
    - Frameworks
    - Programming Languages
    - Products
    - Companies
    - Public Concepts

    Examples:

    User:
    Tell me about PostgreSQL

    Output:
    Tell me about PostgreSQL

    ---

    User:
    Explain LangChain

    Output:
    Explain LangChain

    ---

    User:
    What is React?

    Output:
    What is React?

    ---

    User:
    What did Shubh do at LTIMindtree?

    Output:
    What did Shubh do at LTIMindtree?

    ---

    Conversation:
    User: What did Shubh do at LTIMindtree?

    User: What technologies did he use there?

    Output:
    What technologies did Shubh use at LTIMindtree?

    Conversation:
    {recent_history}

    Current Question:
    {question}

    Standalone Question:
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    rewritten_question = (
        response.choices[0]
        .message
        .content
        .strip()
    )

    bad_phrases = [
        "there is no mention",
        "i don't know",
        "not enough information",
        "the conversation does not",
        "based on the conversation",
        "cannot determine",
        "insufficient information",
    ]

    if any(
        phrase in rewritten_question.lower()
        for phrase in bad_phrases
    ):
        return question

    return rewritten_question