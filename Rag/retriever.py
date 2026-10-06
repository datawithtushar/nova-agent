from langchain_core.documents import Document as LangChainDocument
from qdrant_client.models import Document as QdrantDocument
from config import QDRANT_COLLECTION_NAME, QDRANT_URL, QDRANT_API_KEY, EMBEDDING_MODEL
from Rag.vector_store import get_qdrant_client
    

# Retriver for retriving the chunks-----------------------------------------------------------------

def retrieve_documents(question, top_k=5):
    """Retrieve relevant documents from the Qdrant collection based on the query."""
    client=get_qdrant_client()

    results= client.query_points(
        collection_name=QDRANT_COLLECTION_NAME,
        query=QdrantDocument(text=question,model=EMBEDDING_MODEL),
        limit=top_k,
        with_payload=True
    )


    documents = []

    for point in results.points:
        documents.append(LangChainDocument(page_content=point.payload["page_content"],metadata=point.payload["metadata"],))

    return documents


