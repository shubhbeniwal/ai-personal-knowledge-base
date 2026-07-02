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

    memory_collection.add(

        ids=[
            str(uuid.uuid4())
        ],

        documents=[
            text
        ]

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

        if distance < 1.2:
            memory_docs.append(doc)

    if not memory_docs:
        return ""

    return "\n".join(memory_docs)

def should_store_memory(
    user_message
):

    keywords = [

        "remember",

        "my favorite",

        "my favourite",

        "i like",

        "i love",

        "i prefer",

        "my name is",

        "i live",

        "i work",

        "my goal",

        "my hobby",

        "my birthday"

    ]

    text = user_message.lower()

    return any(
        keyword in text
        for keyword in keywords
    )