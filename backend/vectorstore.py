from chromadb import PersistentClient

from sentence_transformers import SentenceTransformer


client = PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    "knowledge_base"
)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


import uuid


def store_chunks(chunks):

    embeddings = model.encode(
        chunks
    ).tolist()

    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks
    )


def search_chunks(query):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=5
    )

    return "\n".join(
        results["documents"][0]
    )