import uuid

from chromadb import PersistentClient

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
    
client = PersistentClient(
    path="./chroma_db"
)

memory_collection = client.get_or_create_collection(
    "conversation_memory"
)

def save_memory(text):

    embedding = model.encode(text).tolist()

    memory_collection.add(
        ids=[str(uuid.uuid4())],
        documents=[text],
        embeddings=[embedding]
    )
    
    print("\n--- SAVING MEMORY ---")
    print(text)
    
def retrieve_memory(query):
    
    query_embedding = model.encode(
        query
    ).tolist()

    results = memory_collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=3,
        include=["documents", "distances"]

    )

    print("\n--- MEMORY RETRIEVAL ---")
    print(results)  
    
    if not results["documents"]:
        return ""

    if not results["documents"][0]:
        return ""

    memory_docs = []

    for doc, distance in zip(
        results["documents"][0],
        results["distances"][0]
    ):

        if distance < 0.8:
            memory_docs.append(doc)

    if not memory_docs:
        return ""

    return "\n".join(memory_docs)

def should_store_memory(user_message):

    text = user_message.lower().strip()

    question_starters = [
        "what",
        "who",
        "where",
        "when",
        "why",
        "how",
        "which",
        "can",
        "could",
        "would",
        "do",
        "does",
        "did",
        "is",
        "are",
        "am",
        "was",
        "were"
    ]

    for starter in question_starters:
        if text.startswith(starter + " "):
            return False

    if text.endswith("?"):
        return False

    memory_patterns = [
        "i work",
        "i live",
        "my goal",
        "my birthday",
        "my favourite",
        "remember",
        "my name is",
        "i am",
        "i work at",
        "i live in",
        "i prefer",
        "i like",
        "i love",
        "my favorite",
        "my favourite",
        "my hobby",
        "my hobbies",
        "my goals",
        "my birthday",
        "my pet",
        "my dog",
        "my cat",
        "i study",
        "i am studying",
        "i graduated from",
        "i use",
        "i enjoy"
    ]

    return any(
        pattern in text
        for pattern in memory_patterns
    )
    
def clean_memory_text(text):

    text = text.strip()

    prefixes = [
        "remember ",
        "remember that ",
    ]

    lower_text = text.lower()

    for prefix in prefixes:

        if lower_text.startswith(prefix):

            return text[len(prefix):]

    return text