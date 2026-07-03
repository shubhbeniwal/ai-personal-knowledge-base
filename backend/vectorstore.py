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
    
    print(
        "COLLECTION COUNT:",
        collection.count()
    )
    
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
            n_results=10,
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
            n_results=10
        )

    print("\n--- Retrieval Results ---")

    for doc, distance in zip(
        results["documents"][0],
        results["distances"][0]
    ):
        print(
            f"\nDistance: {distance}"
        )
        print(
            doc[:150]
        )

    semantic_docs = []

    sources = []

    for doc, metadata, distance in zip(

        results["documents"][0],

        results["metadatas"][0],

        results["distances"][0]

    ):

        if distance < 1.8:

            semantic_docs.append(doc)

            sources.append(
                metadata["source"]
            )

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

    context = "\n".join(
        documents
    )

    return context, list(
        set(sources)
    )