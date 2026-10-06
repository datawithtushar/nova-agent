import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    PayloadSchemaType,
    Document,
)

from config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    QDRANT_COLLECTION_NAME,
    EMBEDDING_MODEL,
)


# --------------------------------------------------
# QDRANT CLIENT
# --------------------------------------------------

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    cloud_inference=True,
)


# --------------------------------------------------
# RETURN QDRANT CLIENT
# --------------------------------------------------

def get_qdrant_client():
    return client


# --------------------------------------------------
# VECTOR CONFIG
# --------------------------------------------------

VECTOR_SIZE = 384


# --------------------------------------------------
# CREATE COLLECTION
# --------------------------------------------------

def create_collection():

    if not client.collection_exists(
        collection_name=QDRANT_COLLECTION_NAME
    ):

        print(
            f"Creating Qdrant collection: "
            f"{QDRANT_COLLECTION_NAME}"
        )

        client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

    else:

        print(
            f"Using existing Qdrant collection: "
            f"{QDRANT_COLLECTION_NAME}"
        )


    # --------------------------------------------------
    # CREATE PAYLOAD INDEX
    # --------------------------------------------------

    try:

        client.create_payload_index(
            collection_name=QDRANT_COLLECTION_NAME,
            field_name="metadata.source",
            field_schema=PayloadSchemaType.KEYWORD,
        )

        print(
            "Created payload index: metadata.source"
        )

    except Exception:

        print(
            "Payload index metadata.source already exists."
        )


# --------------------------------------------------
# DELETE OLD DOCUMENT CHUNKS
# --------------------------------------------------

def delete_document_chunks(file_path):

    create_collection()

    client.delete(
        collection_name=QDRANT_COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="metadata.source",
                    match=MatchValue(
                        value=str(file_path)
                    ),
                )
            ]
        ),
        wait=True,
    )


# --------------------------------------------------
# CREATE DETERMINISTIC POINT ID
# --------------------------------------------------

def create_point_id(document):

    source = str(
        document.metadata.get(
            "source",
            ""
        )
    )

    page = str(
        document.metadata.get(
            "page",
            ""
        )
    )

    content = document.page_content

    unique_value = (
        f"{source}|{page}|{content}"
    )

    return str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            unique_value
        )
    )


# --------------------------------------------------
# STORE CHUNKS
# --------------------------------------------------

def store_chunks(chunks):

    if not chunks:

        print(
            "No chunks to store."
        )

        return None


    create_collection()

    points = []


    for chunk in chunks:

        point_id = create_point_id(
            chunk
        )


        point = PointStruct(
            id=point_id,

            vector=Document(
                text=chunk.page_content,
                model=EMBEDDING_MODEL,
            ),

            payload={
                "page_content": chunk.page_content,
                "metadata": chunk.metadata,
            },
        )


        points.append(
            point
        )


    client.upsert(
        collection_name=QDRANT_COLLECTION_NAME,
        points=points,
        wait=True,
    )


    print(
        f"Stored {len(points)} chunks in Qdrant."
    )

    return client