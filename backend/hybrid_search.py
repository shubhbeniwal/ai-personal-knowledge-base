from chromadb import PersistentClient
from rank_bm25 import BM25Okapi


client = PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    "knowledge_base"
)


def keyword_search(query, selected_documents=None):

    if selected_documents:

        data = collection.get(
            where={
                "source": {
                    "$in": selected_documents
                }
            }
        )

    else:

        data = collection.get()

    documents = data["documents"]

    tokenized_docs = [
        doc.lower().split()
        for doc in documents
    ]

    bm25 = BM25Okapi(
        tokenized_docs
    )

    tokenized_query = (
        query.lower().split()
    )

    scores = bm25.get_scores(
        tokenized_query
    )

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:5]