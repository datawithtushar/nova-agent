from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

def get_embedding_model():
    """Load and return the Hugging Face embedding model."""

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    return embedding_model
