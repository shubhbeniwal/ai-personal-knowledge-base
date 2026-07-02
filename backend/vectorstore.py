import os

from chromadb import PersistentClient

from sentence_transformers import SentenceTransformer

from hybrid_search import keyword_search


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


def search_chunks(
    query,
    selected_documents=None
):
    
    keyword_results = keyword_search(
        query,
        selected_documents
    )

    query_embedding = model.encode(
        query
    ).tolist()

    if selected_documents:

        results = collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=5,
            where={
                "source": {
                    "$in": selected_documents
                }
            }
        )

    else:

        results = collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=5
        )

    print(results)

    semantic_docs = results["documents"][0]

    keyword_docs = [
        item[0]
        for item in keyword_results
    ]

    documents = list(
        dict.fromkeys(
            semantic_docs + keyword_docs
        )
    )
    
    documents = documents[:5]

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