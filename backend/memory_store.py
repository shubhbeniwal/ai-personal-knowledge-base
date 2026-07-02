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

        n_results=3

    )

    print("\n--- MEMORY RETRIEVAL ---")
    print(results)  
    
    if not results["documents"]:
        return ""

    if not results["documents"][0]:
        return ""

    return "\n".join(
        results["documents"][0]
    )