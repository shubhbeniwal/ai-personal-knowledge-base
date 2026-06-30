import os

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

def store_chunks(
    chunks,
    source
):

    embeddings = model.encode(
        chunks
    ).tolist()

    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]

    metadatas = [
        {
            "source": os.path.basename(source)
        }
        for _ in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
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
    
    print(results)

    documents = results["documents"][0]

    sources = [
        item["source"]
        for item in results["metadatas"][0]
    ]

    context = "\n".join(
        documents
    )

    return context, list(
        set(sources)
    )